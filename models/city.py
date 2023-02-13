#!/usr/bin/python3
"""This module contains classes, functions and constants related to city model."""
from models.base_model import BaseModel


class City(BaseModel):
    """City class, contains city related attributes to store."""
    state_id = ''
    name = ''
