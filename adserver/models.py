from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.db import models
from django.core.urlresolvers import reverse
from adserver.utils import build_blank_ads
from myads.adserver.utils import build_snippet

ADSLOT_SIZE_CHOICES = (
    ('300x250','300x250 Medium Rectangle'),
    ('250x250','250x250 Square Pop-Up'),
    ('240x400','240x400 Vertical Rectangle'),
    ('336x280','336x280 Large Rectangle'),
    ('180x150','180x150 Rectangle'),
    ('300x100','300x100 3:1 Rectangle'),
    ('720x300','720x300 Pop-Under'),
    ('468x60','468x60 Full banner'),
    ('234x60','234x60 Half banner'),
    ('88x31','88x31 Micro bar'),
    ('120x90','120x90 Button 1'),
    ('120x60','120x60 Button 2'),
    ('120x240','120x240 Vertical banner'),
    ('125x125','125x125 Square button'),
    ('728x90','728x90 Leaderboard'),
    ('160x600','160x600 Wide skyscraper'),
    ('120x600','120x600 Skyscraper'),
    ('300x600','300x600 Half page ad'),
)

class AdSlotManager(models.Manager):
    def from_request(self, request):
        qs = self.get_query_set()
        if request.user.is_anonymous():
            return qs.none()
        return qs.filter(user=request.user)

class AdSlot(models.Model):
    user = models.ForeignKey(User, verbose_name=_("User"))
    title = models.CharField(_("Title"), max_length=100, help_text=_("For example My Banners"))
    slot = models.SlugField(_("Slot"), max_length=100, help_text=_("For example my-banners, top-banner"))
    sizes = models.CharField(_("Sizes"), max_length=25, choices=ADSLOT_SIZE_CHOICES, blank=True, null=True,
                                help_text=_("This field is optional"))

    objects = AdSlotManager()

    class Meta:
        unique_together = ("user", "slot")

    def get_absolute_url(self):
        return reverse('adserver_ads', args=[self.slot, ])

    def get_active_ads(self):
        now = datetime.now()
        queryset = self.advertisement_set.active()
        if queryset:
            return queryset[0]
        return None

    def get_ads_code(self):
        ads = self.get_active_ads()
        if ads:
            return ads.code
        return build_blank_ads(self)

    def get_snippet(self):
        return build_snippet(self)

    def __unicode__(self):
        return self.title


class AdvertisementManager(models.Manager):
    def active(self):
        now = datetime.now()
        return self.get_query_set().filter(start_date__lte=now, is_active=True).order_by("?") # random



class Advertisement(models.Model):
    user = models.ForeignKey(User, verbose_name=_("User"))
    adslot = models.ForeignKey(AdSlot, verbose_name=_("Ad Slot"))
    title = models.CharField(_("Title"), max_length=100, help_text=_("For example My Adfoo Ads"))
    is_active = models.BooleanField(_("Active"), default=True, help_text=_("Is active or inactive"))
    start_date = models.DateTimeField(_("Start Date"), blank=True, null=True,  help_text=_("The ad start date"))
    end_date = models.DateTimeField(_("Finish Date"), blank=True, null=True,
        help_text=_("The ad start date, if it is blank ads is infinite."))
    view_count = models.IntegerField(_("View Count"), help_text=_("Total ad impressions"), default=0)
    code = models.TextField(_("Ads Code"), help_text="Advertising code here...")

    objects = AdvertisementManager()


    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:
            self.start_date = datetime.today()
        super(Advertisement, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('adserver_edit_advertisement', args=[self.adslot.slot, self.id])

    def get_start_date(self):
        return self.start_date

    def get_end_date(self):
        return self.end_date or _("Infinite")

class VisitorManager(models.Manager):
    def active(self, timeout=10):
        now = datetime.now()
        tolerance = now - timedelta(minutes=timeout)
        return self.get_query_set().filter(last_visit_date__gte=tolerance)

class Visitor(models.Model):
    ip_address = models.IPAddressField(_("IP Address"))
    user_agent = models.CharField(_("Visitor Informations"), max_length=255)
    visit_count = models.IntegerField(_("View Count"), default=1)
    last_visit_url = models.CharField(_("Visited Page Url"), max_length=255)
    last_visit_date = models.DateTimeField(_("Last Visit Date"), auto_now_add=True, auto_now=True)

    objects = VisitorManager()

    def __unicode__(self):
        return self.ip_address
