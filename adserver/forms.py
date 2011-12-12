from django import forms
from myads.adserver.models import AdSlot, Advertisement

class AdSlotForm(forms.ModelForm):
    class Meta:
        model = AdSlot
        exclude = ('user', )


class AddAdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        exclude = ('user', 'adslot', 'start_date', 'end_date', 'view_count')

class EditAdvertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        exclude = ('user', 'adslot')