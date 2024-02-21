"""
Notes Database models.
"""
from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()



class Note(models.Model):
    """Note model to storing user notes."""

    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    shared_with = models.ManyToManyField(User, through='NoteShare', related_name='share_notes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class NoteShare(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='shared_with_users')
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_notes')

    class Meta:
        unique_together = ('note', 'shared_with')

class NoteVersionHistory(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='history')
    title = models.CharField(max_length=100)
    content = models.TextField()
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.note.title} (version at {self.updated_at})"