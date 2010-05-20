# Django settings for first project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = '/usr/local/rd/django/test-db/simple1.db'             # Or path to database file if using sqlite3.
TEST_DATABASE_NAME = '/usr/local/rd/django/test-db/simple-test.db'             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '@!+pn=pph&o30zaz)u$pq&kx5zy_y_v%-25+#es@91#h0%zgql'

# default is sessionid
SESSION_COOKIE_NAME = 'ctssessionid'
# The age of session cookies, in seconds
SESSION_COOKIE_AGE = 300
# default is False.
#SESSION_SAVE_EVERY_REQUEST = True

AUTHENTICATION_BACKENDS = (
    'leocornus.django.ploneproxy.authen.backends.PloneModelBackend',
#    'django.contrib.auth.backends.ModelBackend',
    )

# setting for leocornus.django.ploneproxy
PLONEPROXY_AUTHEN_URL = 'http://internal.host.name/Plone/login_form'
PLONEPROXY_COOKIE_NAME = '__ac'
PLONEPROXY_LANG_FIELD_NAME = 'ldp_lang'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'leocornus.django.ploneproxy.authen.middleware.PloneCookieMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'leocornus.django.ploneproxy.middleware.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'leocornus.django.ploneproxy.urls'

TEMPLATE_DIRS = (
    #'/usr/local/rd/django/playground/first/templates',
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'leocornus.django.ploneproxy',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'leocornus.django.ploneproxy.authen',
)
