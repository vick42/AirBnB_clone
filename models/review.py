#!/usr/bin/python3
"""This module contains classes, functions and constants."""
from models.base_model import BaseModel


class Review(BaseModel):
    """This Review class contains review related attributes to store."""
    place_id = ""
    user_id = ""
    text = ""
