import calendar
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from adserver.helpers import detect_browser
from myads.adserver.utils import build_blank_ads
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

    @property
    def get_width(self):
        if not self.sizes:
            return None
        width, height = self.sizes.split("x")
        return int(width)

    @property
    def get_height(self):
        if not self.sizes:
            return None
        width, height = self.sizes.split("x")
        return int(height)


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
        help_text=_("The ad end date, if it is blank ads is infinite."))
    view_count = models.IntegerField(_("View Count"), help_text=_("Total ad impressions"), default=0)
    # view count denormalized by track_visitor method
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

    def get_state(self):
        return _('Published') if self.is_active else _('Not Published')

    def get_end_date(self):
        return self.end_date or _("Infinite")

    # stats
    def get_last_visitors(self):
        return self.visitor_set.all()[:30]

    def track_visitor(self, request):
        ip_address = request.META.get("REMOTE_ADDR")
        user_agent = request.META.get("HTTP_USER_AGENT")
        visitor, created = self.visitor_set.get_or_create(ip_address=ip_address, user_agent=user_agent)

        visitor.last_visit_url = request.META.get("HTTP_REFERER", "")
        visitor.last_visit_date = datetime.now()
        visitor.visit_count += 1
        visitor.save()

        # denormalize view count field
        self.view_count += 1
        self.save()

class VisitorManager(models.Manager):

    def active(self, timeout=settings.ADSERVER_ONLINE_TIMEOUT):
        now = datetime.now()
        tolerance = now - timedelta(minutes=timeout)
        return self.get_query_set().filter(last_visit_date__gte=tolerance)

    def last_month_visits(self):
        """
        return dict for charts...

        example:
            {
                "view_count" : [23,43,54],
                "unique_visits" : [23,43,54],
                "date" : ["12 dec","13 dec","13 dec"],
            }
        """
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("""
        SELECT
        Sum(adserver_visitor.visit_count) AS view_count,
        Count(adserver_visitor.visit_count) AS unique_visits,
        Date(adserver_visitor.last_visit_date) AS date
        FROM adserver_visitor
        GROUP BY date;
        """)

        result_dict = {
            "view_count" : [],
            "unique_visits" : [],
            "date" : []
        }
        for view_count, unique_visits, date in  cursor.fetchall():
            result_dict["date"].append(date)
            result_dict["unique_visits"].append(unique_visits)
            result_dict["view_count"].append(view_count)
        return result_dict


class Visitor(models.Model):
    advertisement = models.ForeignKey(Advertisement)
    ip_address = models.IPAddressField(_("IP Address"))
    user_agent = models.CharField(_("Visitor Informations"), max_length=255)
    visit_count = models.IntegerField(_("View Count"), default=1)
    last_visit_url = models.CharField(_("Visited Page Url"), max_length=255)
    last_visit_date = models.DateTimeField(_("Last Visit Date"), auto_now_add=True, auto_now=True)

    objects = VisitorManager()

    class Meta:
        ordering = ["-last_visit_date",]

    def save(self, **kwargs):
        super(Visitor, self).save(**kwargs)

    def __unicode__(self):
        return self.ip_address

    def get_user_agent(self):
        browser = detect_browser(self.user_agent)
        if not browser:
            return _("Unknown")
        return "%s (%s)" % (browser.get("name"), browser.get("version"))
    get_user_agent.short_description = _("Visitor Informations")