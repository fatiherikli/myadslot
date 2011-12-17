from django.conf import settings
from django.core.urlresolvers import reverse

def build_snippet(slot):
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
        <div>%(size)s</div>
        """ % {
            "size" : slot.sizes
        }
    return snippet

def escape_js(code):
    import re
    pattern = re.compile(re.escape("script"), re.IGNORECASING)
    _code = re.sub(pattern,"scr' + 'ipt", code)
    return _code.\
           replace("\n","\\n").\
           replace("\r","\\r")


def render_ads(slot):
    code = slot.get_ads_code()
    ads_template = """document.write('%(code)s');""" % {
        "code" : escape_js(code)
        }
    return ads_template





