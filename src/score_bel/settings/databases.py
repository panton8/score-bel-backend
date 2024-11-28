import os

__all__ = (
    'DATABASES',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'scorebel_bs1l'),
        'USER': os.environ.get('POSTGRES_USER', 'scorebel'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 's1dBMyzJI72y3nmw1DrUe6nb3Dth7Hzs'),
        'HOST': os.environ.get('POSTGRES_HOST', 'dpg-ct4cn8d6l47c73f8ki90-a.frankfurt-postgres.render.com'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
        'TEST': {
            'NAME': 'test_score_bel_default',
        },
    }
}
