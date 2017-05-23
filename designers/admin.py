from django import forms
from django.contrib import admin

from .models import PriceList, Designers, CardOfObjectForDesigner


class PriceListInline(admin.TabularInline):
    model = PriceList


class CardOfObjectForDesignerInline(admin.TabularInline):
    model = CardOfObjectForDesigner


class DesignersAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'phone_number', 'email', 'experience', 'address', 'working_area', 'distance_work',
                           'website', 'minimal_order', 'description', 'brigade']}),
    ]
    inlines = [PriceListInline, CardOfObjectForDesignerInline]
    list_display = ('name', 'phone_number', 'email', 'experience', 'address', 'working_area', 'distance_work',
                    'website', 'minimal_order', 'description', 'brigade')
    search_fields = ('name', 'phone_number', 'email', 'experience', 'address', 'working_area', 'distance_work',
                     'website', 'minimal_order', 'description', 'brigade')


admin.site.register(Designers, DesignersAdmin)
