from django import forms
from core.forms import CustomForm
from myads.adserver.models import AdSlot, Advertisement
from django.utils.translation import ugettext_lazy as _

class AdSlotForm(forms.ModelForm, CustomForm):
    def clean_slot(self):
        slot = self.cleaned_data["slot"]
        try:
            AdSlot.objects.get(slot=slot)
        except AdSlot.DoesNotExist:
            return slot
        raise forms.ValidationError(_("This slot already exists."))

    class Meta:
        model = AdSlot
        exclude = ('user', )


class AddAdvertisementForm(forms.ModelForm, CustomForm):
    class Meta:
        model = Advertisement
        exclude = ('user', 'adslot', 'start_date', 'end_date', 'view_count')


class EditAdvertisementForm(forms.ModelForm, CustomForm):

    class Meta:
        model = Advertisement
        exclude = ('user', 'adslot', 'view_count')

