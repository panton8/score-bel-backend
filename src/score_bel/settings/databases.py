import os

__all__ = (
    'DATABASES',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'railway'),
        'USER': os.environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'ieDmvMgTpPKcyZtFHmrtoiSFpnyGyDxM'),
        'HOST': os.environ.get('POSTGRES_HOST', 'junction.proxy.rlwy.net'),
        'PORT': os.environ.get('POSTGRES_PORT', '26459'),
    }
}
