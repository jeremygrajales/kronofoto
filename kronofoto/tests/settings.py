import os

SECRET_KEY = 'fake-key'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GOOGLE_RECAPTCHA_SECRET_KEY = '6LfrDaYZAAAAAIh-2I4jNHweoV3hsN2l6WLsVKB3'
GOOGLE_RECAPTCHA_SITE_KEY = '6LfrDaYZAAAAACy95Wcr9vVMp2MmlFogL8ouwl52'
GOOGLE_TAG_ID = 'GTM-P4BQ99S'

GOOGLE_MAPS_KEY = 'AIzaSyCpvd2OrbPbk0_9iE4UEpq6k_Qi1_KaLwQ'
GRID_DISPLAY_COUNT = 3

MEDIA_ROOT = os.path.join(BASE_DIR, 'media2', 'media')


KF_DJANGOCMS_NAVIGATION = False
KF_DJANGOCMS_SUPPORT = False
KF_DJANGOCMS_ROOT = 'iowa'
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'archive.apps.ArchiveConfig',
    'django.contrib.gis',
    'django.contrib.sites',
    'gtm',
]
ROOT_URLCONF = 'tests.urls'
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.spatialite',
        'NAME': ":memory:",
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
SITE_ID = 1
MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
]
LOCAL_CONTEXTS = 'https://anth-ja77-lc-dev-42d5.uc.r.appspot.com/api/v1/'
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    },
}
