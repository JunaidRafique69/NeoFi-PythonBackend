"""
Urls mappings for the recipe app.
"""
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import NoteViewSet, NoteVersionHistoryAPIView, NoteShareViewSet

from django.urls import (
    path,
    include,
)

router = DefaultRouter()
router.register("notes", NoteViewSet)


app_name = "note"

urlpatterns = [
    path("", include(router.urls)),
     path("notes/note-versions/<int:pk>/", NoteVersionHistoryAPIView.as_view(),
         name="note-version-detail"),
    path("note-share/", NoteShareViewSet.as_view({"post": "create"}), name="note-share-create"),
]
