from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from directory.filterset import DepartmentFilter
from directory.models import Department
from directory.serializers import DepartmentSerializer, DepartmentListSerializer

from restapp.pagination import ResultsSetPagination
from rest_framework.permissions import AllowAny


class DepartmentPublicView(ListCreateAPIView):
    serializer_class = DepartmentListSerializer
    pagination_class = ResultsSetPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend)
    filterset_class = DepartmentFilter
    search_fields = ('name_ru', 'name_en', 'name_uz')
    ordering = ['-pk']
    permission_classes = (AllowAny,)
    http_method_names = ['get']

    def get_queryset(self):
        return Department.objects.all()


class DepartmentDetailPublicView(APIView):
    serializer_class = DepartmentSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['get']

    def get(self, request, pk):
        region = get_object_or_404(Department, id=pk)
        serializer = DepartmentListSerializer(region)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DepartmentView(ListCreateAPIView):
    serializer_class = DepartmentListSerializer
    pagination_class = ResultsSetPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend)
    filterset_class = DepartmentFilter
    search_fields = ('name_ru', 'name_en', 'name_uz')
    ordering = ['-pk']

    def get_queryset(self):
        return Department.objects.all()

    def post(self, request, **kwargs):
        serializer = DepartmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=self.request.user)
        return Response(serializer.data, status.HTTP_201_CREATED)


class DepartmentDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        return Department.objects.all()

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def get(self, request, pk):
        region = get_object_or_404(Department, id=pk)
        serializer = DepartmentListSerializer(region)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        department = get_object_or_404(Department, id=pk)
        serializer = self.serializer_class(department, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=self.request.user)
        return Response(serializer.data, status.HTTP_202_ACCEPTED)
