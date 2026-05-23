from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import TutorProfile


@receiver(pre_save, sender=TutorProfile)
def tutor_verification_approved(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old = TutorProfile.objects.get(pk=instance.pk)
    except TutorProfile.DoesNotExist:
        return
    if (
        old.verification_status != TutorProfile.VerificationStatus.APPROVED
        and instance.verification_status == TutorProfile.VerificationStatus.APPROVED
    ):
        from notifications.services import NotificationService
        NotificationService.notify_verification_approved(instance)
