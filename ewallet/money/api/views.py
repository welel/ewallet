"""Module with API views."""
from django.db import transaction as transaction_decorators, utils
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from money.models import Wallet, Transaction
from money.api.serializers import (
    WalletGetSerializer,
    WalletCreateUpdateSerializer,
    TransactionGetSerializer,
    TransactionCreateUpdateSerializer,
)


class WalletView(APIView):
    """Views for operating ``Wallet`` model.

        * GET: list all wallets
        * POST: create a wallet
        * PUT: update a wallet
        * DELETE: delete a wallet

        Only `name` can be set for a wallet,
        `balance` and `slug` have default values.
        Operations Update/Delete require `slug` of a wallet
        as a function argument.
    """

    def get(self, request):
        wallets = Wallet.objects.all()
        serializer = WalletGetSerializer(wallets, many=True)
        return Response(serializer.data)

    def post(self, request):
        wallet = Wallet()
        serializer = WalletCreateUpdateSerializer(wallet, data=request.data)
        if serializer.is_valid():
            saved_instance = serializer.save()
            return Response(WalletCreateUpdateSerializer(saved_instance).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, slug: str):
        wallet = get_object_or_404(Wallet, slug=slug)
        serializer = WalletCreateUpdateSerializer(wallet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug: str):
        wallet = get_object_or_404(Wallet, slug=slug)
        operation = wallet.delete()
        if operation:
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    @api_view(['GET', ])
    def get_by_slug(request, slug:str):
        wallet = get_object_or_404(Wallet, slug=slug)
        serializer = WalletGetSerializer(wallet)
        return Response(serializer.data)


class TransactionView(APIView):
    """Views for operating ``Transaction`` model.

        * GET (get): list all transactions
        * GET (get_by_wallet): list all transaction of a specific wallet
        * POST: create a transaction
        * DELETE: delete a transaction (if it possible)

        Fields `wallet` and `transaction_type` are required,
        other fields have default values.
    """

    def get(self, request):
        transactions = Transaction.objects.all()
        serializer = TransactionGetSerializer(transactions, many=True)
        return Response(serializer.data)

    @staticmethod
    @api_view(['GET', ])
    def get_by_wallet(request, wallet_slug: str):
        if request.method == 'GET':
            wallet = get_object_or_404(Wallet, slug=wallet_slug)
            transactions = Transaction.objects.filter(wallet=wallet)
            serializer = TransactionGetSerializer(transactions, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @transaction_decorators.atomic
    def post(self, request):
        wallet = get_object_or_404(Wallet, slug=request.data['slug'])
        transaction = Transaction(wallet=wallet)
        serializer = TransactionCreateUpdateSerializer(transaction,
                                                       data=request.data)
        if serializer.is_valid():
            transaction = Transaction(**serializer.validated_data)
            transaction.wallet = wallet
            transaction, success = transaction.provide_transaction()
            if success:
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id: int):
        transaction = get_object_or_404(Transaction, id=id)
        try:
            transaction.delete()
        except utils.IntegrityError:
            data = {'details': 'The transaction cannot be deleted.'}
            return Response(status=status.HTTP_400_BAD_REQUEST, data=data)
        return Response(status=status.HTTP_200_OK)
