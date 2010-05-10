
# modpython.py

"""
A PythonAuthenHandler implementation based on mod_python.  This is depends
on mod_python to be install in your Python environment.
"""

import os
import datetime

from mod_python import apache
from mod_python import util
from mod_python import Cookie

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

def authenhandler(request):

    request.user = ''

    if isValidSession(request):
        return apache.OK
    else:
        util.redirect(request, "/ext/login?next=%s" % request.unparsed_uri)
        return apache.HTTP_UNAUTHORIZED

def isValidSession(req):

    """
    Authentication handler that checks against Django's auth database.
    """

    cookies = Cookie.get_cookies(req)
    if not cookies.has_key('sessionid'):
        return False

    sessionId = cookies['sessionid'].value

    # mod_python fakes the environ, and thus doesn't process SetEnv.  This fixes
    # that so that the following import works
    os.environ.update(req.subprocess_env)

    # check for PythonOptions
    _str_to_bool = lambda s: s.lower() in ('1', 'true', 'on', 'yes')

    options = req.get_options()
    permission_name = options.get('DjangoPermissionName', None)
    staff_only = _str_to_bool(options.get('DjangoRequireStaffStatus', "on"))
    superuser_only = _str_to_bool(options.get('DjangoRequireSuperuserStatus', "off"))
    settings_module = options.get('DJANGO_SETTINGS_MODULE', None)
    if settings_module:
        os.environ['DJANGO_SETTINGS_MODULE'] = settings_module

    from django.contrib.sessions.models import Session
    from django import db
    db.reset_queries()

    try:
        try:
            session = Session.objects.get(pk=sessionId)
        except Session.DoesNotExist:
            return False

        if session.expire_date > datetime.datetime.now():
            return True
        else:
            return False
    finally:
        db.connection.close()

def authenhandlerOrg(request):

    """
    
    """

    # check for PythonOptions
    _str_to_bool = lambda s: s.lower() in ('1', 'true', 'on', 'yes')

    options = request.get_options()
    permission_name = options.get('DjangoPermissionName', None)               
    staff_only = _str_to_bool(options.get('DjangoRequireStaffStatus', "on"))
    superuser_only = _str_to_bool(options.get('DjangoRequireSuperuserStatus',
                                              "off"))
    settings_module = options.get('DJANGO_SETTINGS_MODULE', None)
    if settings_module:                                              
        os.environ['DJANGO_SETTINGS_MODULE'] = settings_module

    from django.contrib import admin
    admin.autodiscover()

    if (request.user == None) or (not admin.site.has_permission(request)):
        # not valid user!
        admin.site.login(request)
        return apache.HTTP_UNAUTHORIZED

    else: # cookie is valid
        return apache.OK
