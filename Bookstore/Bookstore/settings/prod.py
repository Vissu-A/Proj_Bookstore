from .base import *

DEBUG = False

ALLOWED_HOSTS = ['3.128.88.4', 'book.webfordemo.xyz']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': credentials['prod_host'],
        'PORT': credentials['prod_port'],
        'USER': credentials['prod_user'],
        'PASSWORD': credentials['prod_pwd'],
        'NAME': credentials['prod_name'],
        'OPTIONS': {
            # 'read_default_file': os.path.join(BASE_DIR, 'my.cnf'),
            'init_command': 'SET default_storage_engine=INNODB',
        },
    }
}


# allauth creates redirect url in http by default, adding this line will make allauth create https  redirect urls
ACCOUNT_DEFAULT_HTTP_PROTOCOL='https' 