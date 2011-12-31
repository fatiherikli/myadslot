from django.conf import settings
from django.core.urlresolvers import reverse

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
        json type casting for decimal, datetime etc..
    """
    import datetime, decimal
    if isinstance(item, decimal.Decimal):
        return int(item)
    if isinstance(item, datetime.datetime) or isinstance(item, datetime.date):
        return str(item)
    return item
