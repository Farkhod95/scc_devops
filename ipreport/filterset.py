from django_filters.rest_framework import FilterSet
from ipreport.models import Employee, Wlan, DeviceType, IpAddress, IpAddressInfo, CameraType, Camera, WlanParent, \
    EmployeeFile


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


class EmployeeFileFilter(FilterSet):

    class Meta:
        model = EmployeeFile
        fields = {
            'title': ['exact'],
        }


class WlanParentFilter(FilterSet):

    class Meta:
        model = WlanParent
        fields = {
            'name': ['exact'],
            'ip_address': ['exact'],
            'mask': ['exact'],
        }


class WlanFilter(FilterSet):

    class Meta:
        model = Wlan
        fields = {
            'wlan_id': ['exact'],
            'name': ['exact'],
            'ip_address': ['exact'],
            'parent': ['exact'],
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

class IpAddressInfoFilter(FilterSet):

    class Meta:
        model = IpAddressInfo
        fields = {
            'ipaddress': ['exact'],
            'employee': ['exact'],
            'ip_address': ['exact'],
            'status': ['exact'],
            'mac_address': ['exact'],
        }


class CameraTypeFilter(FilterSet):

    class Meta:
        model = CameraType
        fields = {
            'name': ['exact'],
        }



class CameraFilter(FilterSet):

    class Meta:
        model = Camera
        fields = {
            'ip_address': ['exact'],
            'maska': ['exact'],
            'type': ['exact'],
        }