from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from ipreport.filterset import EmployeeFilter
from ipreport.models import Employee
from ipreport.serializers import EmployeeSerializer, EmployeeListSerializer

from restapp.pagination import ResultsSetPagination


class EmployeeView(ListCreateAPIView):
    serializer_class = EmployeeListSerializer
    pagination_class = ResultsSetPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend)
    filterset_class = EmployeeFilter
    search_fields = ('fio', 'gender', 'phone', 'ip_address', 'ratsiya')
    ordering = ['id']

    def get_queryset(self):
        return Employee.objects.all()

    def post(self, request, **kwargs):
        serializer = EmployeeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=self.request.user)
        return Response(serializer.data, status.HTTP_201_CREATED)


class EmployeeDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        return Employee.objects.all()

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def get(self, request, pk):
        instance = get_object_or_404(Employee, id=pk)
        serializer = EmployeeListSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        instance = get_object_or_404(Employee, id=pk)
        serializer = self.serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=self.request.user)
        return Response(serializer.data, status.HTTP_202_ACCEPTED)
