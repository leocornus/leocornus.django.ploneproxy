
# utils.py

"""
some utility methods.
"""

import httplib2
import urllib

from django.conf import settings
from django.core.urlresolvers import reverse

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

LEOCORNUS_HTTP_AGENT_NAME = 'Leocornus Django PloneProxy (httplib2 Agent)'
PLONEPROXY_REDIRECT_FIELD_NAME = 'next'
PLONEPROXY_TOKEN_FIELD_NAME = 'token'

PLONE_MAIL_PASSWORD_FORM = 'mail_password'
PLONE_PASSWORD_RESET_FORM = 'pwreset_form'
PLONE_PASSWORD_RESET_FINISH = 'pwreset_finish'

def getBaseURL(request):

    return '%s://%s' % (request.is_secure() and 'https' or 'http',
                        request.get_host())

def prepareOtherLang(request, redirectField, currentLang, tokenField=None):

    if currentLang == 'en':
        lang_code = 'fr'
        lang_name = 'Français'
    else:
        lang_code = 'en'
        lang_name = 'English'

    redirect_to = request.REQUEST.get(redirectField, '')

    paramName = settings.PLONEPROXY_LANG_FIELD_NAME

    # the new param
    newLang = '%s=%s' % (paramName, lang_code)
    lang_link = '%s?%s' % (request.path, newLang)
    if redirect_to != '':
        lang_link = '%s&%s=%s' % (lang_link, redirectField, redirect_to)

    if tokenField:
        token = request.REQUEST.get(tokenField, '')
        if token != '':
            lang_link = '%s&%s=%s' % (lang_link, tokenField, token)

    return (lang_name, lang_link)

def prepareForgotPasswordURL(request, redirect_field, current_lang):

    base_url = reverse('leocornus.django.ploneproxy.views.mailPassword')
    url = '%s?%s=%s' % (base_url, settings.PLONEPROXY_LANG_FIELD_NAME,
                        current_lang)

    redirect_to = request.REQUEST.get(redirect_field, None)
    if redirect_to:
        url = '%s&%s=%s' % (url, redirect_field, redirect_to)

    return url

def mailPlonePassword(request, redirect_to, userId):
    """
    post the mail_password request to Plone site and parse the response.
    If success, the response status will be 200.  Be careful here, 
    if Plone could not find userid, the response status is still 200.
    We need do more work to decide!
    """

    http = httplib2.Http()

    mailpw_url = buildPloneMailpwURL(request, redirect_to)

    headers = {}
    headers['Content-type'] = 'application/x-www-form-urlencoded'
    headers['User-Agent'] = LEOCORNUS_HTTP_AGENT_NAME

    mail_form = {}
    mail_form['userid'] = userId

    response, content = http.request(mailpw_url, 'POST', headers=headers,
                                     body=urllib.urlencode(mail_form))
    # parse the response to decide it is success or not!
    if response['status'] == '200':
        if content.find('<form name="%s"' % PLONE_MAIL_PASSWORD_FORM) > 0:
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

    baseURL = getBaseURL(request)
    if redirect_to.endswith('/'):
        return '%s%s%s' % (baseURL, redirect_to, PLONE_MAIL_PASSWORD_FORM)
    else:
        return '%s%s/%s' % (baseURL, redirect_to, PLONE_MAIL_PASSWORD_FORM)

def resetPlonePassword(request, redirect_to, token, userId, newPassword):
    """
    reset password for a Plone site.
    If success, Plone site will redirect the response to pwreset_finish,
    So the response status will be 302
    """

    http = httplib2.Http()
    pwreset_url = buildPlonePwresetURL(request, redirect_to)

    headers = {}
    headers['Content-type'] = 'application/x-www-form-urlencoded'
    headers['User-Agent'] = LEOCORNUS_HTTP_AGENT_NAME

    pwreset_form = {}
    pwreset_form['randomstring'] = token
    pwreset_form['userid'] = userId
    pwreset_form['password'] = newPassword
    pwreset_form['password2'] = newPassword
    pwreset_form['form.submitted'] = '1'

    response, content = http.request(pwreset_url, 'POST', headers=headers,
                                     body=urllib.urlencode(pwreset_form))

    # parse the response
    if response['status'] == '302' and \
       response['location'].endswith(PLONE_PASSWORD_RESET_FINISH):
        return True
    else:
        return False

def buildPlonePwresetURL(request, redirect_to):

    baseURL = getBaseURL(request)
    if redirect_to.endswith('/'):
        return '%s%s%s' % (baseURL, redirect_to, PLONE_PASSWORD_RESET_FORM)
    else:
        return '%s%s/%s' % (baseURL, redirect_to, PLONE_PASSWORD_RESET_FORM)
