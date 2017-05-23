from django import forms
from django.contrib import admin

from .models import Choice, Question, Master, PriceForRemodeling, PriceForTiling, PriceForWallsAndCeiling, \
    CardOfObjectForMaster, TypesOfWork


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)


class PriceForRemodelingInline(admin.TabularInline):
    model = PriceForRemodeling


class PriceForWallsAndCeilingInline(admin.TabularInline):
    model = PriceForWallsAndCeiling


class PriceForTilingInline(admin.TabularInline):
    model = PriceForTiling


class TypesOfWorkInline(admin.TabularInline):
    model = TypesOfWork


class CardOfObjectForMasterInline(admin.TabularInline):
    model = CardOfObjectForMaster


class CardOfObject(admin.ModelAdmin):
    model = CardOfObjectForMaster
    inlines = [TypesOfWorkInline]
    fieldsets = [
        (None,  {'fields': ['description', 'location', 'budged_from', 'budged_to']}),
    ]
    list_display = ('__str__', 'description', 'location', 'budged_from', 'budged_to')
    search_fields = ['description', 'location', 'budged_from', 'budged_to']
admin.site.register(CardOfObjectForMaster, CardOfObject)


class MasterAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,  {'fields': ['second_name', 'first_name', 'middle_name', 'phone_number', 'email', 'city', 'country',
                            'experience', 'additional_info']}),
    ]
    inlines = [PriceForRemodelingInline, PriceForWallsAndCeilingInline, PriceForTilingInline,
               CardOfObjectForMasterInline, ]
    list_display = ('second_name', 'first_name', 'middle_name', 'phone_number', 'email', 'city', 'country', 'experience')
    search_fields = ['second_name', 'first_name', 'middle_name', 'phone_number', 'email', 'city', 'country', 'experience']
admin.site.register(Master, MasterAdmin)

