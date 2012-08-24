from django.utils.translation import ugettext as _

from django.shortcuts import render_to_response
from django.template import RequestContext

from feedback.forms import FeedbackForm


def leave_feedback(
        request,
        template_name='feedback/feedback_form.html'):

    form = FeedbackForm(request.POST or None)
    if form.is_valid():
        feedback = form.save(commit=False)
        feedback.user = request.user
        feedback.context = ''
        feedback.save()
        url = request.POST.get('next', request.META.get('HTTP_REFERER', '/'))
        return render_to_response(template_name, {
            'message': _("Your feedback has been saved successfully.")
        }, context_instance=RequestContext(request))

    return render_to_response(
        template_name, {
            'feedback_form': form
        }, context_instance=RequestContext(request))

