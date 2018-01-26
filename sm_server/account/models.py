import uuid
from django.db import models


class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    identity_key = models.BinaryField()
    signed_pre_key = models.BinaryField()


class PreKey(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    key_id = models.IntegerField()
    key = models.BinaryField()

    class Meta:
        unique_together = ('account', 'key_id')
