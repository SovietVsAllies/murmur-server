import base64
import binascii
import uuid

from django.db import transaction
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from account.models import Account, PreKey
from api.serializers import AccountSerializer, PreKeySerializer


def validate_account(pk):
    try:
        return Account.objects.get(id=uuid.UUID(bytes=base64.b64decode(pk + '==')))
    except (binascii.Error, ValueError):
        raise ValidationError({'code': -100, 'message': 'Invalid account id'})
    except Account.DoesNotExist:
        raise ValidationError({'code': -101, 'message': 'Account does not exist'})


class AccountViewSet(viewsets.ViewSet):
    def create(self, request):
        try:
            identity_key = base64.b64decode(request.data['identity_key'] + '==')
            signed_pre_key = base64.b64decode(request.data['signed_pre_key'] + '==')
            account = Account(identity_key=identity_key, signed_pre_key=signed_pre_key)
            account.save()
            return Response(AccountSerializer(account).data)
        except KeyError as e:
            raise ValidationError({'code': -100, 'message': '%s is required' % e})

    def retrieve(self, request, pk):
        try:
            account = validate_account(pk)
            return Response(AccountSerializer(account).data)
        except KeyError as e:
            raise ValidationError({'code': -100, 'message': '%s is required' % e})


class PreKeyViewSet(viewsets.ViewSet):
    def create(self, request):
        try:
            account = validate_account(request.data['account'])
            key_ids = request.data['key_ids']
            keys = list(map(lambda k: base64.b64decode(k + '=='), request.data['keys']))
            if len(key_ids) != len(keys):
                raise ValidationError('Key count does not match')
            with transaction.atomic():
                for key_id, key in zip(key_ids, keys):
                    pre_key = PreKey.objects.filter(key_id=key_id)
                    if pre_key.exists():
                        pre_key.delete()
                    PreKey(account=account, key_id=key_id, key=key).save()
            return Response({'code': 0})
        except (ValueError, binascii.Error) as e:
            raise ValidationError({'code': -100, 'message': 'Invalid request: %s' % e})
        except KeyError as e:
            raise ValidationError({'code': -100, 'message': '%s is required' % e})

    def retrieve(self, request, pk):
        try:
            account = validate_account(pk)
            pre_key = PreKey.objects.filter(account=account).order_by('key_id')[0]
            response = Response(PreKeySerializer(pre_key).data)
            pre_key.delete()
            return response
        except PreKey.DoesNotExist:
            return Response({'code': -102, 'message': 'No pre keys for this account'})
