from modeltranslation.translator import register, TranslationOptions

from ipreport.models import DeviceType


@register(DeviceType)
class DeviceTypeTranslationOptions(TranslationOptions):
    fields = ('name',)
