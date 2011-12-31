from django.utils.translation import trans_real
from django.conf import settings
import gettext

def reset_translation_cache():
    if settings.USE_I18N:
        try:
            # Reset gettext.GNUTranslation cache.
            gettext._translations = {}

            # Reset Django by-language translation cache.
            trans_real._translations = {}

            # Delete Django current language translation cache.
            trans_real._default = None
        except AttributeError:
            pass