from django.urls import re_path, path

from ipreport.views.camera import CameraView, CameraDetailView
from ipreport.views.camera_type import CameraTypeView, CameraTypeDetailView
from ipreport.views.device_type import DeviceTypeView, DeviceTypeDetailView
from ipreport.views.employee import EmployeeView, EmployeeDetailView
from ipreport.views.ip_address import IpAddressView, IpAddressDetailView
from ipreport.views.ip_address_info import IpAddressInfoView, IpAddressInfoDetailView
from ipreport.views.wlan import WlanView, WlanDetailView
from ipreport.views.wlan_parent import WlanParentView, WlanParentDetailView

urlpatterns = [
    re_path(r'^employee/$', EmployeeView.as_view(), name='employee_view'),
    path('employee/<int:pk>', EmployeeDetailView.as_view(), name='employee_detail_view'),

    re_path(r'^wlan-parent/$', WlanParentView.as_view(), name='wlan-parent-view'),
    path('wlan-parent/<int:pk>', WlanParentDetailView.as_view(), name='wlan-parent-detail-view'),

    re_path(r'^wlan/$', WlanView.as_view(), name='wlan-view'),
    path('wlan/<int:pk>', WlanDetailView.as_view(), name='wlan-detail-view'),

    re_path(r'^device-type/$', DeviceTypeView.as_view(), name='device-type-view'),
    path('device-type/<int:pk>', DeviceTypeDetailView.as_view(), name='device-type-detail-view'),

    re_path(r'^ip-address/$', IpAddressView.as_view(), name='ip-address-view'),
    path('ip-address/<int:pk>', IpAddressDetailView.as_view(), name='ip-address-detail-view'),

    re_path(r'^ip-address-info/$', IpAddressInfoView.as_view(), name='ip-address-info-view'),
    path('ip-address-info/<int:pk>', IpAddressInfoDetailView.as_view(), name='ip-address-info-detail-view'),

    re_path(r'^camera-type/$', CameraTypeView.as_view(), name='camera-type-view'),
    path('camera-type/<int:pk>', CameraTypeDetailView.as_view(), name='camera-type-detail-view'),

    re_path(r'^camera/$', CameraView.as_view(), name='camera-view'),
    path('camera/<int:pk>', CameraDetailView.as_view(), name='camera-detail-view'),
]
