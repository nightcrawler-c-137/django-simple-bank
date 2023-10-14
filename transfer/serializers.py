from rest_framework import serializers

from .models import Transfer
from customer.serializers import CustomerSerializer


class TransferSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    class Meta:
        model = Transfer
        fields = ('amount', 'transfer_type', 'customer')


class TransferHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ('amount', 'transfer_type', 'created_time')