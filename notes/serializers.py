"""
Serializers for Recipe APIS
"""
from rest_framework import serializers
from .models import Note, NoteVersionHistory, NoteShare


class NoteSerializer(serializers.ModelSerializer):
    """Serializer for notes."""

    class Meta:
        model = Note
        fields = ["id", "title", "content"]
        read_only_fields = ["id"]

class NoteDetailSerializer(serializers.ModelSerializer):
    """Serializer for notes."""

    class Meta:
        model = Note
        fields = "__all__"
        read_only_fields = ["id"]

class NoteVersionHistorySerializer(serializers.ModelSerializer):
    """Serializer for notes versions."""

    class Meta:
        model = NoteVersionHistory
        fields = "__all__"
        read_only_fields = ["id"]

class NoteShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteShare
        fields = '__all__'