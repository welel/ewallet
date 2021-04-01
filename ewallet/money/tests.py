from django.test import TestCase
from django.db import utils
from django.utils.text import slugify

from money.models import Wallet, Transaction


FIRST_WALLET_NAME = 'wallet1'
SECOND_WALLET_NAME = 'wallet2'

class WalletTestCase(TestCase):

    def setUp(self):
        Wallet.objects.create(name=FIRST_WALLET_NAME)
        Wallet.objects.create(name=SECOND_WALLET_NAME)

    def test_count(self):
        self.assertEquals(Wallet.objects.count(), 2)

    def test_default_name(self):
        wallet = Wallet.objects.create()
        self.assertNotEqual(wallet.name, '')

    def test_unique_name(self):
        with self.assertRaises(utils.IntegrityError):
            Wallet.objects.create(name=FIRST_WALLET_NAME)

    def test_default_balance(self):
        self.assertEquals(
            Wallet.objects.get(name=FIRST_WALLET_NAME).balance, 0
        )
        self.assertEquals(
            Wallet.objects.get(name=SECOND_WALLET_NAME).balance, 0
        )

    def test_slug(self):
        wallet1 = Wallet.objects.get(name=FIRST_WALLET_NAME)
        wallet2 = Wallet.objects.get(name=SECOND_WALLET_NAME)
        self.assertEquals(
            wallet1.slug, slugify(FIRST_WALLET_NAME, allow_unicode=True)
        )
        self.assertEquals(
            wallet2.slug, slugify(SECOND_WALLET_NAME, allow_unicode=True)
        )


class TransactionTestCase(TestCase):

    def setUp(self):
        Wallet.objects.create(name=FIRST_WALLET_NAME)
        Wallet.objects.create(name=SECOND_WALLET_NAME)
        first_wallet = Wallet.objects.get(name=FIRST_WALLET_NAME)
        second_wallet = Wallet.objects.get(name=SECOND_WALLET_NAME)
        Transaction.objects.create(
            wallet=first_wallet, transaction_type=Transaction.TYPE_INCOME,
            amount=100, comment='transaction1'
        )
        Transaction.objects.create(
            wallet=second_wallet, transaction_type=Transaction.TYPE_OUTCOME,
            amount=200, comment='transaction2'
        )

    def test_types(self):
        self.assertEquals(Transaction.TYPE_INCOME, 'income')
        self.assertEquals(Transaction.TYPE_OUTCOME, 'outcome')

    def test_type(self):
        transactoions = Transaction.objects.exclude(
            transaction_type=Transaction.TYPE_INCOME
        )
        self.assertEquals(transactoions.count(), 1)
        transactoions = transactoions.exclude(
            transaction_type=Transaction.TYPE_OUTCOME
        )
        self.assertEquals(transactoions.count(), 0)

    def test_default_amount(self):
        transaction = Transaction()
        self.assertEquals(transaction.amount, 0)

    def test_null_type(self):
        wallet = Wallet.objects.get(name=FIRST_WALLET_NAME)
        transaction = Transaction(wallet=wallet)
        with self.assertRaises(utils.IntegrityError):
            transaction.save()
