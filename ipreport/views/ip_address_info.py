# views/IpAddressInfo.py
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from ipreport.filterset import IpAddressInfoFilter
from ipreport.models import IpAddressInfo
from ipreport.serializers import IpAddressInfoSerializer, IpAddressInfoListSerializer

from restapp.pagination import ResultsSetPagination
from restapp.utils.responses import nonContent


class IpAddressInfoFieldInfoView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        field_info = []
        for field in IpAddressInfo._meta.fields:
            field_info.append({
                "field_name": field.name,
                "verbose_name": str(field.verbose_name),
                "help_text": str(field.help_text) if field.help_text else "",
                "type": field.get_internal_type(),
                "max_length": getattr(field, 'max_length', None),
                "choices": dict(field.choices) if field.choices else None
            })
        return Response(field_info)


class IpAddressInfoView(ListCreateAPIView):
    serializer_class = IpAddressInfoListSerializer
    pagination_class = ResultsSetPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend)
    filterset_class = IpAddressInfoFilter
    search_fields = ('ip_address', 'employee__fio', 'mac_address', 'pc_name')
    ordering = ['id']

    def get_queryset(self):
        return IpAddressInfo.objects.all()

    def post(self, request):
        serializer = IpAddressInfoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=self.request.user)
        return Response(serializer.data, status.HTTP_201_CREATED)


class IpAddressInfoDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = IpAddressInfoSerializer

    def get_queryset(self):
        return IpAddressInfo.objects.all()

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def get(self, request, pk):
        instance = get_object_or_404(IpAddressInfo, id=pk)
        serializer = IpAddressInfoListSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        instance = get_object_or_404(IpAddressInfo, id=pk)
        serializer = self.serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=self.request.user)
        return Response(serializer.data, status.HTTP_202_ACCEPTED)

    def delete(self, request, pk):
        instance = get_object_or_404(IpAddressInfo, id=pk)
        instance.delete()
        return Response(nonContent(), status.HTTP_204_NO_CONTENT)
