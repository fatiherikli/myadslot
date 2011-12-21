from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from adserver.forms import AdSlotForm, AddAdvertisementForm, EditAdvertisementForm
from adserver.models import Advertisement
from core.decorators import render_template
from myads.adserver.models import AdSlot
from myads.auth.decorators import login_required
from myads.adserver.utils import render_slot
from django.core.urlresolvers import reverse

def track(request, username, slot):
    user = get_object_or_404(User, username=username)
    slot = get_object_or_404(AdSlot, user=user, slot=slot)
    ads = slot.get_active_ads()
    if ads and not 'preview_mode' in request.GET:
        ads.track_visitor(request)
    return HttpResponse(render_slot(slot))


@login_required
@render_template
def dashboard(request, template="adserver/dashboard.html"):
    slots = AdSlot.objects.from_request(request)
    return template, {
        "slots" : slots
    }

@login_required
@render_template
def advertisements(request, slot, template="adserver/advertisements.html"):
    slot = get_object_or_404(AdSlot, user=request.user, slot=slot)
    return template, {
        "slot" : slot
    }

@login_required
def delete_slot(request, slot):
    slot = get_object_or_404(AdSlot, user=request.user, slot=slot)
    slot.delete()
    return HttpResponseRedirect(reverse('dashboard'))


@login_required
@render_template
def preview_slot(request, slot, template="adserver/preview_slot.html"):
    slot = get_object_or_404(AdSlot, user=request.user, slot=slot)
    return template, {
        "slot" : slot
    }

@login_required
@render_template
def get_slot_snippet(request, slot, template="adserver/get_slot_snippet.html"):
    slot = get_object_or_404(AdSlot, user=request.user, slot=slot)
    return template, {
        "slot" : slot
    }


@login_required
@render_template
def add_advertisement(request, slot, template="adserver/add_advertisement.html"):
    slot = get_object_or_404(AdSlot, user=request.user, slot=slot)
    form = AddAdvertisementForm()
    if request.method == "POST":
        form = AddAdvertisementForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.adslot = slot
            form.save()
            return HttpResponseRedirect(reverse("adserver_ads", args=[slot.slot]))

    return template, {
        "slot" : slot,
        "form" : form
    }


@login_required
@render_template
def stats_advertisement(request, slot, ads_id, template="adserver/stats_advertisement.html"):
    slot = get_object_or_404(AdSlot, user=request.user, slot=slot)
    advertisement = get_object_or_404(Advertisement, id=ads_id, adslot=slot)
    return template, {
        "advertisement" : advertisement
    }

@login_required
@render_template
def edit_advertisement(request, slot, ads_id, template="adserver/edit_advertisement.html"):
    slot = get_object_or_404(AdSlot, user=request.user, slot=slot)
    advertisement = get_object_or_404(Advertisement, id=ads_id, adslot=slot)
    form = EditAdvertisementForm(instance=advertisement)
    if request.method == "POST":
        form = EditAdvertisementForm(request.POST, instance=advertisement)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.adslot = slot
            form.save()
            return HttpResponseRedirect(reverse("adserver_ads", args=[slot.slot]))

    return template, {
        "slot" : slot,
        "form" : form
    }


@login_required
@render_template
def add_slot(request, template="adserver/add_slot.html"):
    form = AdSlotForm()
    if request.method == "POST":
        form = AdSlotForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()

    return template, {
        "form" : form
    }


@login_required
@render_template
def edit_slot(request, slot, template="adserver/edit_slot.html"):
    slot = get_object_or_404(AdSlot, user=request.user, slot=slot)
    form = AdSlotForm(instance=slot)
    if request.method == "POST":
        form = AdSlotForm(request.POST, instance=slot)
        if form.is_valid():
            form.instance.user = request.user
            form.save()

    return template, {
        "form" : form
    }

