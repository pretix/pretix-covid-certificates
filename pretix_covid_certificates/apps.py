from django.utils.translation import gettext_lazy
from . import __version__

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 3.6 or above to run this plugin!")


class PluginApp(PluginConfig):
    default = True
    name = "pretix_covid_certificates"
    verbose_name = "Digital Covid Certificates"

    class PretixPluginMeta:
        name = gettext_lazy("Digital Covid Certificates")
        author = "Martin Gross"
        description = gettext_lazy(
            "This plugin allows to configure the validation of COVID test- and vaccination certificates using pretixSCAN for Android"
        )
        visible = True
        featured = True
        version = __version__
        category = "INTEGRATION"
        compatibility = "pretix>=3.6.0"

    def ready(self):
        from . import signals  # NOQA


