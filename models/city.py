#!/usr/bin/python3
"""This module creates a user class."""
from models.base_model import BaseModel


class City(BaseModel):
    """Class for manaaging city objects."""
    state_id = ''
    name = ''
