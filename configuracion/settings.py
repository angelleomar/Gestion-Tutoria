"""

Generado por 'django' usando Django 4.1.6.

"""

import os
import posixpath
import environ

env = environ.Env()

# Cree rutas dentro del proyecto de esta manera: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configuraciones de desarrollo de inicio rápido: no aptas para producción

# ADVERTENCIA DE SEGURIDAD: ¡mantenga en secreto la clave secreta utilizada en la producción!
SECRET_KEY = 'o!ld8nrt4vc*h1zoey*wj48x*q0#ss12h=+zh)kk^6b3aygg=!'

# ADVERTENCIA DE SEGURIDAD: ¡no ejecute con la depuración activada en producción!
DEBUG = True

ALLOWED_HOSTS = []

# cambiar los modelos de usuario predeterminados a nuestro modelo personalizado
AUTH_USER_MODEL = 'accounts.User' 

# Definición de la aplicación

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cleanup',
]

# Aplicaciones de terceros
INSTALLED_APPS += [
    'crispy_forms',
    'rest_framework',
    'channels',
]

# aplicaciones personalizadas
INSTALLED_APPS += [
    'app.apps.AppConfig',
    'accounts.apps.AccountsConfig',
  
    'course.apps.CourseConfig',

    'search.apps.SearchConfig',
 
  
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'configuracion.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'configuracion.wsgi.application'

ASGI_APPLICATION = "configuracion.asgi.application"




# BASES DE DATOS = {
#     'por defecto': {
# 'MOTOR': 'django.db.backends.sqlite3',
# 'NOMBRE': os.path.join(BASE_DIR, 'db.sqlite3'),
# }
# }

# --------------------------------------------
# Es posible que algunos campos del modelo no funcionen en sqlite db, así que configure su postgresql
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}

# https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-DEFAULT_AUTO_FIELD
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Validación de contraseña
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internacionalización
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Archivos estáticos (CSS, JavaScript, Imágenes)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATIC_ROOT = posixpath.join(*(BASE_DIR.split(os.path.sep) + ['staticfiles']))

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com' # Aquí estoy usando gmail como host de correo electrónico, pero puedes cambiarlo

EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('USER_EMAIL')
EMAIL_HOST_PASSWORD = os.environ.get('USER_PASSWORD')

CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ]
}


STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')
