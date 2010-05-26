
# views.py

"""
django view classes for leocornus.django.ploneproxy
"""

import httplib2
import urllib

from django.core.urlresolvers import reverse

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.forms import AuthenticationForm

from django.shortcuts import render_to_response
from django.contrib.sites.models import Site
from django.contrib.sites.models import RequestSite
from django.http import HttpResponseRedirect
from django.template import RequestContext

from django.utils.translation import get_language
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache

from leocornus.django.ploneproxy import LEOCORNUS_HTTP_AGENT_NAME

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

def login(request, template_name='login.html',
          redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Displays the login form and handles the login action.
    """

    redirect_to = request.REQUEST.get(redirect_field_name, '')
    resDict = {}

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Light security check -- make sure redirect_to isn't garbage.
            if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL
            
            from django.contrib.auth import login
            login(request, form.get_user())

            # looks like everything is fine now.
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return HttpResponseRedirect(redirect_to)
        else:
            # invalid form input!
            if form.errors.has_key('__all__'):
                resDict['invalid_cred'] = 'Please enter a correct username and password'
            else:
                resDict['invalid_fields'] = 'All fields must be filled in'
    else:
        form = AuthenticationForm(request)

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

    resDict['form'] = form
    resDict[redirect_field_name] = redirect_to

    # url for forgot password.
    resDict['forgot_pw_url'] = prepareForgotPasswordURL(request.REQUEST,
                                                        redirect_field_name,
                                                        lang)

    return render_to_response(template_name, resDict,
                              context_instance=RequestContext(request))

login = never_cache(login)

def prepareOtherLang(request, redirect_field, currentLang):

    if currentLang == 'en':
        lang_code = 'fr'
        lang_name = 'Français'
    else:
        lang_code = 'en'
        lang_name = 'English'

    redirect_to = request.REQUEST.get(redirect_field, '')

    paramName = settings.PLONEPROXY_LANG_FIELD_NAME

    # the new param
    newLang = '%s=%s' % (paramName, lang_code)
    lang_link = '%s?%s' % (request.path, newLang)
    if redirect_to != '':
        lang_link = '%s&%s=%s' % (lang_link,
                                  redirect_field, redirect_to)

    return (lang_name, lang_link)

def prepareForgotPasswordURL(request, redirect_field, current_lang):

    base_url = reverse('leocornus.django.ploneproxy.views.mailPassword')
    url = '%s?%s=%s' % (base_url, settings.PLONEPROXY_LANG_FIELD_NAME,
                        current_lang)

    redirect_to = request.get(redirect_field, None)
    if redirect_to:
        url = '%s&%s=%s' % (url, redirect_field, redirect_to)

    return url
    

def mailPassword(request, template_name='mail_password.html',
                 redirect_field_name=REDIRECT_FIELD_NAME):
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
            if mailPlonePassword(buildPloneMailpwURL(request, redirect_to),
                                 userId):
                responseDict['confirm_mail_password'] = 'mail password confirm!'
            else:
                # handle other errors.
                responseDict['error'] = 'we got error!'
                responseDict['invalid_userid'] = 'could not find user id!'
        else:
            responseDict['error'] = 'error'
            responseDict['invalid_url'] = 'the url you provided is not valid!'

    return render_to_response(template_name,
                              responseDict,
                              context_instance=RequestContext(request))

def mailPlonePassword(ploneMailpwURL, userId):

    http = httplib2.Http()

    headers = {}
    headers['Content-type'] = 'application/x-www-form-urlencoded'
    headers['User-Agent'] = LEOCORNUS_HTTP_AGENT_NAME

    mail_form = {}
    mail_form['userid'] = userId

    response, content = http.request(ploneMailpwURL, 'POST', headers=headers,
                                     body=urllib.urlencode(mail_form))
    # parse the response to decide it is success or not!
    if response['status'] == '200':
        if content.find('<form name="mail_password"') > 0:
            # could not find user name
            return False
        else:
            # everything should be fine now!
            return True
    else:
        return False

def buildPloneMailpwURL(request, redirect_to):

    """
    make Plone mail password url by adding mail_password at the end.
    """

    baseURL = '%s://%s' % (request.is_secure() and 'https' or 'http',
                           request.get_host())
    if redirect_to.endswith('/'):
        return '%s%s%s' % (baseURL, redirect_to, 'mail_password')
    else:
        return '%s%s/%s' % (baseURL, redirect_to, 'mail_password')
