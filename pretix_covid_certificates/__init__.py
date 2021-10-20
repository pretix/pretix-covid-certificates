from django.utils.translation import gettext_lazy

try:
    from pretix.base.plugins import PluginConfig
except ImportError:
    raise RuntimeError("Please use pretix 4.2.0.dev1 or above to run this plugin!")

__version__ = "1.1.0"


class PluginApp(PluginConfig):
    name = "pretix_covid_certificates"
    verbose_name = "Digital Covid Certificates"

    class PretixPluginMeta:
        name = gettext_lazy("Digital Covid Certificates")
        author = "Martin Gross"
        description = gettext_lazy("This plugin allows to configure the validation of COVID test- and vaccination certificates using pretixSCAN for Android")
        visible = True
        version = __version__
        category = "INTEGRATION"
        compatibility = "pretix>=4.2.0.dev1"

    def ready(self):
        from . import signals  # NOQA

    def uninstalled(self, event):
        from pretix.base.models import Question
        # Upon deactivation of the plugin, we are removing all products associated with the
        # question. If we didn't do this, pretixSCAN will keep asking the question - possibly
        # with no way to answer it.
        #
        # Ideally, there should be only a single question per event that has the identifier
        # 'pretix_covid_certificates_question'. But better not assume anything that could be
        # screwed up though manual tampering.
        questions = Question.objects.filter(
            event=event,
            identifier='pretix_covid_certificates_question'
        )

        for question in questions:
            question.items.set([])


default_app_config = "pretix_covid_certificates.PluginApp"
