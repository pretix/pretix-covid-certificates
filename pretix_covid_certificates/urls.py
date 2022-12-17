from django.urls import path

from pretix_covid_certificates.views import CovidCertificatesSettings

urlpatterns = [
    path(
        "control/event/<str:organizer>/<str:event>/covidcerts/",
        CovidCertificatesSettings.as_view(),
        name="settings",
    ),
]
