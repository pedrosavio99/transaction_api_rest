from django.db import models
from django.contrib.auth.models import User


class UserPayer(models.Model):
    document = models.CharField(max_length=14)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Auth_token(models.Model):
    user_payer = models.ForeignKey(UserPayer, on_delete=models.CASCADE)
    token = models.UUIDField(primary_key=True)

    def __str__(self):
        return str(self.token)


class Wallet(models.Model):
    user_payer = models.ForeignKey(UserPayer, on_delete=models.CASCADE)
    balance = models.CharField(max_length=9, default='9000000')

    def __str__(self):
        return self.balance


class Account(models.Model):
    account_number = models.CharField(max_length=14)
    bank = models.IntegerField()
    branch = models.IntegerField()

    def __str__(self):
        return str(self.account_number)


class Status(models.IntegerChoices):
    PENDING = 1, "PENDING"
    FINISHED = 2, "FINISHED"
    REJECTED = 3, "REJECTED"


class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    user_payer = models.ForeignKey(UserPayer, on_delete=models.CASCADE)
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.PositiveSmallIntegerField(choices=Status.choices,default=Status.PENDING)

    def __str__(self):
        return str(self.transaction_id)
