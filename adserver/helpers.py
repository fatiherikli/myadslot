from django.utils.translation import ugettext as _
import re

#see http://andreynikishaev.livejournal.com/78451.html
data_browser = [
    {
        'subString': "Chrome",
        'identity': "Chrome",
        'versionSearch': "Chrome/"
    },
        {
        'subString': "Apple",
        'identity': "Safari",
        'versionSearch': "Version/"
    },
        {   # For Netscape >= 9.0
            'subString': "Navigator",
            'identity': "Netscape",
            'versionSearch': "Navigator/"
    },
        {   # For Netscape 7.0-9.0
            'subString': "Netscape",
            'identity': "Netscape",
            'versionSearch': "Netscape/"
    },
        {   # For Netscape 6.x
            'subString': "Netscape6",
            'identity': "Netscape",
            'versionSearch': "Netscape6/"
    },
        {
        'subString': "Opera Mini",
        'identity': "Opera Mini",
        'versionSearch': "Opera Mini/"
    },
        {
        'subString': "Opera",
        'identity': "Opera",
        'versionSearch': "Version/"
    },
        {
        'subString': "Firefox",
        'identity': "Firefox",
        'versionSearch': "Firefox/"
    },
        {
        'subString': "MSIE",
        'identity': "Explorer",
        'versionSearch': "MSIE "
    },
        {
        'subString': "Konqueror",
        'identity': "Konqueror",
        'versionSearch': "Konqueror/"
    },
        {
        'subString': "SeaMonkey",
        'identity': "SeaMonkey",
        'versionSearch': "SeaMonkey/"
    },
        {
        'subString': "Gecko",
        'identity': "Mozilla",
        'versionSearch': "rv:"
    },
]

def detect_browser(user_agent):
    _browser = {}
    for b in data_browser:
        if b['subString'] in user_agent:
            _browser["name"] = b['identity']
            if b.has_key('versionSearch'):
                f = re.compile(b['versionSearch']+'([0-9\.]+)',re.M)
                m = f.search(user_agent)
                if m:
                    _browser["version"] = m.group(1)
            break

    if not _browser:
        return _("Unknown")
    #return "%s (%s)" % (_browser.get("name"), _browser.get("version"))
    return _browser.get("name")
