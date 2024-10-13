from django.urls import include, re_path

from .v1.routers.router import router

urlpatterns = [
    re_path(r'^v1/', include((router.urls, 'v1')))
]

