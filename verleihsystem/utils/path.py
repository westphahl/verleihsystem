import os

from django.conf import settings


get_media_path = lambda x: os.path.join(settings.MEDIA_ROOT,x )
