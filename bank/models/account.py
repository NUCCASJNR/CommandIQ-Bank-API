#!/usr/bin/env python3

"""Contains Account Model"""

from bank.models.user import BaseModel, User, models


class Account(BaseModel):
    """
    Account Model
    """
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, db_column='user_id')
    account_number = models.IntegerField(blank=False, max_length=10, unique=True)
    account_name = models.CharField(blank=False, max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    class Meta:
        db_table = 'accounts'

    def __str__(self):
        return f"{self.account_name} ({self.account_number}) - {self.user.username}"
