from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework.views import status

from money.models import Wallet, Transaction


class WalletAPIView(APITestCase):

    def setUp(self):
        self.get_url = reverse('money:get-wallets')
        self.create_url = reverse('money:create-wallet')
        Wallet.objects.create(name='Wallet Test')

    def test_get(self):
        wallet = Wallet.objects.first()
        self.assertEquals(Wallet.objects.count(), 1)
        response = self.client.get(self.get_url)
        response_json = response.json()
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response_json), 1)
        first_wallet_data = response_json[0]
        self.assertEquals(first_wallet_data['id'], wallet.id)
        self.assertEquals(first_wallet_data['name'], wallet.name)
        self.assertEquals(first_wallet_data['balance'], wallet.balance)
        self.assertEquals(first_wallet_data['slug'], wallet.slug)

    def test_get_zero_wallets(self):
        Wallet.objects.all().delete()
        response = self.client.get(self.get_url)
        response_json = response.json()
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response_json), 0)

    def test_create(self):
        self.assertEquals(Wallet.objects.count(), 1)
        data = {'name': 'Wallet Name'}
        response = self.client.post(self.create_url, data=data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Wallet.objects.count(), 2)
        wallet = Wallet.objects.last()
        self.assertEquals(wallet.name, data['name'])

    def test_create_not_unique(self):
        self.assertEquals(Wallet.objects.count(), 1)
        data = {'name': 'Wallet Test'}
        response = self.client.post(self.create_url, data=data, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(Wallet.objects.count(), 1)

    def test_update(self):
        self.assertEquals(Wallet.objects.count(), 1)
        data = {'name': 'Wallet Updated'}
        wallet = Wallet.objects.first()
        update_url = reverse('money:update-wallet', args=[wallet.slug])
        response = self.client.put(update_url, data=data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(Wallet.objects.count(), 1)
        wallet = Wallet.objects.first()
        self.assertEquals(wallet.name, 'Wallet Updated')

    def test_delete(self):
        self.assertEquals(Wallet.objects.count(), 1)
        wallet = Wallet.objects.first()
        update_url = reverse('money:delete-wallet', args=[wallet.slug])
        response = self.client.delete(update_url, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(Wallet.objects.count(), 0)


class TransactionAPIView(APITestCase):

    def setUp(self):
        self.get_url = reverse('money:get-transactions')
        self.create_url = reverse('money:create-transaction')
        wallet = Wallet.objects.create(name='Wallet Test', balance=100)
        Transaction.objects.create(
            wallet=wallet, transaction_type=Transaction.TYPE_INCOME,
            amount=100, comment='Hello!'
        )

    def test_get(self):
        self.assertEquals(Transaction.objects.count(), 1)
        transaction = Transaction.objects.first()
        response = self.client.get(self.get_url)
        response_json = response.json()
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response_json), 1)
        first_transaction_data = response_json[0]
        self.assertEquals(first_transaction_data['id'], transaction.id)
        self.assertEquals(
            first_transaction_data['transaction_type'],
            transaction.transaction_type
        )
        self.assertEquals(
            first_transaction_data['wallet'], transaction.wallet.pk
        )
        self.assertEquals(first_transaction_data['amount'], transaction.amount)
        self.assertEquals(
            first_transaction_data['comment'], transaction.comment
        )

    def test_get_by_wallet(self):
        self.assertEquals(Transaction.objects.count(), 1)
        wallet = Wallet.objects.first()
        transaction = Transaction.objects.get(wallet=wallet)
        get_by_wallet_url = reverse('money:get-transactions-by-wallet',
                                    args=[wallet.slug])
        response = self.client.get(self.get_url)
        response_json = response.json()
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response_json), 1)
        first_transaction_data = response_json[0]
        self.assertEquals(first_transaction_data['id'], transaction.id)
        self.assertEquals(
            first_transaction_data['transaction_type'],
            transaction.transaction_type
        )
        self.assertEquals(
            first_transaction_data['wallet'], transaction.wallet.pk
        )
        self.assertEquals(first_transaction_data['amount'], transaction.amount)
        self.assertEquals(
            first_transaction_data['comment'], transaction.comment
        )

    def test_get_zero_wallets(self):
        Transaction.objects.all().delete()
        response = self.client.get(self.get_url)
        response_json = response.json()
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response_json), 0)

    def test_create_income(self):
        self.assertEquals(Transaction.objects.count(), 1)
        wallet = Wallet.objects.first()
        wallet_balance_before = wallet.balance
        amount = 1000
        data = {
            'wallet': wallet.name,
            'transaction_type': Transaction.TYPE_INCOME,
            'amount': amount,
            'comment': 'Hi there!'
        }
        response = self.client.post(self.create_url, data=data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Transaction.objects.count(), 2)
        wallet = Wallet.objects.first()
        transaction = Transaction.objects.filter(wallet=wallet).last()
        self.assertEquals(
            data['transaction_type'], transaction.transaction_type
        )
        self.assertEquals(data['wallet'], transaction.wallet.name)
        self.assertEquals(data['amount'], transaction.amount)
        self.assertEquals(data['comment'], transaction.comment)
        self.assertEquals(
            wallet.balance, wallet_balance_before + transaction.amount
        )

    def test_create_outcome(self):
        self.assertEquals(Transaction.objects.count(), 1)
        wallet = Wallet.objects.first()
        wallet_balance_before = wallet.balance
        amount = 10
        data = {
            'wallet': wallet.name,
            'transaction_type': Transaction.TYPE_OUTCOME,
            'amount': amount,
            'comment': 'Hi there!'
        }
        response = self.client.post(self.create_url, data=data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Transaction.objects.count(), 2)
        wallet = Wallet.objects.first()
        transaction = Transaction.objects.filter(wallet=wallet).last()
        self.assertEquals(
            data['transaction_type'], transaction.transaction_type
        )
        self.assertEquals(data['wallet'], transaction.wallet.name)
        self.assertEquals(data['amount'], transaction.amount)
        self.assertEquals(data['comment'], transaction.comment)
        self.assertEquals(
            wallet.balance, wallet_balance_before - transaction.amount
        )

    def test_delete(self):
        self.assertEquals(Transaction.objects.count(), 1)
        transaction = Transaction.objects.first()
        delete_url = reverse(
            'money:delete-transactions', args=[str(transaction.pk)]
        )
        response = self.client.delete(delete_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(Transaction.objects.count(), 0)

    def test_delete_not_possible(self):
        wallet = Wallet.objects.create(name='Wallet P', balance=90)
        transaction = Transaction.objects.create(
            wallet=wallet, transaction_type=Transaction.TYPE_INCOME,
            amount=100, comment='Hello!'
        )
        delete_url = reverse(
            'money:delete-transactions', args=[str(transaction.pk)]
        )
        response = self.client.delete(delete_url)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
