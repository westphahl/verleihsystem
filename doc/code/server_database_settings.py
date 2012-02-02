DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'verleihsystem',
        'USER': 'verleihsystem',
        'PASSWORD': '',
        'HOST': 'neptun.fbe.fh-weingarten.de', 
        'PORT': '3306',
        'OPTIONS': {
           'init_command': 'SET storage_engine=INNODB',
        }
    }
}
