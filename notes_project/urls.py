"""
Project-level URL Configuration for notes_project.
Includes the admin site and all notes_app routes.
The root URL redirects to the notes list.
"""

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    # Root redirect to notes list
    path('', lambda request: redirect('notes/'), name='root-redirect'),
    # Include all notes_app URLs (auth + CRUD)
    path('', include('notes_app.urls')),
]
