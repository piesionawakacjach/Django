from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']
SECRET_KEY = 'h8(6h=1ulv)d8wyv=06&^db-wx4-k9oi(2ne2r-vl)^zrki%*0'
# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


