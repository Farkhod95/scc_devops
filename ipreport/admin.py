from django.contrib import admin

from ipreport.models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display =  ('fio', 'avatar', 'gender', 'type', 'phone', 'email', 'date_of_birthday',
                  'department', 'position', 'region', 'district', 'ip_address', 'updated_time', 'mac_address', 'vpn',
                  'ratsiya', 'domen', 'file_pdf', 'time_of_employment', 'time_to_go_to_work',)
    fields =  ('fio', 'avatar', 'gender', 'type', 'phone', 'email', 'date_of_birthday',
                  'department', 'position', 'region', 'district', 'ip_address', 'updated_time', 'mac_address', 'vpn',
                  'ratsiya', 'domen', 'file_pdf', 'time_of_employment', 'time_to_go_to_work',)
    search_fields = ('fio', 'phone', 'email', 'date_of_birthday', 'department', 'position', 'region', 'district')
