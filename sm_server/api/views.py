import base64

from rest_framework import status, viewsets
from rest_framework.response import Response

from account.models import Account
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
