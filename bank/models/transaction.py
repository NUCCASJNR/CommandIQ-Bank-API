#!/usr/bin/env python3

"""Contains Transaction model"""

from bank.models.account import Account, models, BaseModel


class Transaction(BaseModel):
    """
    Transaction class that inherits from basemodel
    """

    account_id = models.ForeignKey(Account, on_delete=models.CASCADE, db_column='account_id')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=[('deposit', 'Deposit'), ('withdrawal', 'Withdrawal'),
                                                                ('transfer', 'Transfer')])
