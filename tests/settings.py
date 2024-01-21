DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "django-cursor-pagination",
        "USER": "django-cursor-pagination",
        "PASSWORD": "django-cursor-pagination",
        "HOST": "localhost",
        "PORT": "5432",
    }
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': 'django-cursor-pagination.sqlite3',
    # }
}

INSTALLED_APPS = ["tests"]

SECRET_KEY = "secret"

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
