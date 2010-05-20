
# __init__.py

"""
some middleware classes for leocornus.django.ploneproxy
"""

from django.conf import settings
from django.utils.cache import patch_vary_headers
from django.utils import translation

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

# using the Plone site's default cookie name.
settings.PLONEPROXY_COOKIE_NAME = getattr(settings, 'PLONEPROXY_COOKIE_NAME',
                                          '__ac')

# using localhost:8080
settings.PLONEPROXY_AUTHEN_URL = getattr(settings, 'PLONEPROXY_AUTHEN_URL',
                                         'http://localhost:8080/Plone/login_form')

# the default language field name
settings.PLONEPROXY_LANG_FIELD_NAME = getattr(settings, 'PLONEPROXY_LANG_FIELD_NAME',
                                              'ldp_lang')
class LocaleMiddleware(object):
    """
    This middleware is copied from the default Django LocaleMiddleware.
    We try to provide one more choice for use to pick the prefer language
    from the request parameter, which could be configured through the
    PLONEPROXY_LANG_PARAM_NAME.
    """

    def process_request(self, request):

        langParam = request.REQUEST.get(settings.PLONEPROXY_LANG_FIELD_NAME,
                                        '')
        if langParam != '':
            language = langParam
        else:
            language = translation.get_language_from_request(request)

        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()

    def process_response(self, request, response):
        patch_vary_headers(response, ('Accept-Language',))
        if 'Content-Language' not in response:
            response['Content-Language'] = translation.get_language()
        translation.deactivate()
        return response
