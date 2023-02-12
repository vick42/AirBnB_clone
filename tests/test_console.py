#!/usr/bin/python3
"""This test module consists test classes and function to test TestHBNBCommand."""
from console import HBNBCommand
from models.engine.file_storage import FileStorage
import unittest
import datetime
from unittest.mock import patch
import sys
from io import StringIO
import re


class TestHBNBCommand(unittest.TestCase):
    """This class contains methods to test HBNBCommand console."""

    def setUp(self) -> None:
        """Setup test case"""
        return super().setUp()

    def create_class(self, classname):
        """Creates a class for console tests."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create {}".format(classname))
        uid = f.getvalue()[:-1]
        return uid

    def test_help(self):
        """Tests help command"""
        expect_string = '''
Documented commands (type help <topic>):
========================================
EOF  all  count  create  destroy  help  quit  show  update

'''
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help")
            self.assertEqual(expect_string, f.getvalue())

    def test_create_class(self, ):
        """Tests create <className> command."""
        available_classes = HBNBCommand.classes
        for cls_name in available_classes.keys():
            uid = self.create_class(classname=cls_name)
            uuid_length = 36
            self.assertEqual(len(uid), uuid_length)

    def test_create_error(self):
        """Tests create command with errors."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create unknowClass")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

    def test_update(self):
        """Tests update <className> <id> "att_name": "att_val" command"""
        classname = "User"
        attr = "first_name"
        val = "Bob"
        uid = self.create_class(classname)
        self.assertEqual(len(uid), 36)
        cmd = 'update {} {} "{}" "{}"'.format(classname, uid, attr, val)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(cmd)
        s = f.getvalue()
        self.assertEqual(len(s), 0)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('show {} {}'.format(classname, uid))
        s = f.getvalue()
        self.assertIn(attr, s)
        self.assertIn(val, s)

    def test_show(self):
        """Tests show <className>.("<id>") command"""
        classname = "User"
        uid = self.create_class(classname)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, uid))
        s = f.getvalue()
        self.assertIn(uid, s)

    def test_count_error(self):
        """Tests count <className> command with errors."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(" count unknownClass")
        msg = f.getvalue()
        self.assertEqual(msg, "** class doesn't exist **\n")
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("count ")
        msg = f.getvalue()
        self.assertEqual(msg, "** class name missing **\n")

    def test_emptyline(self):
        """Tests emptyline functionality."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("\n")
        s = "\n"
        self.assertEqual(s, f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("\n")
        s = "\n"
        self.assertEqual(s, f.getvalue())

    def test_count(self):
        """Test test count <className> command."""
        class_name = 'BaseModel'
        self.create_class(class_name)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("count {}".format(class_name))
        s = f.getvalue()[:-1]
        self.assertTrue(len(s) > 0)
        self.assertTrue(int(s) > 0)
