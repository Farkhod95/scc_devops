from rest_framework import serializers

from directory.serializers import RegionListPublicSerializer, DistrictListPublicSerializer, CountryListSerializer, \
    DepartmentListSerializer, PositionSerializer, RegionListSerializer, DistrictSerializer
from users.serializers import UserDetailSerializer
from .models import Employee, Wlan, DeviceType, IpAddress, IpAddressInfo, CameraType, Camera, WlanParent


# Tarjima asosiy serializeri
class LocaleSerializer(serializers.ModelSerializer):
    name_en = serializers.CharField(allow_blank=False)
    name_uz = serializers.CharField(allow_blank=False)
    name_ru = serializers.CharField(allow_blank=False)


class BaseLocaleSerializer(serializers.ModelSerializer):
    """
    Dinamik ko‘p tilli serializer:
    Modelda mavjud bo‘lgan *_en/_uz/_ru maydonlar avtomatik qo‘shiladi.
    """
    TRANSLATABLE_BASES = [
        # eng ko‘p uchraydiganlar
        'name',
    ]
    LANGS = ['en', 'uz', 'ru']
    REQUIRED_BASES = {'name', }  # muhim maydonlar

    def get_fields(self):
        fields = super().get_fields()
        model = getattr(self.Meta, 'model', None)
        if not model:
            return fields

        # Modeldagi real maydonlar to‘plami
        model_field_names = {f.name for f in model._meta.get_fields()}

        for base in self.TRANSLATABLE_BASES:
            for lang in self.LANGS:
                f_name = f"{base}_{lang}"
                if f_name in model_field_names:
                    fields[f_name] = serializers.CharField(
                        allow_blank=False,
                        required=(base in self.REQUIRED_BASES)
                    )
        return fields


class EmployeeHeadSerializer(LocaleSerializer):
    position_detail = PositionSerializer(source="position", read_only=True)

    class Meta:
        model = Employee
        fields = ("id", "fio", "avatar", "position", 'pc_name')


class EmployeeSerializer(LocaleSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'fio', 'avatar', 'gender', 'type', 'phone', 'email', 'date_of_birthday', 'pc_name',
                  'department', 'position', 'region', 'district', 'ip_address', 'updated_time', 'mac_address', 'vpn',
                  'ratsiya', 'domen', 'file_pdf', 'time_of_employment', 'time_to_go_to_work',)
        extra_kwargs = {
            'fio': {"required": True},
            'type': {"required": True},
        }


class EmployeeListSerializer(LocaleSerializer):
    department_detail = DepartmentListSerializer(source="department", read_only=True)
    position_detail = PositionSerializer(source="position", read_only=True)
    region_detail = RegionListSerializer(source="region", read_only=True)
    district_detail = DistrictSerializer(source="district", read_only=True)
    department_head_detail = EmployeeHeadSerializer(source="department_head", read_only=True)
    created_by_detail = UserDetailSerializer(source="created_by", read_only=True)
    updated_by_detail = UserDetailSerializer(source="updated_by", read_only=True)

    class Meta:
        model = Employee
        fields = ('id', 'fio', 'avatar', 'gender', 'type', 'phone', 'email', 'date_of_birthday', 'department', 'department_detail',
                  'position', 'position_detail', 'region', 'department_head', 'department_head_detail', 'pc_name',
                  'region_detail', 'district_detail', 'district', 'ip_address', 'updated_time', 'mac_address', 'vpn',
                  'ratsiya', 'domen', 'file_pdf', 'time_of_employment', 'time_to_go_to_work', 'created_time',
                  'updated_time', 'created_by', 'created_by_detail', 'updated_by', 'updated_by_detail',)


class EmployeePublicSerializer(LocaleSerializer):
    department_detail = DepartmentListSerializer(source="department", read_only=True)
    position_detail = PositionSerializer(source="position", read_only=True)

    class Meta:
        model = Employee
        fields = ('id', 'fio', 'avatar', 'gender', 'type', 'phone', 'email', 'date_of_birthday', 'pc_name',
                  'department', 'department_detail', 'position', 'position_detail', 'region', 'district', 'ip_address', 'updated_time', 'mac_address', 'vpn',
                  'ratsiya', 'domen', 'file_pdf', 'time_of_employment', 'time_to_go_to_work',)


class WlanParentSerializer(LocaleSerializer):
    class Meta:
        model = WlanParent
        fields = ('id', 'name', 'ip_address', 'mask', 'gateway', 'text')


