#!/usr/bin/env python3

"""Contains Event class"""

from bank.models.base_model import BaseModel, models


class Event(BaseModel):
    """
    Event class
    """
    event_type = models.CharField(max_length=50)
    payload = models.JSONField()

    class Meta:
        db_table = 'events'

    def __str__(self):
        return f"{self.event_type} at {self.created_at}"
