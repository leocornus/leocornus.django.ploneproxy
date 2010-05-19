
# __init__.py

"""
some middleware classes for leocornus.django.ploneproxy
"""

from django.conf import settings
from django.utils.cache import patch_vary_headers
from django.utils import translation

__author__ = "Sean Chen"
__email__ = "sean.chen@leocorn.com"

class LocaleMiddleware(object):
    """
    This middleware is copied from the default Django LocaleMiddleware.
    We try to provide one more choice for use to pick the prefer language
    from the request parameter, which could be configured through the
    PLONEPROXY_LANG_PARAM_NAME.
    """

    def process_request(self, request):

        try:
            paramName = settings.PLONEPROXY_LANG_PARAM_NAME
            if not paramName:
                # set to None, then we use default.
                paramName = 'ldp_lang'
        except AttributeError:
            # using the default Plone cookie name.
            paramName = 'ldp_lang'

        langParam = request.REQUEST.get(paramName, None)
        if langParam:
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
