"""
Notes App URL Configuration
Maps URL patterns to their corresponding views.
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'notes_app'

urlpatterns = [
    # ── Authentication ────────────────────────────────────────────────
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='notes_app/login.html',
        redirect_authenticated_user=True,
    ), name='login'),
    path('logout/', views.custom_logout, name='logout'),

    # ── Notes CRUD ────────────────────────────────────────────────────
    path('notes/', views.NoteListView.as_view(), name='note-list'),
    path('notes/add/', views.NoteCreateView.as_view(), name='note-create'),
    path('notes/<int:pk>/', views.NoteDetailView.as_view(), name='note-detail'),
    path('notes/<int:pk>/edit/', views.NoteUpdateView.as_view(), name='note-update'),
    path('notes/<int:pk>/delete/', views.NoteDeleteView.as_view(), name='note-delete'),
]
