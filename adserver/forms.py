from django import forms
from adserver.models import Message
from core.forms import CustomForm
from myads.adserver.models import AdSlot, Advertisement
from django.utils.translation import ugettext_lazy as _

class AdSlotForm(forms.ModelForm, CustomForm):
    def clean_slot(self):
        slot = self.cleaned_data["slot"]
        check = AdSlot.objects.filter(slot=slot)
        if self.instance.pk:
            check = check.exclude(pk=self.instance.pk)
        if check.exists():
            raise forms.ValidationError(_("This slot already exists."))
        return slot

    class Meta:
        model = AdSlot
        exclude = ('user', )


class InformationForm(forms.ModelForm, CustomForm):
    class Meta:
        model = Message
        exclude = ('user', 'adslot', 'read', 'ip_address')

class AddAdvertisementForm(forms.ModelForm, CustomForm):
    class Meta:
        model = Advertisement
        exclude = ('user', 'adslot', 'start_date', 'end_date', 'view_count')


class EditAdvertisementForm(forms.ModelForm, CustomForm):

    class Meta:
        model = Advertisement
        exclude = ('user', 'adslot', 'view_count')

