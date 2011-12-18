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
