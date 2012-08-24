from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.mail import mail_admins
from django.template import Context
from django.template.loader import get_template

class BaseFeedback(models.Model):
    class Meta:
        abstract = True
        ordering = ['-time']

    type = models.CharField(choices=settings.FEEDBACK_CHOICES, max_length=100, verbose_name=_('Type'))
    message = models.TextField(verbose_name=_('Message'))
    time = models.DateTimeField(auto_now_add=True, verbose_name=_('Time'))
    context = models.TextField(verbose_name=_('Context'))

    def __unicode__(self):
        return self.message

    def get_absolute_url(self):
        return reverse('admin:view-feedback', args=[self.id])


class Feedback(BaseFeedback):
    user = models.ForeignKey(User, verbose_name=_('User'))


class AnonymousFeedback(BaseFeedback):
    user = models.ForeignKey(User, verbose_name=_('User'), null=True, blank=True, default=None)
    email = models.EmailField()


@receiver(post_save, sender=AnonymousFeedback)
@receiver(post_save, sender=Feedback)
def notify_admin_feedback(sender, instance, created, **kwargs):
    """Email admin whenever feedback is saved."""
    if created:
        c = Context({
            'message': instance.message,
            'from': instance.user,
            'email': getattr(instance, 'email', None)
            })
        t = get_template('feedback/feedback_message.txt')
        mail_admins(
            "Feedback",
            t.render(c),
            fail_silently=False,
            connection=None,
            html_message=None)



