DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Information Desk', 'info@resiskane.se'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'resiskane',
        'USER': 'david',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

TIME_ZONE = 'Europe/Stockholm'

LANGUAGE_CODE = 'sv-se'

SITE_ID = 1

USE_I18N = True

USE_L10N = True

MEDIA_ROOT = ''

MEDIA_URL = 'http://resiskane.se/media/'

ADMIN_MEDIA_PREFIX = '/admin_media/'

if not DEBUG:
    import secret_key
    SECRET_KEY = secret_key.SECRET_KEY
else:
    SECRET_KEY = None

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

STATIC_DOC_ROOT = './static'

ROOT_URLCONF = 'resiskane.urls'

TEMPLATE_DIRS = (

)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'resiskane.planner',
    'resiskane.skotte',
    'south'
)
