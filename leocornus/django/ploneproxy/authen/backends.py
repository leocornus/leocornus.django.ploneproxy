
# backends.py

"""
Django authentication backend implementation for ploneproxy.
"""

import urllib
import httplib2
from Cookie import SimpleCookie

from django.db import connection
from django.contrib.auth.models import User
from django.conf import settings

from leocornus.django.ploneproxy.authen.models import PloneAuthenState

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

class PloneModelBackend(object):
    """
    Authenticates against a Plone site!
    """

    # TODO: Model, login attribute name and password attribute name should be
    # configurable.
    def authenticate(self, username=None, password=None):

        ploneCookie = self.authPloneUser(username, password)
        if ploneCookie:
            cookieName, cookieValue = ploneCookie
            try:
                user = User.objects.get(username=username)

            except User.DoesNotExist:
                # create a user object for this new user.
                # save first name, email, ...
                user = User.objects.create(username=username)
                user.set_unusable_password()

            # setup the cookie object based on the user id.
            ploneCookie = PloneAuthenState(user_id=user.id, status='valid',
                                           cookie_name=cookieName,
                                           cookie_value=cookieValue)
            ploneCookie.save()
            return user
        #elif lockout:
        #    # Plone user locked out, provide proper message!
        #    # ask for password reset process.
        #    # return the user object with different cookie value!
        #    return None
        else:
            # not valid plone user
            return None

    def authPloneUser(self, username, password):

        http = httplib2.Http()

        login_url = settings.PLONEPROXY_AUTHEN_URL

        headers = {}
        headers['Content-type'] = 'application/x-www-form-urlencoded'
        headers['User-Agent'] = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'

        login_form = {}
        login_form['__ac_name'] = username
        login_form['__ac_password'] = password
        login_form['cookies_enabled'] = '1'
        login_form['js_enabled'] = '0'
        login_form['form.submitted'] = '1'
        body = urllib.urlencode(login_form)

        try:
            res, cont = http.request(login_url, 'POST',
                                     headers=headers, body=body)
        except Exception:
            # not valid login url!
            return None
        
        if res.has_key('set-cookie'):
            cookie = SimpleCookie()
            cookie.load(res['set-cookie'])

            cookieName = settings.PLONEPROXY_COOKIE_NAME
            if cookie.has_key(cookieName):

                cookieValue = cookie.get(cookieName).value
                return (cookieName, cookieValue)

        # no valid cookie found!
        return None

    def has_perm(self, user_obj, perm):
        return perm in self.get_all_permissions(user_obj)

    def has_module_perms(self, user_obj, app_label):
        """
        Returns True if user_obj has any permissions in the given app_label.
        """
        for perm in self.get_all_permissions(user_obj):
            if perm[:perm.index('.')] == app_label:
                return True
        return False

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
