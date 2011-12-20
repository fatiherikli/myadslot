import re
from django.utils.cache import patch_vary_headers
from django.utils import translation

# see http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_DOMAIN_PREFIX = {
    "tr" : "TR_tr",
    "en" : "EN_us"
}

class LocaleMiddleware(object):
    """
    This is a very simple middleware that parses a request
    and decides what translation object to install in the current
    thread context. This allows pages to be dynamically
    translated to the language the user desires (if the language
    is available, of course).
    """

    def process_request(self, request):
        domain_prefix = request.META.get("HTTP_HOST","").split(".")[0]
        if domain_prefix in LANGUAGE_DOMAIN_PREFIX:
            translation.activate(LANGUAGE_DOMAIN_PREFIX[domain_prefix])
            request.LANGUAGE_CODE = LANGUAGE_DOMAIN_PREFIX[domain_prefix]
        else:
            translation.activate(LANGUAGE_DOMAIN_PREFIX["en"])
            request.LANGUAGE_CODE = LANGUAGE_DOMAIN_PREFIX["en"]
#            translation.activate(translation.get_language_from_request(request))
#            request.LANGUAGE_CODE = LANGUAGE_DOMAIN_PREFIX[translation.get_language_from_request(request)]

    def process_response(self, request, response):
        patch_vary_headers(response, ('Accept-Language',))
        if 'Content-Language' not in response:
            response['Content-Language'] = translation.get_language()
        translation.deactivate()
        return response

class MobileDomainMiddleware(object):
    def process_request(self, request):
        if 'mobile.' in request.META["HTTP_HOST"] or 'm.' in request.META["HTTP_HOST"]:
            request.is_mobile = True


#see http://djangosnippets.org/snippets/2001/
class MobileDetectionMiddleware(object):
    """
    Useful middleware to detect if the user is
    on a mobile device.
    """

    def process_request(self, request):
        if getattr(request, "is_mobile", False):
            return

        is_mobile = False;

        if request.META.has_key('HTTP_USER_AGENT'):
            user_agent = request.META['HTTP_USER_AGENT']

            # Test common mobile values.
            pattern = "(up.browser|up.link|mmp|symbian|smartphone|midp|wap|phone|windows ce|pda|mobile|mini|palm|netfront)"
            prog = re.compile(pattern, re.IGNORECASE)
            match = prog.search(user_agent)

            if match:
                is_mobile = True;
            else:
                # Nokia like test for WAP browsers.
                # http://www.developershome.com/wap/xhtmlmp/xhtml_mp_tutorial.asp?page=mimeTypesFileExtension

                if request.META.has_key('HTTP_ACCEPT'):
                    http_accept = request.META['HTTP_ACCEPT']

                    pattern = "application/vnd\.wap\.xhtml\+xml"
                    prog = re.compile(pattern, re.IGNORECASE)

                    match = prog.search(http_accept)

                    if match:
                        is_mobile = True

            if not is_mobile:
                # Now we test the user_agent from a big list.
                user_agents_test = ("w3c ", "acs-", "alav", "alca", "amoi", "audi",
                                    "avan", "benq", "bird", "blac", "blaz", "brew",
                                    "cell", "cldc", "cmd-", "dang", "doco", "eric",
                                    "hipt", "inno", "ipaq", "java", "jigs", "kddi",
                                    "keji", "leno", "lg-c", "lg-d", "lg-g", "lge-",
                                    "maui", "maxo", "midp", "mits", "mmef", "mobi",
                                    "mot-", "moto", "mwbp", "nec-", "newt", "noki",
                                    "xda",  "palm", "pana", "pant", "phil", "play",
                                    "port", "prox", "qwap", "sage", "sams", "sany",
                                    "sch-", "sec-", "send", "seri", "sgh-", "shar",
                                    "sie-", "siem", "smal", "smar", "sony", "sph-",
                                    "symb", "t-mo", "teli", "tim-", "tosh", "tsm-",
                                    "upg1", "upsi", "vk-v", "voda", "wap-", "wapa",
                                    "wapi", "wapp", "wapr", "webc", "winw", "winw",
                                    "xda-",)

                test = user_agent[0:4].lower()
                if test in user_agents_test:
                    is_mobile = True

        request.is_mobile = is_mobile