from django.db.models.signals import post_save

from django.dispatch import receiver
from Accounts.models import Account
from .models import *

@receiver(post_save, sender=Account)
def create_fund(sender, instance, created,**kwargs):
	if created:
		Fund.objects.create(user=instance)


@receiver(post_save, sender=Account)
def save_fund(sender, instance, **kwargs):
	instance.fund.save()

@receiver(post_save, sender=Account)
def create_bank_info(sender, instance, created,**kwargs):
	if created:
		Bank_Info.objects.create(user=instance)


@receiver(post_save, sender=Account)
def save_fund(sender, instance, **kwargs):
	instance.bank_info.save()
