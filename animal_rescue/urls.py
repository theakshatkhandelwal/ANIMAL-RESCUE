"""
URL configuration for animal_rescue project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('rescue.urls')),
]

# Serve media files in both development and production
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    # Serve media files in production (for Render)
    # Note: For production, consider using cloud storage (AWS S3, Cloudinary) instead
    # Render's filesystem is ephemeral, so uploaded files may be lost on restart
    media_root = settings.MEDIA_ROOT
    if os.path.exists(media_root):
        urlpatterns += [
            re_path(r'^media/(?P<path>.*)$', serve, {
                'document_root': media_root,
                'show_indexes': False,
            }),
        ]


