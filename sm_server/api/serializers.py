import base64
import binascii

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from account.models import Account, PreKey


class BinaryField(serializers.Field):
    def to_representation(self, value):
        return base64.b64encode(value)

    def to_internal_value(self, data):
        try:
            return base64.b64decode(data, validate=True)
        except binascii.Error:
            raise ValidationError('Invalid base64 string: %s' % data)


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'identity_key', 'signed_pre_key')


class PreKeySerializer(serializers.ModelSerializer):
    key = BinaryField()

    class Meta:
        model = PreKey
        fields = ('account', 'key_id', 'key')
