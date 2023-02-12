#!/usr/bin/python3
import sys
import cmd
from models import storage
from models.base_model import BaseModel
from models import User, Place, State, City, Amenity, Review


class HBNBCommand(cmd.Cmd):
    """ Command Line Interface for the HBNB console"""

    classes = {
        'BaseModel': BaseModel,
        'User': User,
        'Amenity': Amenity,
        'City': City,
        'Place': Place,
        'Review': Review,
        'State': State,
    }

    dot_commands = ['all', 'count', 'show', 'destroy', 'update']

    types = {
        'number_rooms': int, 'number_bathrooms': int,
        'max_guest': int, 'price_by_night': int,
        'latitude': float, 'longitude': float
    }

    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    def do_quit(self, command):
        """Exits HBNB console."""
        exit()

    def hep_quit(self):
        """Prints help text for quit command"""
        print("Quit command to exit the program.\n")

    def do_EOF(self, arg):
        """Handles EOF to exit program"""
        print()
        exit()

    def help_EOF(self):
        """Prints the help text for EOF command"""
        print("EOF command to exit the program without formatting.\n")

    def do_create(self, args):
        """ Creates an object of a given class type."""
        if not args:
            print("** class name missing **")
            return
        elif args not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        new_instance = HBNBCommand.classes[args]()
        storage.save()
        print(new_instance.id)
        storage.save()

    def help_create(self):
        """ Prints help text for the create command."""
        print("Creates a class of a given type")
        print("\t[Usage]: create <className>\n")

    def do_show(self, args):
        """Prints the string representation of an instance based on the class name and id"""
        params = args.partition(" ")
        c_name = params[0]
        c_id = params[2].strip()

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id
        try:
            print(storage._FileStorage__objects[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """Prints help text for the show command."""
        print("Prints the string representation of an instance based on the class name and id.")
        print("\t[Usage]: show <className> <objId>\n")

    def do_destroy(self, args):
        """Deletes an instance based on the class name and id (save the change into the JSON file)."""
        params = args.partition(" ")
        c_name = params[0]
        c_id = params[2].strip()

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id

        try:
            del (storage.all()[key])
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """Prints help text for the destroy command."""
        print("Destroys an instance based on the class name and id.")
        print("\t[Usage]: destroy <className> <objId>\n")

    def do_all(self, args):
        """Show all objects from storage."""

        obj_list = []
        if args:
            params = args.partition(" ")
            c_name = params[0]

            if not c_name:
                print("** class name missing **")
                return
            elif args not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for k, v in storage._FileStorage__objects.items():
                if c_name == k.split('.')[0]:
                    obj_list.append(str(v))
        else:
            for k, v in storage._FileStorage__objects.items():
                obj_list.append(str(v))
        print(obj_list)

    def help_all(self):
        """Prints help text for the all command."""
        print("Prints all string representation of all instances based or not on the class name."
              " ClassName is optional.")
        print("\t[Usage]: all <className>\n")

    def do_update(self, args):
        """Show all objects from storage."""

        # handle class name from args
        params = args.partition(' ')
        if params[0]:
            c_name = params[0]
        else:
            print("** class name missing **")
            return
        if c_name not in HBNBCommand.classes:  # class name invalid
            print("** class doesn't exist **")
            return

        # handle instance id from args
        params = params[2].partition(' ')
        if params[0]:
            c_id = params[0]
        else:
            print("** instance id missing **")
            return
        key = c_name + "." + c_id
        if key not in storage.all():
            print("** no instance found **")
            return

        # handle attribute name and value pass as JSON/dict {"key": "value"}
        attr_params = params[2]
        if '{' in attr_params and '}' in attr_params and type(eval(attr_params)) is dict:
            kwargs = eval(attr_params)
            args = []  # reformat kwargs into list, ex: [<attr_name>, <attr_value>, ...]
            for k, v in kwargs.items():
                args.append(k)
                args.append(v)
        else:  # isolate args
            att_name = None
            if attr_params and attr_params[0] == '\"':  # check for quoted arg
                second_quote = attr_params.find('\"', 1)
                att_name = attr_params[1:second_quote]
                attr_params = attr_params[second_quote + 1:]

            # if att_name was not quoted arg
            attr_params = attr_params.partition(' ')
            if not att_name and attr_params[0]:
                att_name = attr_params[0]

            # check for quoted val arg
            att_val = None
            attr_val_pre_parsed = attr_params[2]
            if attr_val_pre_parsed and attr_val_pre_parsed[0] == '\"':
                att_val = attr_val_pre_parsed[1:args[2].find('\"', 1)]

            # if att_val was not quoted arg
            if not att_val and attr_val_pre_parsed:
                att_val = attr_val_pre_parsed.partition(' ')[0]

            args = [att_name, att_val]

        # retrieve dictionary of current objects
        new_dict = storage.all()[key]

        # iterate through attr names and values
        for index, att_name in enumerate(args):
            # block only runs on even iterations
            if (index % 2 == 0):
                att_val = args[index + 1]  # following item is value
                if not att_name:  # check for att_name
                    print("** attribute name missing **")
                    return
                if not att_val:  # check for att_value
                    print("** value missing **")
                    return
                # type cast as necessary
                if att_name in HBNBCommand.types:
                    att_val = HBNBCommand.types[att_name](att_val)

                # update dictionary with name, value pair
                new_dict.__dict__.update({att_name: att_val})

        new_dict.save()  # save updates to file

    def help_update(self):
        """Prints help text for the update command."""
        print("Updates an instance based on the class name and id by adding or updating attribute.")
        print("Only one attribute can be updated at a time.")
        print(
            '\t[Usage]: update <class name> <id> <attribute name> "<attribute value>"')

    def precmd(self, line):
        """Pre computes advance commands.
        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _command = _class_name = _id = _args = ''

        if not ('.' in line and '(' in line and ')' in line):

            return line

        try:  # parse line left to right
            pline = line[:]  # parsed line
            # parse class name
            _class_name = pline[:pline.find('.')]

            # parse command
            _command = pline[pline.find('.') + 1:pline.find('(')]
            if _command not in HBNBCommand.dot_commands:
                raise Exception('Invalid command "{}". Valid commands are {}'.format(
                    _command, HBNBCommand.dot_commands))

            # parse arguments, if exists
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # pline convert to tuple

                # isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')
                # possible bug here:
                # empty quotes register as empty _id when replaced

                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *args or **kwargs
                    if pline[0] == '{' and pline[-1] == '}'\
                            and type(eval(pline)) == dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
                        # _args = _args.replace('\"', '')
            line = ' '.join([_command, _class_name, _id, _args])

        except Exception as mess:
            raise Exception(mess)
        finally:
            return line

    def do_count(self, args):
        """Counts current number of instances of a class."""
        if not args:
            print("** class name missing **")
            return
        elif args not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        count = 0
        for k, v in storage._FileStorage__objects.items():
            if args == k.split('.')[0]:
                count += 1
        print(count)

    def help_count(self):
        """Prints help text for count command."""
        print("\tUsage: count <class_name>")

    def emptyline(self):
        print('')


if __name__ == '__main__':
    HBNBCommand().cmdloop()
