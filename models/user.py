#!/usr/bin/python3
"""This module defines a user reated classes, functions and constants"""
from models.base_model import BaseModel


class User(BaseModel):
    """This class defines a user model."""
    email = ''
    password = ''
    first_name = ''
    last_name = ''
