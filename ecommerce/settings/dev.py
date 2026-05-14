from .settings import *

DEBUG = os.getenv("DEBUG", "False") == "True"

INSTALLED_APPS += [
    "silk", 
]
MIDDLEWARE += ["silk.middleware.SilkyMiddleware"] 

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


CELERY_BROKER_URL = "redis://localhost:6379/0"
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND")

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")