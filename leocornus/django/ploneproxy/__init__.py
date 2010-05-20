
# __init__.py

"""
we will set up default values for new introduced settings.
"""

from django.conf import settings

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
