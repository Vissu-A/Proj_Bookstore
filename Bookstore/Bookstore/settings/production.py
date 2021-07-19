from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'bookstore-db.czjpnwmwrggk.us-east-2.rds.amazonaws.com',
        'PORT': '3306',
        'USER': 'vissu',
        'PASSWORD': 'vissu6793',
        'NAME': 'bookstore',
        'OPTIONS': {
            # 'read_default_file': os.path.join(BASE_DIR, 'my.cnf'),
            'init_command': 'SET default_storage_engine=INNODB',
        },
    }
}
