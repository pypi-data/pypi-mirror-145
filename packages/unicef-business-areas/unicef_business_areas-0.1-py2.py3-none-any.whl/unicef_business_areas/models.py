from django.db import models
from django.utils.translation import gettext as _

from django_countries.fields import CountryField

app_label = 'unicef_business_areas'


class TimeStampedModel:
    last_modify_date = models.DateTimeField(editable=False, blank=True, auto_now_add=True,
                                            auto_now=True)


class Region(models.Model, TimeStampedModel):
    code = models.CharField(_('code'), max_length=10, unique=True)
    name = models.CharField(_('name'), max_length=50, unique=True)

    class Meta:
        app_label = 'unicef_business_areas'

    def __str__(self):
        return f"{self.name}"


class AbstractBusinessArea(models.Model, TimeStampedModel):
    code = models.CharField(_('code'), max_length=10, unique=True)
    name = models.CharField(_('name'), max_length=50, unique=True)
    long_name = models.CharField(_('long name'), max_length=150)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    country = CountryField()

    class Meta:
        app_label = 'unicef_business_areas'
        abstract = True
        verbose_name = _('Business Area')
        verbose_name_plural = _('Business Areas')

    def __str__(self):
        return f"{self.name}"


class BusinessArea(AbstractBusinessArea, TimeStampedModel):
    class Meta:
        app_label = 'unicef_business_areas'
        swappable = 'BUSINESSAREA_MODEL'