class WlanParentListSerializer(LocaleSerializer):
    created_by_detail = UserDetailSerializer(source="created_by", read_only=True)
    updated_by_detail = UserDetailSerializer(source="updated_by", read_only=True)

    class Meta:
        model = WlanParent
        fields = ('id', 'name', 'ip_address', 'mask', 'gateway', 'text', 'created_time', 'updated_time',
                  'created_by', 'created_by_detail', 'updated_by', 'updated_by_detail')


class WlanSerializer(LocaleSerializer):
    class Meta:
        model = Wlan
        fields = ('id', 'parent', 'port_number', 'wlan_id', 'name', 'ip_address', 'maska', 'gateway')


class WlanListSerializer(LocaleSerializer):
    parent_detail = WlanParentSerializer(source="parent", read_only=True)
    created_by_detail = UserDetailSerializer(source="created_by", read_only=True)
    updated_by_detail = UserDetailSerializer(source="updated_by", read_only=True)

    class Meta:
        model = Wlan
        fields = ('id', 'parent', 'parent_detail', 'port_number', 'wlan_id', 'name', 'ip_address', 'maska', 'gateway', 'created_time', 'updated_time',
                  'created_by', 'created_by_detail', 'updated_by', 'updated_by_detail')


class DeviceTypeSerializer(LocaleSerializer):
    class Meta:
        model = DeviceType
        fields = ('id', 'name')


class IpAddressSerializer(LocaleSerializer):
    class Meta:
        model = IpAddress
        fields = ('id', 'ip_address', 'mask', 'gateway', 'type', 'text', 'pc_name')
        extra_kwargs = {
            'ip_address': {"required": True},
            'mask': {"required": True},
            'type': {"required": True},
        }


class IpAddressListSerializer(LocaleSerializer):
    type_detail = DeviceTypeSerializer(source="type", read_only=True)
    created_by_detail = UserDetailSerializer(source="created_by", read_only=True)
    updated_by_detail = UserDetailSerializer(source="updated_by", read_only=True)

    class Meta:
        model = IpAddress
        fields = ('id', 'ip_address', 'mask', 'gateway', 'type','type_detail', 'text', 'created_time', 'updated_time',
                  'created_by', 'created_by_detail', 'updated_by', 'updated_by_detail', 'pc_name',)


class IpAddressInfoSerializer(LocaleSerializer):
    class Meta:
        model = IpAddressInfo
        fields = ('id', 'pc_name', 'ipaddress', 'employee', 'ip_address', 'status', 'mac_address')
        extra_kwargs = {
            'ipaddress': {"required": True},
            'employee': {"required": True},
            'ip_address': {"required": True},
        }


class IpAddressInfoListSerializer(LocaleSerializer):
    ipaddress_detail = IpAddressSerializer(source="ipaddress", read_only=True)
    employee_detail = EmployeePublicSerializer(source="employee", read_only=True)
    created_by_detail = UserDetailSerializer(source="created_by", read_only=True)
    updated_by_detail = UserDetailSerializer(source="updated_by", read_only=True)

    class Meta:
        model = IpAddressInfo
        fields = ('id', 'pc_name', 'ipaddress', 'ipaddress_detail', 'employee', 'employee_detail', 'ip_address', 'status',
                  'created_time', 'updated_time', 'created_by', 'created_by_detail', 'updated_by', 'updated_by_detail',
                  'mac_address')


class CameraTypeSerializer(LocaleSerializer):
    class Meta:
        model = CameraType
        fields = ('id', 'name')


class CameraSerializer(LocaleSerializer):
    class Meta:
        model = Camera
        fields = ('id', 'image', 'ip_address', 'maska', 'gateway', 'model', 'serial_number', 'type', 'address')
        extra_kwargs = {
            'ip_address': {"required": True},
            'maska': {"required": True},
            'type': {"required": True},
        }


class CameraListSerializer(LocaleSerializer):
    type_detail = CameraTypeSerializer(source="type", read_only=True)
    created_by_detail = UserDetailSerializer(source="created_by", read_only=True)
    updated_by_detail = UserDetailSerializer(source="updated_by", read_only=True)

    class Meta:
        model = Camera
        fields = ('id', 'image', 'ip_address', 'maska', 'gateway', 'model', 'serial_number', 'type', 'type_detail',
                  'address', 'created_time', 'updated_time', 'created_by', 'created_by_detail', 'updated_by', 'updated_by_detail')
