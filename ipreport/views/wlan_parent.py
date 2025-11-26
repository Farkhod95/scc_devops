# views/WlanParent.py
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from ipreport.filterset import WlanParentFilter
from ipreport.models import WlanParent
from ipreport.serializers import WlanParentSerializer, WlanParentListSerializer

from restapp.pagination import ResultsSetPagination
from restapp.utils.responses import nonContent


class WlanParentFieldInfoView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        field_info = []
        for field in WlanParent._meta.fields:
            field_info.append({
                "field_name": field.name,
                "verbose_name": str(field.verbose_name),
                "help_text": str(field.help_text) if field.help_text else "",
                "type": field.get_internal_type(),
                "max_length": getattr(field, 'max_length', None),
                "choices": dict(field.choices) if field.choices else None
            })
        return Response(field_info)


class WlanParentView(ListCreateAPIView):
    serializer_class = WlanParentListSerializer
    pagination_class = ResultsSetPagination
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend)
    filterset_class = WlanParentFilter
    search_fields = ('name', 'ip_address', 'mask')
    ordering = ['id']

    def get_queryset(self):
        return WlanParent.objects.all()

    def post(self, request):
        serializer = WlanParentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=self.request.user)
        return Response(serializer.data, status.HTTP_201_CREATED)


class WlanParentDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = WlanParentSerializer

    def get_queryset(self):
        return WlanParent.objects.all()

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def get(self, request, pk):
        instance = get_object_or_404(WlanParent, id=pk)
        serializer = WlanParentListSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        instance = get_object_or_404(WlanParent, id=pk)
        serializer = self.serializer_class(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(updated_by=self.request.user)
        return Response(serializer.data, status.HTTP_202_ACCEPTED)

    def delete(self, request, pk):
        instance = get_object_or_404(WlanParent, id=pk)
        instance.delete()
        return Response(nonContent(), status.HTTP_204_NO_CONTENT)
