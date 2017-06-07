from collections import OrderedDict

from betterforms.multiform import MultiModelForm
from django import forms
from django.forms import ModelForm, Textarea, MultiWidget, TextInput, MultiValueField, CharField
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime  # for checking renewal date range.

from phonenumber_field.widgets import PhoneNumberPrefixWidget

from designers.models import Designers, PriceList, CardOfObjectForDesigner, Photo

date_field_errors = {
    'required': 'Это поле обязятельно для заполнения',
    'invalid': 'Введите дату в формате ГГГГ-ММ или ГГГГ или количество лет',
    'unique': 'Пользователь с таким логином уже существует',
    'password': 'пароли не совпали'
}


class DesignerForm(ModelForm):
    class Meta:
        model = Designers
        widgets = {
            'description': Textarea(attrs={'cols': 40, 'rows': 5}),
        }
        fields = (
            'group', 'name', 'phone_number', 'email', 'address', 'working_area', 'distance_work', 'experience',
            'website',
            'minimal_order', 'description', 'brigade')


class PriceListForm(ModelForm):
    class Meta:
        model = PriceList
        fields = ('full_design_project', 'supervision', 'decorating_of_premises', 'consulting', 'working_project',
                  "three_d_visualisation")


class CardOfObjectForDesignerForm(ModelForm):
    three_d_visualisation = forms.FileField(
        label='Выберите файл',
        help_text='максимальный размер 42 MB',
        widget=forms.FileInput(attrs={'class': 'upload'})
    )

    class Meta:
        model = CardOfObjectForDesigner
        fields = ('description', 'location', 'budged_from', 'budged_to', 'three_d_visualisation')


class DesignerCreationMultiForm(MultiModelForm):
    form_classes = OrderedDict((
        ('designers', DesignerForm),
        ('price_list', PriceListForm),
    ))


class PhotoForm(forms.ModelForm):
    file = forms.FileField(
        label='Выберите файл',
        help_text='максимальный размер 42 MB',
        widget=forms.FileInput(attrs={'class': 'upload'})
    )

    class Meta:
        model = Photo
        fields = ('title', 'description', 'file',)
