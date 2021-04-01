from rest_framework import serializers

from money.models import Wallet, Transaction


class WalletGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'name', 'slug', 'balance']


class WalletCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['name']


class TransactionGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'wallet', 'transaction_type', 'data',
                  'amount', 'comment']


class TransactionCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['wallet', 'transaction_type', 'amount', 'comment']
