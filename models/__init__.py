"""This module contains storage model classes, function and constants."""
from .engine.file_storage import FileStorage
from .amenity import Amenity
from .city import City
from .place import Place
from .review import Review
from .state import State
from .user import User

storage = FileStorage()
storage.reload()
