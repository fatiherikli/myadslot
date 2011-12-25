from decimal import Decimal
import datetime
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils import simplejson

def build_snippet(slot):
    """
    type(slot) => myads.adserver.models.AdSlot
    """
    snippet = """
        <script type="text/javascript">
          (function() {
            /* %(slot_title)s */
            var protocol = ('https:' == document.location.protocol ? 'https://ssl' : 'http://')
            var adserver_js = protocol + '%(domain)s%(adserver_track_js)s';
            document.write('<scr' + 'ipt type="text/javascript" src="' + adserver_js + '"></scr' + 'ipt>');
          })();

        </script>
        """ % {
        "domain" : getattr(settings, 'ADSERVER_DOMAIN'),
        "adserver_track_js" : reverse("adserver_track_js", args=[slot.user.username, slot.slot]),
        "slot_title" : slot.title
    }
    return snippet

def build_blank_ads(slot):
    """
    type(slot) => myads.adserver.models.AdSlot
    """
    snippet = """
        <div style='width:%(width)spx; height:%(height)spx; text-align:center; background:whitesmoke; border:1px solid #dedede;'>
        <div style='font-size:40px; margin-top:%(margin_top)spx;'>%(ads_text)s</div>
        </div>
        """ % {
        "size" : slot.sizes,
        "width" : (slot.get_width or 100) - 2, # -2 for inline borders
        "height" : (slot.get_height or 100) - 2, # -2 for inline borders
        "margin_top" : (slot.get_height or 100) / 2 - 10, # for vertical align and -10px font-size
        "ads_text" : slot.sizes or "Ads"
    }
    return snippet

def escape_js(code):
    import re
    pattern = re.compile(re.escape("script"), re.IGNORECASE)
    _code = re.sub(pattern,"scr' + 'ipt", code)
    return _code.\
    replace("'","\\'").\
    replace("\n","\\n").\
    replace("\r","\\r")


def render_slot(slot):
    """
    type(slot) => myads.adserver.models.AdSlot
    """
    code = slot.get_ads_code()
    ads_template = """document.write('%(code)s');""" % {
        "code" : escape_js(code)
    }
    return ads_template


def jsonify(item):
    """
        type casting for decimal, datetime etc..
    """
    if isinstance(item, Decimal):
        return int(item)
    if isinstance(item, datetime.datetime):
        return str(item)
    return item


def build_statistic_data(sql):
    """
        return stringify json for charts...
    """
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute(sql)
    result = []
    for item in  cursor.fetchall():
        result.append(map(jsonify, list(item))) # make list from tuple and jsonify list
    return simplejson.dumps(result)


def advertisement_month_visits(advertisement_id):
    """
    result example:
        [["2011-12-18", 11, 2], ["2011-12-21", 2, 1], ["2011-12-25", 11, 1]]
    """
    return build_statistic_data("""
        SELECT
        Date(adserver_visitor.last_visit_date) AS date,
        Sum(adserver_visitor.visit_count) AS view_count,
        Count(adserver_visitor.visit_count) AS unique_visits
        FROM adserver_visitor
        WHERE advertisement_id = %s
        GROUP BY date;
        """ % advertisement_id)

def slot_month_visits(slot_id):
    """
    result example:
        [["2011-12-18", 11, 2], ["2011-12-21", 2, 1], ["2011-12-25", 11, 1]]
    """
    return build_statistic_data("""
        SELECT
        Date(adserver_visitor.last_visit_date) AS date,
        Sum(adserver_visitor.visit_count) AS view_count,
        Count(adserver_visitor.visit_count) AS unique_visits
        FROM adserver_visitor
        INNER JOIN  adserver_advertisement ON adserver_visitor.advertisement_id = adserver_advertisement.id
        WHERE adserver_advertisement.adslot_id = %s
        GROUP BY date;
        """ % slot_id)