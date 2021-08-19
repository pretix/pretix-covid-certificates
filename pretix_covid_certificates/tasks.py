from django_scopes import scopes_disabled
from pretix.base.models import Event, QuestionAnswer
from pretix.celery_app import app


@app.task
@scopes_disabled()
def expire_certificate_answers(event):
    event = Event.objects.get(pk=event)
    QuestionAnswer.objects.filter(
        question__event=event,
        question__identifier='pretix_covid_certificates_question',
    ).delete()
    return event.organizer.slug, event.slug
