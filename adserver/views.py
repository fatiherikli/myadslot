from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models.aggregates import Sum
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from myads.adserver.forms import AdSlotForm, AddAdvertisementForm, EditAdvertisementForm, InformationForm
from myads.adserver.models import Advertisement
from myads.adserver.stats import slot_month_visits, stats_browser, stats_slot_advertisements, slot_month_hours
from myads.core.decorators import render_template
from myads.core.views import JsonResponse
from myads.adserver.models import AdSlot
from myads.auth.decorators import login_required
from myads.adserver.utils import render_slot

def total_impression(request):
    impression = Advertisement.objects.aggregate(Sum("view_count"))["view_count__sum"]
    return JsonResponse(impression)

def track(request, username, slot):
    user = get_object_or_404(User, username=username)
    slot = get_object_or_404(AdSlot, user=user, slot=slot)
    ads = slot.get_active_ads()
    if ads and not 'preview_mode' in request.GET:
        ads.track_visitor(request)
    return HttpResponse(render_slot(slot))


@render_template
def information_message(request, username, slot, template="adserver/information_form.html"):
    user = get_object_or_404(User, username=username)
    slot = get_object_or_404(AdSlot, user=user, slot=slot)
    form = InformationForm()
    if request.method == "POST":
        form = InformationForm(request.POST)
        if form.is_valid():
            form.instance.user = user
            form.instance.adslot = slot
            form.instance.ip_address = request.META.get("REMOTE_ADDR")
            form.save()
    return template, {
        "form" : form,
        "is_popup" : True
    }


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
def preview_slot(request, slot, template="adserver/slot_preview.html"):
    slot = get_object_or_404(AdSlot, user=request.user, slot=slot)
    return template, {
        "slot" : slot
    }

@login_required
@render_template
def get_slot_snippet(request, slot, template="adserver/slot_get_snippet.html"):
    slot = get_object_or_404(AdSlot, user=request.user, slot=slot)
    return template, {
        "slot" : slot
    }


@login_required
@render_template
def add_advertisement(request, slot, template="adserver/advertisement_add.html"):
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
def advertisement_visitors(request, ads_id, template="adserver/advertisement_visitors.html"):
    advertisement = get_object_or_404(Advertisement, id=ads_id, adslot__user=request.user)
    visitors = advertisement.visitor_set.all()
    return template, {
        "advertisement" : advertisement,
        "last_visitors" : visitors
    }

@login_required
@render_template
def stats_slot(request, slot, template="adserver/slot_stats.html"):
    slot = get_object_or_404(AdSlot, user=request.user, slot=slot)
    return template, {
        "slot" : slot,
        "last_month_visits" :  slot_month_visits(slot.id),
        "last_month_hours" :  slot_month_hours(slot.id),
        "browser_stats" : stats_browser(slot.id),
        "slot_advertisements" : stats_slot_advertisements(slot.id),
    }

@login_required
@render_template
def edit_advertisement(request, ads_id, template="adserver/advertisement_edit.html"):    
    advertisement = get_object_or_404(Advertisement, id=ads_id, adslot__user=request.user)
    slot = advertisement.adslot
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
def delete_advertisement(request, ads_id):
    advertisement = get_object_or_404(Advertisement, id=ads_id, adslot__user=request.user)
    slot = advertisement.adslot
    advertisement.delete()
    return HttpResponseRedirect(slot.get_absolute_url())

@login_required
@render_template
def add_slot(request, template="adserver/slot_add.html"):
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
def edit_slot(request, slot, template="adserver/slot_edit.html"):
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
