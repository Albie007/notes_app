"""
Notes App Models
Defines the Note model linked to Django's built-in User model.
"""

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Note(models.Model):
    """
    Represents a user's note with title, content, and timestamps.
    Each note belongs to a single user via ForeignKey.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notes',
        help_text='The owner of this note.'
    )
    title = models.CharField(
        max_length=200,
        help_text='Title of the note.'
    )
    content = models.TextField(
        help_text='Body content of the note.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Timestamp when the note was created.'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text='Timestamp when the note was last updated.'
    )

    class Meta:
        ordering = ['-updated_at']
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Returns the URL for the detail view of this note."""
        return reverse('notes_app:note-detail', kwargs={'pk': self.pk})
