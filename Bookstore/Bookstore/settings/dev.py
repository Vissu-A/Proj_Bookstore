from .base import *

DEBUG = True

ALLOWED_HOSTS = ['3.128.88.4', 'book.webfordemo.xyz']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': credentials['dev_host'],
        'PORT': credentials['dev_port'],
        'USER': credentials['dev_user'],
        'PASSWORD': credentials['dev_pwd'],
        'NAME': credentials['dev_name'],
        'OPTIONS': {
            # 'read_default_file': os.path.join(BASE_DIR, 'my.cnf'),
            'init_command': 'SET default_storage_engine=INNODB',
        },
    }
}
