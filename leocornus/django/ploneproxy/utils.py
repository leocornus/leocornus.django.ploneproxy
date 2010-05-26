
# utils.py

"""
some utility methods.
"""

import httplib2
import urllib

from django.conf import settings
from django.core.urlresolvers import reverse

from leocornus.django.ploneproxy import LEOCORNUS_HTTP_AGENT_NAME

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

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

    redirect_to = request.REQUEST.get(redirect_field, None)
    if redirect_to:
        url = '%s&%s=%s' % (url, redirect_field, redirect_to)

    return url

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
