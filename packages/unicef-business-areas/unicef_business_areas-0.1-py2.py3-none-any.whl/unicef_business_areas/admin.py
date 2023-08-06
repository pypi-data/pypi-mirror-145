import logging

from django.contrib import admin, messages
from django.contrib.admin import ModelAdmin

from admin_extra_buttons.decorators import button
from admin_extra_buttons.mixins import ExtraButtonsMixin

from .models import BusinessArea, Region
from .sync import load_business_area, load_region

logger = logging.getLogger(__name__)


@admin.register(Region)
class RegionAdmin(ExtraButtonsMixin, ModelAdmin):
    list_display = ['code', 'name']

    @button()
    def sync(self, request):
        load_region()


@admin.register(BusinessArea)
class BusinessAreaAdmin(ExtraButtonsMixin, ModelAdmin):
    list_display = ['code', 'name', 'long_name', 'region', 'country']
    list_filter = ['region', 'country']
    search_fields = ('name',)

    @button()
    def sync(self, request):
        try:
            load_business_area()
        except BaseException as e:
            logger.error(e)
            self.message_user(request, str(e), messages.ERROR)
