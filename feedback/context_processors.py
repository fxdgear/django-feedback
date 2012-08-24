from django.conf import settings

from feedback.forms import FeedbackForm, AnonymousFeedbackForm


def feedback_form(request):
    feedback_form = None
    if getattr(settings, 'ALLOW_ANONYMOUS_FEEDBACK', False):
        if request.user.is_authenticated():
            feedback_form = FeedbackForm()
        else:
            feedback_form = AnonymousFeedbackForm()
    elif request.user.is_authenticated():
        feedback_form = FeedbackForm()

    return {'feedback_form': feedback_form}

