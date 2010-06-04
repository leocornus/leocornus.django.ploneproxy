
# modpython.py

"""
A PythonAuthenHandler implementation based on mod_python.  This is depends
on mod_python to be install in your Python environment.
"""

import os
import re

from datetime import datetime
from datetime import timedelta

from mod_python import apache
from mod_python import util
from mod_python import Cookie

from leocornus.django.ploneproxy.utils import LEOCORNUS_HTTP_HEADER_KEY
from leocornus.django.ploneproxy.utils import LEOCORNUS_HTTP_HEADER_VALUE
from leocornus.django.ploneproxy.utils import PLONEPROXY_REDIRECT_FIELD_NAME
from leocornus.django.ploneproxy.utils import PLONEPROXY_TOKEN_FIELD_NAME
from leocornus.django.ploneproxy.utils import PLONE_LOGIN_FORM
from leocornus.django.ploneproxy.utils import PLONE_MAIL_PASSWORD_FORM
from leocornus.django.ploneproxy.utils import PLONE_PASSWORD_RESET_FORM
from leocornus.django.ploneproxy.utils import PLONE_LOGOUT

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

def authenhandler(request):
    """
    a very simple PythonAuthenHandler based on Django's default Session
    management.
    """

    request.user = ''
    options = request.get_options()

    if request.unparsed_uri.endswith(PLONE_LOGOUT):
        # logout request.
        logout_url = options.get('PLONEPROXY_LOGOUT_URL', '/ext/logout')
        util.redirect(request, logout_url)
        return apache.OK

    if isGreenRequest(request):
        return apache.OK

    pwreset = checkPasswordresetRequest(request)
    if len(pwreset) > 0:
        pwreset_url = options.get('PLONEPROXY_PWRESET_URL',
                                  '/ext/password_reset')
        # we will use the default Django REDIRECT_FIELD_NAME: next
        util.redirect(request, "%s?%s=%s&%s=%s" % \
                      (pwreset_url,
                       PLONEPROXY_REDIRECT_FIELD_NAME, pwreset[0][0],
                       PLONEPROXY_TOKEN_FIELD_NAME, pwreset[0][1]))
        return apache.OK

    if isValidSession(request):
        return apache.OK
    else:
        # introduce a Python option for the login url, so we could configure
        # it in httpd.conf, PythonOption or SetEnv
        login_url = options.get('PLONEPROXY_LOGIN_URL', '/ext/login')
        # we will use the default Django REDIRECT_FIELD_NAME: next
        util.redirect(request, "%s?%s=%s" % \
                      (login_url,
                       PLONEPROXY_REDIRECT_FIELD_NAME, request.unparsed_uri))
        return apache.HTTP_UNAUTHORIZED

def isGreenRequest(req):
    """
    green request will be pass through without authentication, there are only
    2 green requests now: mail_password and pwrest_form
    """

    if not (req.unparsed_uri.endswith(PLONE_LOGIN_FORM) or \
            req.unparsed_uri.endswith(PLONE_MAIL_PASSWORD_FORM) or \
            req.unparsed_uri.endswith(PLONE_PASSWORD_RESET_FORM)):
        # not qualified.
        return False

    if not req.headers_in.has_key(LEOCORNUS_HTTP_HEADER_KEY):
        return False

    if req.headers_in[LEOCORNUS_HTTP_HEADER_KEY] != LEOCORNUS_HTTP_HEADER_VALUE:
        return False

    if req.connection.local_ip != req.connection.remote_ip:
        # make sure the request is sent from local machine.
        return False

    # everything looks fine now!
    return True

def checkPasswordresetRequest(req):
    """
    it is quiet easy for now.
    """

    return re.findall(r'(.*)/passwordreset/([0-9a-zA-Z]{32})$',
                      req.unparsed_uri)

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
            if isResourcesRequest(req):
                # just pass
                return True
            # this is a valid session, update the expre date!
            expiry = settings.SESSION_COOKIE_AGE
            session.expire_date = datetime.now() + timedelta(seconds=expiry)
            session.save()
            return True
        else:
            return False
    finally:
        db.connection.close()

def isResourcesRequest(req):
    """
    session less means not need update expire date.
    """

    if not (req.unparsed_uri.endswith('css') or \
            req.unparsed_uri.endswith('js') or \
            req.unparsed_uri.endswith('kss') or \
            req.unparsed_uri.endswith('gif') or \
            req.unparsed_uri.endswith('jpg') or \
            req.unparsed_uri.endswith('png')):
        # not qualified.
        return True

    # everything looks fine now!
    return True
