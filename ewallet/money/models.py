import uuid
from django.db import models


class Wallet(models.Model):
	name = models.CharField(max_length=100, blank=True)
	balance = models.PositiveIntegerField(default=0)
	
	def save(self, *args, **kwargs):
		if self.name == '':
			self.name = 'Wallet {}'.format(uuid.uuid4())
		return super(Wallet, self).save(*args, **kwargs)


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
		max_length=10, choices=TYPE_CHOICES, editable=False
	)
	data = models.DateTimeField(auto_now_add=True, editable=False)
	amount = models.PositiveIntegerField(default=0, editable=False)
	comment = models.TextField(max_length=2500, blank=True)
