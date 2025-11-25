from modeltranslation.translator import register, TranslationOptions

from ipreport.models import DeviceType, CameraType


@register(DeviceType)
class DeviceTypeTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(CameraType)
class CameraTypeTranslationOptions(TranslationOptions):
    fields = ('name',)
