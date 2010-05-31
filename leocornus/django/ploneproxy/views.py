
# views.py

"""
django view classes for leocornus.django.ploneproxy
"""

import httplib2

from django.conf import settings
from django.contrib.auth import authenticate

from django.shortcuts import render_to_response
from django.contrib.sites.models import Site
from django.contrib.sites.models import RequestSite
from django.http import HttpResponseRedirect
from django.template import RequestContext

from django.utils.translation import get_language
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache

from utils import PLONEPROXY_REDIRECT_FIELD_NAME
from utils import PLONEPROXY_TOKEN_FIELD_NAME
from utils import getBaseURL
from utils import buildPloneLoginURL
from utils import prepareOtherLang
from utils import prepareForgotPasswordURL
from utils import mailPlonePassword
from utils import resetPlonePassword

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

def login(request, template_name='login.html',
          redirect_field_name=PLONEPROXY_REDIRECT_FIELD_NAME):
    """
    Displays the login form and handles the login action.
    """

    redirect_to = request.REQUEST.get(redirect_field_name, '')
    resDict = {}
    

    if request.method == "POST":

        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        # keep user name.
        resDict['username'] = username

        # Light security check -- make sure redirect_to isn't garbage.
        if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
            resDict['invalid_url'] = 'Invalid URL! Please double check your url!'
        elif username == '' or password == '':
            # all fields are required!
            resDict['invalid_fields'] = 'All fields must be filled in'
        else:
            loginurl = buildPloneLoginURL(request, redirect_to)
            user = authenticate(username=username, password=password,
                                loginurl=loginurl)
            if user is None:
                resDict['invalid_cred'] = 'Please enter a correct username and password'
            else:
                from django.contrib.auth import login
                login(request, user)

                # looks like everything is fine now.
                if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()

                return HttpResponseRedirect(redirect_to)

    request.session.set_test_cookie()
    if Site._meta.installed:
        current_site = Site.objects.get_current()
    else:
        current_site = RequestSite(request)
    resDict['site'] = current_site
    resDict['site_name'] = current_site.name

    # decide another available language.
    lang = get_language()
    lang_name, lang_link = prepareOtherLang(request, redirect_field_name, lang)
    resDict[settings.PLONEPROXY_LANG_FIELD_NAME] = lang
    resDict['lang_name'] = lang_name
    resDict['lang_link'] = lang_link

    resDict[redirect_field_name] = redirect_to

    # url for forgot password.
    resDict['forgot_pw_url'] = prepareForgotPasswordURL(request,
                                                        redirect_field_name,
                                                        lang)

    return render_to_response(template_name, resDict,
                              context_instance=RequestContext(request))

login = never_cache(login)

def logout(request, template_name='logout.html'):

    resDict = {}

    # decide another available language.
    lang = get_language()
    lang_name, lang_link = prepareOtherLang(request, 'fake', lang)
    resDict['lang_name'] = lang_name
    resDict['lang_link'] = lang_link

    from django.contrib.auth.views import logout
    logout(request)

    return render_to_response(template_name, resDict,
                              context_instance=RequestContext(request))

def mailPassword(request, template_name='mail_password.html',
                 redirect_field_name=PLONEPROXY_REDIRECT_FIELD_NAME):
    """
    view class to handle user mail password request.
    """

    responseDict = {}

    redirect_to = request.REQUEST.get(redirect_field_name, '')
    responseDict[redirect_field_name] = redirect_to

    userId = request.REQUEST.get('userid', '')
    responseDict['userid'] = userId

    # preparing the other lanaguage
    lang = get_language()
    lang_name, lang_link = prepareOtherLang(request, redirect_field_name, lang)
    responseDict[settings.PLONEPROXY_LANG_FIELD_NAME] = lang
    responseDict['lang_name'] = lang_name
    responseDict['lang_link'] = lang_link

    if request.method == 'POST':

        if userId == '':
            # not valid request.
            responseDict['error'] = 'we got error!'
            responseDict['no_userid'] = 'userid is required'
        elif redirect_to != '':
            # send request to Plone and wait for response.
            if mailPlonePassword(request, redirect_to, userId):
                responseDict['confirm_mail_password'] = 'mail password confirm!'
            else:
                # handle other errors.
                responseDict['error'] = 'we got error!'
                responseDict['invalid_userid'] = 'could not find user id!'
        else:
            responseDict['error'] = 'error'
            responseDict['invalid_url'] = 'the url you provided is not valid!'

    return render_to_response(template_name, responseDict,
                              context_instance=RequestContext(request))

def passwordReset(request, template_name='password_reset.html',
                  redirect_field_name=PLONEPROXY_REDIRECT_FIELD_NAME):
    """
    view class for user to reset password.
    """

    responseDict = {}

    redirect_to = request.REQUEST.get(redirect_field_name, '')
    responseDict[redirect_field_name] = redirect_to

    userId = request.REQUEST.get('userid', '')
    responseDict['userid'] = userId
    token = request.REQUEST.get(PLONEPROXY_TOKEN_FIELD_NAME, '')
    responseDict[PLONEPROXY_TOKEN_FIELD_NAME] = token

    # preparing the other lanaguage
    lang = get_language()
    lang_name, lang_link = prepareOtherLang(request, redirect_field_name,
                                            lang, PLONEPROXY_TOKEN_FIELD_NAME)
    responseDict[settings.PLONEPROXY_LANG_FIELD_NAME] = lang
    responseDict['lang_name'] = lang_name
    responseDict['lang_link'] = lang_link

    if request.method == 'POST':

        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if token == '' or redirect_to == '':
            # not valid url.
            responseDict['error'] = 'error'
            responseDict['invalid_url'] = 'the url you provided is not valid!'
        elif userId == '':
            # not valid request.
            responseDict['error'] = 'we got error!'
            responseDict['no_userid'] = 'userid is required'
        elif password1 == '' or password2 == '':
            responseDict['error'] = 'we got error!'
            responseDict['no_password'] = 'both passwords are required'
        elif password1 != password2:
            responseDict['error'] = 'we got error!'
            responseDict['password_no_match'] = 'password not match!'
        else:
            # everything is fine now!
            # send request to Plone and wait for response.
            if resetPlonePassword(request, redirect_to, token, userId,
                                  password1):
                responseDict['confirm_password_reset'] = 'password success!'
                responseDict['redirect_link'] = '%s%s' % (getBaseURL(request),
                                                          redirect_to)
            else:
                # handle other errors.
                responseDict['error'] = 'we got error!'
                responseDict['password_reset_fail'] = 'reset password fail!'

    return render_to_response(template_name, responseDict,
                              context_instance=RequestContext(request))
