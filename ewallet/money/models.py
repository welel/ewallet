import uuid

from django.db import models, utils
from django.utils.text import slugify


class Wallet(models.Model):
    name = models.CharField(max_length=100, blank=True, unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    balance = models.PositiveIntegerField(default=0, editable=False)

    def save(self, *args, **kwargs):
        if self.name == '':
            self.name = 'Wallet {}'.format(uuid.uuid4())

        slug = slugify(self.name, allow_unicode=True)
        if not self.slug or self.slug != slug:
            self.slug = slug
        return super().save(*args, **kwargs)


class Transaction(models.Model):
    TYPE_INCOME = 'income'
    TYPE_OUTCOME = 'outcome'
    TYPE_CHOICES = (
        (TYPE_INCOME, 'Deposit'),
        (TYPE_OUTCOME, 'Withdrawal'),
    )
    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE, editable=False
    )
    transaction_type = models.CharField(
        max_length=10, choices=TYPE_CHOICES, blank=False, default=None
    )
    data = models.DateTimeField(auto_now_add=True, editable=False)
    amount = models.PositiveIntegerField(default=0)
    comment = models.TextField(max_length=2500, blank=True)

    def provide_transaction(self) -> ('Transaction', bool):
        """Changes a wallet `balance` considering transactions `amount`."""
        if not (self.wallet or self.transaction_type or self.amount):
            return self, False
        if self.transaction_type == self.TYPE_INCOME:
            self.wallet.balance += self.amount
            self.wallet.save(update_fields=['balance'])
        elif self.transaction_type == self.TYPE_OUTCOME \
                and self.wallet.balance >= self.amount:
            self.wallet.balance -= self.amount
            self.wallet.save(update_fields=['balance'])
        else:
            return self, False
        return self, True

    def is_deletion_possible(self) -> bool:
        """Checks possibility of rollback of the transaction."""
        if not (self.wallet or self.transaction_type or self.amount):
            return False
        if self.transaction_type == self.TYPE_INCOME:
            return self.wallet.balance >= self.amount
        return True

    def delete(self, *args, **kwargs):
        if self.is_deletion_possible():
            self.wallet.balance -= self.amount
            self.wallet.save(update_fields=['balance'])
        else:
            raise utils.IntegrityError
        return super().delete(*args, **kwargs)
