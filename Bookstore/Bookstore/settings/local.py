from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': credentials['local_host'],
        'PORT': credentials['local_port'],
        'USER': credentials['local_user'],
        'PASSWORD': credentials['local_pwd'],
        'NAME': credentials['local_name'],
        'OPTIONS': {
            # 'read_default_file': os.path.join(BASE_DIR, 'my.cnf'),
            'init_command': 'SET default_storage_engine=INNODB',
        },
    }
}