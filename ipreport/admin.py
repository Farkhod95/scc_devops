from django.contrib import admin

from ipreport.models import Employee, IpAddress, IpAddressInfo


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display =  ('fio', 'avatar', 'gender', 'type', 'phone', 'email', 'date_of_birthday',
                  'department', 'position', 'region', 'district', 'ip_address', 'updated_time', 'mac_address', 'vpn',
                  'ratsiya', 'domen', 'file_pdf', 'time_of_employment', 'time_to_go_to_work',)
    fields =  ('fio', 'avatar', 'gender', 'type', 'phone', 'email', 'date_of_birthday',
                  'department', 'position', 'region', 'district', 'ip_address', 'updated_time', 'mac_address', 'vpn',
                  'ratsiya', 'domen', 'file_pdf', 'time_of_employment', 'time_to_go_to_work',)
    search_fields = ('fio', 'phone', 'email', 'date_of_birthday', 'department', 'position', 'region', 'district')



@admin.register(IpAddress)
class IpAddressAdmin(admin.ModelAdmin):
    list_display = ('id', 'ip_address', 'pc_name', 'mask', 'gateway', 'type', 'text')
    fields = ('ip_address', 'pc_name', 'mask', 'gateway', 'type', 'text')
    search_fields = ('ip_address', 'pc_name',)



@admin.register(IpAddressInfo)
class IpAddressInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'ipaddress', 'ip_address', 'employee', 'pc_name', 'status', 'mac_address')
    fields = ('ipaddress', 'ip_address', 'employee', 'pc_name', 'status', 'mac_address')
    search_fields = ('ipaddress', 'employee', 'ip_address')