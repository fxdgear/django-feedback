from django import forms

from feedback.models import Feedback, AnonymousFeedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        exclude = ('user', 'context', )


class AnonymousFeedbackForm(forms.ModelForm):
    class Meta:
        model = AnonymousFeedback
        exclude = ('user', 'context', )

    def __init__(self, *args, **kwargs):
        super(AnonymousFeedbackForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [
            'email',
            'type',
            'message',
        ]

