import base64
import uuid

from rest_framework import status, viewsets, mixins
from rest_framework.response import Response

from account.models import Account, PreKey
from api.serializers import AccountSerializer, PreKeySerializer


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


class PreKeyViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = PreKey.objects.all()
    serializer_class = PreKeySerializer
