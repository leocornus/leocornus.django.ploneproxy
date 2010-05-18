
# modpython.py

"""
A PythonAuthenHandler implementation based on mod_python.  This is depends
on mod_python to be install in your Python environment.
"""

import os
from datetime import datetime
from datetime import timedelta

from mod_python import apache
from mod_python import util
from mod_python import Cookie

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

def authenhandler(request):
    """
    a very simple PythonAuthenHandler based on Django's default Session
    management.
    """

    request.user = ''

    if isValidSession(request):
        return apache.OK
    else:
        # introduce a Python option for the login url, so we could configure
        # it in httpd.conf, PythonOption or SetEnv
        options = request.get_options()
        login_url = options.get('PLONEPROXY_LOGIN_URL', '/ext/login')
        # we will use the default Django REDIRECT_FIELD_NAME: next
        util.redirect(request, "%s?next=%s" % (login_url, request.unparsed_uri))
        return apache.HTTP_UNAUTHORIZED

def isValidSession(req):
    """
    check the Django's session table to decided this is a valid session or not.
    """

    # check for PythonOptions
    _str_to_bool = lambda s: s.lower() in ('1', 'true', 'on', 'yes')

    options = req.get_options()
    permission_name = options.get('DjangoPermissionName', None)
    staff_only = _str_to_bool(options.get('DjangoRequireStaffStatus', "on"))
    superuser_only = _str_to_bool(options.get('DjangoRequireSuperuserStatus', "off"))
    settings_module = options.get('DJANGO_SETTINGS_MODULE', None)
    if settings_module:
        os.environ['DJANGO_SETTINGS_MODULE'] = settings_module

    from django.conf import settings
    cookieName = settings.SESSION_COOKIE_NAME

    cookies = Cookie.get_cookies(req)
    if not cookies.has_key(cookieName):
        return False

    #import pdb; pdb.set_trace()
    sessionId = cookies[cookieName].value

    # mod_python fakes the environ, and thus doesn't process SetEnv.  This fixes
    # that so that the following import works
    os.environ.update(req.subprocess_env)

    from django.contrib.sessions.models import Session
    from django import db
    db.reset_queries()

    try:
        try:
            session = Session.objects.get(pk=sessionId)
        except Session.DoesNotExist:
            return False

        sessionData = session.get_decoded()
        if not sessionData.has_key('_auth_user_id'):
            # this is not a valid session!
            return False

        if session.expire_date > datetime.now():
            # this is a valid session, update the expre date!
            expiry = settings.SESSION_COOKIE_AGE
            session.expire_date = datetime.now() + timedelta(seconds=expiry)
            session.save()
            return True
        else:
            return False
    finally:
        db.connection.close()
