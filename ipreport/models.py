from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator

from directory.models import Region, District, Country, Department, Position
from restapp.models import BaseModel


class Employee(BaseModel):
    GENDERS = (
        ('male', _('Male')),
        ('female', _('Female')),
    )

    TYPES = (
        ('leadership', _('Rahbariyat')),
        ('structure_of_center', _('Markaz tarkibiy tuzilmasi')),
        ('regional_sector_specialist', _('Hududiy sektor mutaxassisi')),
    )

    fio = models.CharField(_('First name'), max_length=255, blank=True, null=True)
    avatar = models.ImageField(upload_to='employee/%Y/%m/%d', null=True)
    gender = models.CharField(choices=GENDERS, max_length=6, null=True, blank=True, )
    type = models.CharField(choices=TYPES, max_length=50, null=True, blank=True, )
    reception_time = models.CharField(_('Reception time'), max_length=255, null=True, blank=True)
    working_time = models.CharField(_('working time'), max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(_('phone'), max_length=255, null=True, blank=True)
    email = models.EmailField(_('email address'), blank=True, null=True)
    date_of_birthday = models.DateField(_('date of birthday'), null=True, blank=True, )
    department = models.ForeignKey(Department, related_name='employee_department', on_delete=models.SET_NULL, null=True,
                                   blank=True)
    position = models.ForeignKey(Position, related_name='employee_position', on_delete=models.SET_NULL, null=True,
                                   blank=True)
    region = models.ForeignKey(Region, related_name='employee_region', on_delete=models.SET_NULL, null=True,
                                   blank=True)
    district = models.ForeignKey(District, related_name='district_region', on_delete=models.SET_NULL, null=True,
                               blank=True)
    department_head = models.ForeignKey('self', verbose_name=_('Bo‘lim boshligi'), related_name='subordinates', on_delete=models.SET_NULL, null=True, blank=True,)

    ip_address = models.CharField(max_length=255, null=True, blank=True, unique=True)
    mac_address = models.CharField(max_length=255, null=True, blank=True, unique=True)
    vpn = models.CharField(max_length=255, null=True, blank=True, unique=True)
    domen = models.CharField(max_length=255, null=True, blank=True, unique=True)
    ratsiya = models.CharField(max_length=255, null=True, blank=True, unique=True)
    file_pdf = models.FileField(blank=True, null=True, upload_to='open_data/%Y/%m/%d')
    time_of_employment = models.DateField(_('Ishga kirgan vaqti'), null=True, blank=True, )
    time_to_go_to_work = models.DateField(_('Ishga ketgan vaqti'), null=True, blank=True, )
    pc_name = models.CharField(max_length=255, null=True, blank=True)


    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')


class WlanParent(BaseModel):
    name = models.CharField(_('Name'), max_length=255, blank=True, null=True)
    ip_address = models.CharField(max_length=255, null=True, blank=True, unique=True)
    mask = models.CharField(_('Name'), max_length=255, blank=True, null=True)
    gateway = models.CharField(max_length=255, null=True, blank=True, unique=True)
    text = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = _('Wlan Parent')
        verbose_name_plural = _('Wlan Parent')


class Wlan(BaseModel):
    parent = models.ForeignKey(WlanParent, related_name='wlan_parents', on_delete=models.SET_NULL, null=True, blank=True)
    port_number = models.CharField(max_length=255, null=True, blank=True, unique=True)
    wlan_id = models.CharField(max_length=255, null=True, blank=True, unique=True)
    name = models.CharField(_('Name'), max_length=255, blank=True, null=True)
    ip_address = models.CharField(max_length=255, null=True, blank=True, unique=True)
    maska = models.CharField(max_length=255, null=True, blank=True)
    gateway = models.CharField(max_length=255, null=True, blank=True)


    class Meta:
        verbose_name = _('Wlan')
        verbose_name_plural = _('Wlan')


class DeviceType(BaseModel):
    name = models.CharField(max_length=255, null=True, blank=True, unique=True)

    class Meta:
        verbose_name = _('Device Type')
        verbose_name_plural = _('Device Type')


class IpAddress(BaseModel):
    ip_address = models.CharField(max_length=255, null=True, blank=True, unique=True)
    pc_name = models.CharField(max_length=255, null=True, blank=True)
    mask = models.CharField(_('Name'), max_length=255, blank=True, null=True)
    gateway = models.CharField(max_length=255, null=True, blank=True, unique=True)
    type = models.ForeignKey(DeviceType, related_name='ip_device', on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField(null=True, blank=True)


    class Meta:
        verbose_name = _('Ip Address')
        verbose_name_plural = _('Ip Address')


class IpAddressInfo(BaseModel):
    STATUS = (
        ('active', _('Active')),
        ('inactive', _('Inactive')),
    )
    pc_name = models.CharField(max_length=255, null=True, blank=True)
    ipaddress = models.ForeignKey(IpAddress, related_name='ipaddress_1', on_delete=models.SET_NULL, null=True, blank=True)
    employee = models.ForeignKey(Employee, related_name='ipaddress_info', on_delete=models.SET_NULL, null=True, blank=True)
    ip_address = models.CharField(max_length=255, null=True, blank=True, unique=True)
    status = models.CharField(choices=STATUS, default='inactive', max_length=50, null=True, blank=True, )
    mac_address = models.CharField(_('MAC address'), max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = _('Ip Address Info')
        verbose_name_plural = _('Ip Address Info')


class CameraType(BaseModel):
    name = models.CharField(max_length=255, null=True, blank=True, unique=True)

    class Meta:
        verbose_name = _('Camera Type')
        verbose_name_plural = _('Camera Type')


class Camera(BaseModel):
    image = models.ImageField(upload_to='camera/%Y/%m/%d', null=True)
    ip_address = models.CharField(max_length=255, null=True, blank=True, unique=True)
    maska = models.CharField(_('Maska'), max_length=255, blank=True, null=True)
    gateway = models.CharField(max_length=255, null=True, blank=True, unique=True)
    model = models.CharField(max_length=255, null=True, blank=True, unique=True)
    serial_number = models.CharField(max_length=255, null=True, blank=True, unique=True)
    type = models.ForeignKey(CameraType, related_name='camera_type', on_delete=models.SET_NULL, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = _('Camera')
        verbose_name_plural = _('Camera')


