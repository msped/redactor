from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Case, Document
from .serializers import (
    CaseSerializer, CaseDetailSerializer, DocumentSerializer)


class CaseListCreateView(ListCreateAPIView):
    """
    API view to list and create cases.
    """
    permission_classes = [IsAuthenticated]
    queryset = Case.objects.all()
    serializer_class = CaseSerializer

    def perform_create(self, serializer):
        """
        Override to set the created_by field to the current user.
        """
        serializer.save(created_by=self.request.user)


class CaseDetailView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a case.
    """
    permission_classes = [IsAuthenticated]
    queryset = Case.objects.all()
    serializer_class = CaseDetailSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'case_id'

    def perform_update(self, serializer):
        """
        Override to set the updated_by field to the current user.
        """
        serializer.save(updated_by=self.request.user)


class DocumentListCreateView(ListCreateAPIView):
    """
    API view to list and create documents for a specific case.
    Handles multiple file uploads in a single request.
    """
    permission_classes = [IsAuthenticated,]
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()
    lookup_field = 'case__id'
    lookup_url_kwarg = 'case_id'

    def create(self, request, *args, **kwargs):
        """
        frontend should send files under the 'original_file'
        key in a multipart/form-data request.
        """
        case_id = self.kwargs.get('case_id')
        case = get_object_or_404(Case, pk=case_id)

        files = request.FILES.getlist('original_file')
        if not files:
            return Response(
                {'detail': 'No files were provided in the request.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        documents_data = [{'case': case.pk, 'original_file': f} for f in files]
        serializer = self.get_serializer(data=documents_data, many=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class DocumentDetailView(RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a document.
    """
    permission_classes = [IsAuthenticated]
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'document_id'
