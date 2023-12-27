#!/usr/bin/env python3

"""Contains Transaction model"""

from bank.models.account import Account, models, BaseModel


class Transaction(BaseModel):
    """
    Transaction class that inherits from basemodel
    """

    account_id = models.ForeignKey(Account, on_delete=models.CASCADE, db_column='account_id')
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    transaction_type = models.CharField(max_length=10, choices=[('deposit', 'Deposit'), ('withdrawal', 'Withdrawal'),
                                                                ('transfer', 'Transfer')])

    class Meta:
        db_table = 'transactions'

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} on {self.created_at}"
