from django.conf import settings
from django.contrib.auth.models import User

from rest_framework import serializers

from api.models import Person, Wallet


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'public_key']

class PersonSerializer(serializers.ModelSerializer):
    wallet = WalletSerializer()

    class Meta:
        model = Person
        fields = ['wallet']

class UserSerializer(serializers.ModelSerializer):
    person = PersonSerializer()

    class Meta:
        model = User
        fields = [
          'id',
          'username',
          'email',
          'first_name',
          'last_name',
          'person',
        ]

