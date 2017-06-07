from collections import OrderedDict

from django.contrib.auth import get_user_model
from django.forms import ModelForm, DateField, SelectDateWidget, Textarea, TextInput, FileInput, FileField
from django.forms.models import inlineformset_factory
from betterforms.multiform import MultiModelForm
from masters.models import Master, PriceForWallsAndCeiling, PriceForRemodeling, PriceForTiling, Photo, CardOfObjectForMaster
from django.forms import formset_factory


class MasterForm(ModelForm):
    # experience = DateField(widget=SelectDateWidget(years=range(1980, 2017), ))
    class Meta:
        model = Master
        widgets = {
            'additional_info': Textarea(attrs={'cols': 40, 'rows': 5}),
            'experience': TextInput(attrs={'placeholder': '5 или 2012'})
        }
        fields = (
            'group', 'first_name', 'second_name', 'middle_name', 'country', 'city', 'phone_number', 'email',
            'experience',
            'additional_info')


PriceForRemodelingFormSet = inlineformset_factory(Master, PriceForRemodeling, extra=0,
                                                  fields=('overhaul', 'remodeling', 'party_remodeling'))
PriceForWallsAndCeilingFormSet = inlineformset_factory(Master, PriceForWallsAndCeiling, extra=0, fields=(
    'alignment', 'plaster', 'putty', 'undercoat', 'colorizing_ceil_and_walls', 'ceiling_skirting_boards',
    'wallpaper'))


class PriceForRemodelingForm(ModelForm):
    class Meta:
        model = PriceForRemodeling
        fields = ('overhaul', 'remodeling', 'party_remodeling')


class PriceForWallsAndCeilingForm(ModelForm):
    class Meta:
        model = PriceForWallsAndCeiling
        fields = ('alignment', 'plaster', 'putty', 'undercoat', 'colorizing_ceil_and_walls', 'ceiling_skirting_boards',
                  'wallpaper')


class PriceForPriceForTilingForm(ModelForm):
    class Meta:
        model = PriceForTiling
        fields = (
            'surface_preparation', 'tailing', 'bathroom_fully', 'stacking_of_porcelain_tiles', 'stacking_of_maze',
            'grout')


class MasterCreationMultiForm(MultiModelForm):
    form_classes = OrderedDict((
        ('master', MasterForm),
        ('price_for_remodeling', PriceForRemodelingForm),
        ('price_for_walls_and_ceiling', PriceForWallsAndCeilingForm),
        ('price_for_tiling', PriceForPriceForTilingForm)
    ))


class CardOfObjectForMasterForm(ModelForm):
    image = FileField(
        label='Выберите файл',
        help_text='максимальный размер 42 MB',
        widget=FileInput(attrs={'class': 'upload'})
    )

    class Meta:
        model = CardOfObjectForMaster
        fields = ('description', 'location', 'budged_from', 'budged_to', 'image')


class PhotoForm(ModelForm):
    file = FileField(
        label='Выберите файл',
        help_text='максимальный размер 42 MB',
        widget=FileInput(attrs={'class': 'upload'})
    )

    class Meta:
        model = Photo
        fields = ('title', 'description', 'file',)
