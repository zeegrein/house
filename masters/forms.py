from collections import OrderedDict

from django.contrib.auth import get_user_model
from django.forms import ModelForm, DateField, SelectDateWidget, Textarea
from django.forms.models import inlineformset_factory
from betterforms.multiform import MultiModelForm
from masters.models import Master, PriceForWallsAndCeiling, PriceForRemodeling, PriceForTiling


class MasterForm(ModelForm):
    # experience = DateField(widget=SelectDateWidget(years=range(1980, 2017), ))
    class Meta:
        model = Master
        widgets = {
            'additional_info': Textarea(attrs={'cols': 40, 'rows': 5}),
        }
        fields = (
            'group', 'first_name', 'second_name', 'middle_name', 'country', 'city', 'phone_number', 'email',
            'experience',
            'additional_info')


PriceForRemodelingFormSet = inlineformset_factory(Master, PriceForRemodeling, extra=0, fields='__all__')
PriceForWallsAndCeilingFormSet = inlineformset_factory(Master, PriceForWallsAndCeiling, extra=0, fields='__all__')


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


class MasterEditMultiForm(MultiModelForm):
    form_classes = {
        'master': MasterForm,
        'price_for_remodeling': PriceForRemodelingForm,
        'price_for_walls_and_ceiling': PriceForWallsAndCeilingForm,
    }
