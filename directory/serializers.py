from rest_framework import serializers

from .models import Region, District, Country, Department, Position


# Tarjima asosiy serializeri
class LocaleSerializer(serializers.ModelSerializer):
    name_en = serializers.CharField(allow_blank=False)
    name_uz = serializers.CharField(allow_blank=False)
    name_ru = serializers.CharField(allow_blank=False)


class CountrySerializer(LocaleSerializer):
    class Meta:
        model = Country
        fields = ('id', 'code', 'name', 'name_en', 'name_uz', 'name_ru')
        extra_kwargs = {
            'code': {"required": True},
            'name_en': {"required": True},
            'name_uz': {"required": True},
            'name_ru': {"required": True},
        }


class CountryListSerializer(LocaleSerializer):
    class Meta:
        model = Country
        fields = ('id', 'code', 'name')


class RelatedRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ('id', 'name')


class RelatedDistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ('id', 'name')


class RelatedPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ('id', 'name')


class RegionSerializer(LocaleSerializer):
    class Meta:
        model = Region
        fields = ('id', 'code', 'name', 'name_en', 'name_uz', 'name_ru')
        extra_kwargs = {
            'code': {"required": True},
            'name_en': {"required": True},
            'name_uz': {"required": True},
            'name_ru': {"required": True},
        }


class RegionListSerializer(LocaleSerializer):
    class Meta:
        model = Region
        fields = ('id', 'code', 'name', 'name_en', 'name_uz', 'name_ru')


class RegionListPublicSerializer(LocaleSerializer):
    class Meta:
        model = Region
        fields = ('id', 'code', 'name')


class RegionListPublicSerializer(LocaleSerializer):
    class Meta:
        model = District
        fields = ('id', 'code', 'name')


class DistrictListPublicSerializer(LocaleSerializer):
    class Meta:
        model = District
        fields = ('id', 'code', 'name')


class DistrictListSerializer(LocaleSerializer):
    region_detail = RegionListSerializer(source='region', read_only=True)

    class Meta:
        model = District
        fields = ('id', 'code', 'name', 'name_en', 'name_uz', 'name_ru', 'region', 'region_detail')


class DistrictSerializer(LocaleSerializer):
    class Meta:
        model = District
        fields = ('id', 'code', 'name', 'name_en', 'name_uz', 'name_ru', 'region')
        extra_kwargs = {
            'code': {"required": True},
            'region': {"required": True},
            'name_en': {"required": True},
            'name_uz': {"required": True},
            'name_ru': {"required": True},
        }



class DepartmentListSerializer(LocaleSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name', 'name_uz', 'name_ru', 'name_en')


class DepartmentSerializer(LocaleSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name', 'name_uz', 'name_ru', 'name_en')
        extra_kwargs = {
            'name_uz': {"required": True},
            'name_ru': {"required": True},
            'name_en': {"required": True},
            'name_kr': {"required": True},
        }


class PositionSerializer(LocaleSerializer):
    class Meta:
        model = Position
        fields = ('id', 'name', 'name_uz', 'name_ru', 'name_en', 'department')
        extra_kwargs = {
            'name_uz': {"required": True},
            'name_ru': {"required": True},
            'name_en': {"required": True},
            'department': {"required": True},
        }


class PositionListSerializer(LocaleSerializer):
    department_detail = DepartmentListSerializer(source="department", read_only=True)

    class Meta:
        model = Position
        fields = ('id', 'name', 'name_uz', 'name_ru', 'name_en', 'department', 'department_detail')
