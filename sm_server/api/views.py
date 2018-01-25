import base64
import binascii
import uuid

from django.db import transaction, IntegrityError
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from account.models import Account, PreKey
from api.serializers import AccountSerializer


class AccountViewSet(viewsets.ViewSet):
    def create(self, request):
        try:
            identity_key = base64.b64decode(request.data['identity_key'])
            signed_pre_key = base64.b64decode(request.data['signed_pre_key'])
            account = Account(identity_key=identity_key, signed_pre_key=signed_pre_key)
            account.save()
            return Response(AccountSerializer(account).data)
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class PreKeyViewSet(viewsets.ViewSet):
    def create(self, request):
        try:
            account = Account.objects.get(id=uuid.UUID(request.data['account']))
            key_ids = request.data['key_ids']
            keys = list(map(base64.b64decode, request.data['keys']))
            if len(key_ids) != len(keys):
                raise ValidationError('Key count does not match')
            with transaction.atomic():
                for key_id, key in zip(key_ids, keys):
                    pre_key = PreKey.objects.filter(key_id=key_id)
                    if pre_key.exists():
                        pre_key.delete()
                    PreKey(account=account, key_id=key_id, key=key).save()
        except (ValueError, binascii.Error) as e:
            raise ValidationError('Invalid request: %s' % e)
        except Account.DoesNotExist:
            raise ValidationError('Account does not exist')
        except KeyError as e:
            raise ValidationError('%s is required' % e)
