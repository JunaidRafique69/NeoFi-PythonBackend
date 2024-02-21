"""
Views for Note API.
"""
from drf_spectacular.utils import (
    extend_schema_view,
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
)
from django.db.models import Q
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Note, NoteVersionHistory, NoteShare
from .serializers import NoteSerializer,NoteDetailSerializer, NoteVersionHistorySerializer, NoteShareSerializer
from .permissions import IsOwnerOrAdminOrShared, IsVersionAccessible

from django.contrib.auth import get_user_model
User = get_user_model()





@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                "notes",
                OpenApiTypes.STR,
                description="Comma separated list of IDs to filter.",
            )
        ]
    )
)
class NoteViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """View for manage note APIs."""

    serializer_class = NoteSerializer
    queryset = Note.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrAdminOrShared]

    def _params_to_ints(self, qs):
        """Convert a list of strings to integers."""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        """Retrieve notes for authenticated user, including shared notes."""
        user = self.request.user

        queryset = self.queryset.filter(
            Q(user=user) | Q(shared_with=user)
        ).order_by("-id").distinct()

        return queryset

    def perform_create(self, serializer):
        """Create a new note."""
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        note = self.get_object()
        serializer.save()
        NoteVersionHistory.objects.create(
            note=note,
            title=note.title,
            content=note.content
        )
    
    def get_serializer_class(self):
        """Return appropriate serializer class based on the request method."""
        if self.request.method in ["GET", "HEAD"]:
            return NoteDetailSerializer
        else:
            return NoteSerializer


class NoteVersionHistoryAPIView(APIView):
    """
    APIView for retrieving versions of a specific note.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsVersionAccessible]

    def get(self, request, *args, **kwargs):
        """
        Retrieve all versions for a specific note.
        """
        note_id = kwargs['pk']
        versions = NoteVersionHistory.objects.filter(note__id=int(note_id)).order_by('-updated_at')
        serializer = NoteVersionHistorySerializer(versions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class NoteShareViewSet(viewsets.ModelViewSet):
    queryset = NoteShare.objects.all()
    serializer_class = NoteShareSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrAdminOrShared]
    def create(self, request, *args, **kwargs):
        """
        Create a new shared note with a user.
        """
        try:
            note_id = request.data.get('note')
            user_id = request.data.get('shared_with')

            note = Note.objects.get(pk=note_id)
            user = User.objects.get(pk=user_id)

            if NoteShare.objects.filter(note=note, shared_with=user).exists():
                return Response({'detail': 'Note is already shared with this user.'}, status=status.HTTP_400_BAD_REQUEST)

            NoteShare.objects.create(note=note, shared_with=user)
            return Response({'detail': 'Note shared successfully.'}, status=status.HTTP_201_CREATED)

        except (Note.DoesNotExist, User.DoesNotExist):
            return Response({'detail': 'Note or user not found.'}, status=status.HTTP_404_NOT_FOUND)

    
@api_view(["GET"])
def health_check(request):
    """Returns successful response."""
    return Response({"healthy": True})
