from django.db import models

from account.models import Account


class PendingMessage(models.Model):
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE)
    payload = models.BinaryField()


class ActiveChannel(models.Model):
    owner = models.OneToOneField(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
