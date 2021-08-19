from django.dispatch import receiver
from django.urls import resolve, reverse
from django.utils.translation import gettext_lazy as _, gettext_noop  # NoQA
from django_scopes import scopes_disabled
from pretix.base.models import Event
from pretix.base.settings import settings_hierarkey
from pretix.base.signals import api_event_settings_fields, periodic_task
from pretix.control.signals import nav_event_settings
from pretix.helpers.periodic import minimum_interval
from rest_framework import serializers

from pretix_covid_certificates.tasks import expire_certificate_answers


@receiver(nav_event_settings, dispatch_uid='pretix_covid_certificates_nav_event_settings')
def nav_event_settings(sender, request, **kwargs):
    url = resolve(request.path_info)
    if not request.user.has_event_permission(request.organizer, request.event, 'can_change_event_settings',
                                             request=request):
        return []
    return [{
        'label': _('COVID Certificate Validation'),
        'url': reverse('plugins:pretix_covid_certificates:settings', kwargs={
            'event': request.event.slug,
            'organizer': request.organizer.slug,
        }),
        'active': url.namespace == 'plugins:pretix_covid_certificates',
    }]


@receiver(periodic_task, dispatch_uid='pretix_covid_certificates_periodic_task')
@scopes_disabled()
@minimum_interval(minutes_after_success=60 * 24)
def periodic_task(sender, **kwargs):
    Event_SettingsStore = get_model('pretixbase', 'Event_SettingsStore') # NoQA
    events = list(Event.objects.filter(
        id__in=Event_SettingsStore.objects.filter(key='covid_certificates_recheck_every_24h', value=True).values_list('object_id', flat=True),
        plugins__contains='pretix_covid_certificates',
    ).values_list('pk', flat=True))

    for eventpk in events:
        expire_certificate_answers.apply(args=(eventpk,))


@receiver(api_event_settings_fields, dispatch_uid="pretix_covid_certificates_api_event_settings_fields")
def api_event_settings_fields(sender, **kwargs):
    return {
        'covid_certificates_allow_vaccinated': serializers.BooleanField(required=False),
        'covid_certificates_allow_vaccinated_min': serializers.IntegerField(required=False),
        'covid_certificates_allow_vaccinated_max': serializers.IntegerField(required=False),
        'covid_certificates_record_proof_vaccinated': serializers.BooleanField(required=False),
        'covid_certificates_allow_cured': serializers.BooleanField(required=False),
        'covid_certificates_allow_cured_min': serializers.IntegerField(required=False),
        'covid_certificates_allow_cured_max': serializers.IntegerField(required=False),
        'covid_certificates_record_proof_cured': serializers.BooleanField(required=False),
        'covid_certificates_allow_tested_pcr': serializers.BooleanField(required=False),
        'covid_certificates_allow_tested_pcr_min': serializers.IntegerField(required=False),
        'covid_certificates_allow_tested_pcr_max': serializers.IntegerField(required=False),
        'covid_certificates_record_proof_tested_pcr': serializers.BooleanField(required=False),
        'covid_certificates_allow_tested_antigen_unknown': serializers.BooleanField(required=False),
        'covid_certificates_allow_tested_antigen_unknown_min': serializers.IntegerField(required=False),
        'covid_certificates_allow_tested_antigen_unknown_max': serializers.IntegerField(required=False),
        'covid_certificates_record_proof_tested_antigen_unknown': serializers.BooleanField(required=False),
        'covid_certificates_accept_eudgc': serializers.BooleanField(required=False),
        'covid_certificates_accept_manual': serializers.BooleanField(required=False),
    }


# Rulenumbers correspond to the covpass-sdk rules and their libpretixui counterparts
settings_hierarkey.add_default('covid_certificates_allow_vaccinated', False, bool)
settings_hierarkey.add_default('covid_certificates_allow_vaccinated_min', 14, int)  # VR_DE_003 / VR_003
settings_hierarkey.add_default('covid_certificates_allow_vaccinated_max', 365, int)  # VR_DE_004 / VR_004
settings_hierarkey.add_default('covid_certificates_record_proof_vaccinated', False, bool)
settings_hierarkey.add_default('covid_certificates_allow_cured', False, bool)
settings_hierarkey.add_default('covid_certificates_allow_cured_min', 27, int)  # RR_DE_001 / RR_001
settings_hierarkey.add_default('covid_certificates_allow_cured_max', 180, int)  # RR_DE_002 / RR_01
settings_hierarkey.add_default('covid_certificates_record_proof_cured', False, bool)
settings_hierarkey.add_default('covid_certificates_allow_tested_pcr', False, bool)
settings_hierarkey.add_default('covid_certificates_allow_tested_pcr_min', 0, int)  # n/a / TR_002
settings_hierarkey.add_default('covid_certificates_allow_tested_pcr_max', 72, int)  # TR_DE_003 / TR_003
settings_hierarkey.add_default('covid_certificates_record_proof_tested_pcr', False, bool)
settings_hierarkey.add_default('covid_certificates_allow_tested_antigen_unknown', False, bool)
settings_hierarkey.add_default('covid_certificates_allow_tested_antigen_unknown_min', 0, int)  # n/a / TR_002
settings_hierarkey.add_default('covid_certificates_allow_tested_antigen_unknown_max', 48, int)  # TR_DE_002 / TR_003
settings_hierarkey.add_default('covid_certificates_record_proof_tested_antigen_unknown', False, bool)
settings_hierarkey.add_default('covid_certificates_accept_eudgc', True, bool)
settings_hierarkey.add_default('covid_certificates_accept_manual', True, bool)
settings_hierarkey.add_default('covid_certificates_recheck_every_24h', False, bool)
