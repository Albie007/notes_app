"""
Notes App Admin Configuration
Register the Note model so admins can manage all notes.
"""

from django.contrib import admin
from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    """Admin interface for the Note model."""
    list_display = ('title', 'user', 'created_at', 'updated_at')
    list_filter = ('user', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-updated_at',)
