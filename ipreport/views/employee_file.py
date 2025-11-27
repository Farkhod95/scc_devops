# views/EmployeeFile.py
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from ipreport.filterset import EmployeeFileFilter
from ipreport.models import EmployeeFile
from ipreport.serializers import EmployeeFileSerializer

from restapp.pagination import ResultsSetPagination
from restapp.utils.responses import nonContent


class EmployeeFileFieldInfoView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        field_info = []
        for field in EmployeeFile._meta.fields:
            field_info.append({
                "field_name": field.name,
                "verbose_name": str(field.verbose_name),
                "help_text": str(field.help_text) if field.help_text else "",
                "type": field.get_internal_type(),
                "max_length": getattr(field, 'max_length', None),
                "choices": dict(field.choices) if field.choices else None
            })
        return Response(field_info)


class EmployeeFileViewList(ListCreateAPIView):
    serializer_class = EmployeeFileSerializer
    pagination_class = ResultsSetPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend)
    filterset_class = EmployeeFileFilter
    search_fields = ('EmployeeFile_id', 'name')
    ordering = ['pk']
    permission_classes = (AllowAny,)
    http_method_names = ['get']

    def get_queryset(self):
        return EmployeeFile.objects.all()


class EmployeeFileView(ListCreateAPIView):
    serializer_class = EmployeeFileSerializer
    pagination_class = ResultsSetPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend)
    filterset_class = EmployeeFileFilter
    search_fields = (
        'EmployeeFile_id', 'name'
    )
    ordering = ['id']

    def get_queryset(self):
        return EmployeeFile.objects.all()

    def post(self, request):
        serializer = EmployeeFileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=self.request.user)
        return Response(serializer.data, status.HTTP_201_CREATED)


class EmployeeFileDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = EmployeeFileSerializer

    def get_queryset(self):
        return EmployeeFile.objects.all()

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def get(self, request, pk):
        instance = get_object_or_404(EmployeeFile, id=pk)
        serializer = EmployeeFileSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        instance = get_object_or_404(EmployeeFile, id=pk)
        serializer = self.serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=self.request.user)
        return Response(serializer.data, status.HTTP_202_ACCEPTED)

    def delete(self, request, pk):
        instance = get_object_or_404(EmployeeFile, id=pk)
        instance.delete()
        return Response(nonContent(), status.HTTP_204_NO_CONTENT)
