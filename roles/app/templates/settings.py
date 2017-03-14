DATABASES = {
  'default' : {
    'ENGINE': 'django.contrib.gis.db.backends.postgis',
    'NAME': '{{ db_name }}',
    'USER': '{{ db_name }}',
    'PASSWORD': '{{ db_password }}',
    'HOST': 'localhost',
    'PORT': '5432',
  }
}

# Static & medias stored in data dir
MEDIA_ROOT = "{{ dir }}/data/medias"
STATIC_ROOT = "{{ dir }}/data/static"

# Static & medias through cdn
STATIC_URL = 'https://{{ hostname }}/static/'
MEDIA_URL = 'https://{{ hostname }}/medias/'

# Webpack
WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'dist/',
        'STATS_FILE': '{{ dir }}/backend/front/dist/webpack-stats.json',
    }
}

# Cache on FS
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '{{ dir }}/cache',
        'TIMEOUT' : None, # No cache
    }
}

# Cached templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            '{{ dir }}/backend/src/templates',
        ],
        'OPTIONS': {
            'loaders' : [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]),
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'mobili.middlewares.version'
            ],
        },
    },
]


# Shared cookies with plans
ALLOWED_HOSTS = [
  '{{ hostname }}',
  'www.{{ hostname }}',
]
SESSION_COOKIE_DOMAIN = '.{{ hostname }}'
SESSION_COOKIE_NAME = 'mobili.auth'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_DOMAIN = '.{{ hostname }}'
CSRF_COOKIE_NAME = 'mobili.csrf'
CSRF_COOKIE_SECURE = True

# Do not use bower
STATICFILES_DIRS = [
    '{{ dir }}/backend/front',
    '{{ dir }}/backend/help',
]

# Setup frontend
FRONTEND_SCREEN_URL = 'https://my.{{ hostname }}/#/screen/{}'
FRONTEND_SCREEN_SHARED_URL = 'https://my.{{ hostname }}/#/share/{}/{}'

# Sentry error reporting
import raven
import os
RAVEN_CONFIG = {
    'dsn': '{{ raven_dsn }}',
    'release': raven.fetch_git_sha('{{ dir }}/backend'),
}

# Custom Config
{% for k,v in django.items() %}
{% if v is none %}
{{ k }} = None
{% elif v is sameas True %}
{{ k }} = True
{% elif v is sameas False %}
{{ k }} = False
{% elif v is number %}
{{ k }} = {{ v }}
{% elif v is string %}
{{ k }} = '{{ v }}'
{% elif v is mapping %}
{{ k }} = {
  {% for kk, vv in v.items() %}
  '{{ kk }}' : '{{ vv }}',
  {% endfor %}
}
{% elif v is sequence %}
{{ k }} = [
  {% for vv in v %}
  '{{ vv }}',
  {% endfor %}
]
{% endif %}
{% endfor %}
