from django_filters.rest_framework import FilterSet
from ipreport.models import Employee, Wlan, DeviceType, IpAddress


class EmployeeFilter(FilterSet):

    class Meta:
        model = Employee
        fields = {
            'fio': ['exact'],
            'position': ['exact'],
            'department': ['exact'],
            'region': ['exact'],
            'district': ['exact'],
            'type': ['exact'],
            'ip_address': ['exact'],
        }

class WlanFilter(FilterSet):

    class Meta:
        model = Wlan
        fields = {
            'wlan_id': ['exact'],
            'name': ['exact'],
            'ip_address': ['exact'],
        }


class DeviceTypeFilter(FilterSet):

    class Meta:
        model = DeviceType
        fields = {
            'name': ['exact'],
        }



class IpAddressFilter(FilterSet):

    class Meta:
        model = IpAddress
        fields = {
            'ip_address': ['exact'],
            'mask': ['exact'],
            'type': ['exact'],
        }
