#!/usr/bin/python3
"""HBNB console module for managing HBNB application data.

Commands:
- create: Create a new instance of a class.
- show: Print an instance based on the class and id.
- destroy: Delete an instance based on the class and id.
- all: Print string representations of instances.
- update: Update an instance based on class, id, attribute, and value.
- count: Count the number of instances of a class.
- quit: Exit the console.
"""


import cmd
import json
import shlex
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


classes = {
    "Amenity": Amenity,
    "BaseModel": BaseModel,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User
}


class HBNBCommand(cmd.Cmd):
    """
    Defines the HBNB command interpreter.
    """

    prompt = "(hbnb) "

    def emptyline(self):
        """
        Ignore empty lines.
        """
        pass

    def do_quit(self, line):
        """
        Quit command to exit the program.
        """
        return True

    def do_EOF(self, line):
        """
        EOF signal to exit the program.
        """
        print("")
        return True

    def do_create(self, args):
        """
        Create a new instance of a class and save it to the database.

        Usage: create <class_name> [param1=value1] [param2=value2] ...

        Examples:
            - create BaseModel
            - create User email="test@example.com" password="123456"

        Note:
            The class_name should be one of the available classes: Amenity, BaseModel,
            City, Place, Review, State, User.
        """
        if not args:
            print("** class name missing **")
            return

        try:
            args = shlex.split(args)
            class_name = args[0]
            if class_name not in classes:
                raise NameError("Class doesn't exist")

            new_instance = classes[class_name]()

            for arg in args[1:]:
                key, value = arg.split("=")
                key = key.replace("_", " ")
                value = value.replace("_", " ")

                # Check if the value is enclosed in double quotes and remove
                # them
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]

                try:
                    value = eval(value)
                except NameError:
                    pass

                setattr(new_instance, key, value)

            # Check and handle the state_id attribute manually if provided
            if "state_id" in new_instance.__dict__:
                state_id = new_instance.__dict__["state_id"]
                if state_id not in [
                        state.id for state in storage.all(State).values()]:
                    raise ValueError("State ID doesn't exist")

            new_instance.save()
            print(new_instance.id)

        except NameError as e:
            print("** {} **".format(e))
        except ValueError as e:
            print("** {} **".format(e))
        except Exception as e:
            print("** {}".format(e))

    def do_show(self, line):
        """
        Prints the string representation of an instance.

        Usage: show <class> <id>

        Prints the string representation of the instance with the given class and id.
        """
        try:
            if not line:
                raise SyntaxError("Class name missing")

            args = shlex.split(args)
            class_name = args[0]
            if class_name not in classes:
                raise NameError("Class doesn't exist")
            if len(args) < 2:
                raise IndexError("Instance id missing")

            objects = storage.all()
            key = "{}.{}".format(class_name, args[1])
            if key in objects:
                print(objects[key])
            else:
                raise KeyError("No instance found")

        except SyntaxError as e:
            print("** {} **".format(e))
        except NameError as e:
            print("** {} **".format(e))
        except IndexError as e:
            print("** {} **".format(e))
        except KeyError as e:
            print("** {} **".format(e))

    def do_destroy(self, line):
        """
        Deletes an instance based on the class name and id.

        Usage: destroy <class> <id>

        Deletes the instance with the given class and id.
        """
        try:
            if not line:
                raise SyntaxError("Class name missing")

            args = split(line)
            class_name = args[0]
            if class_name not in classes:
                raise NameError("Class doesn't exist")
            if len(args) < 2:
                raise IndexError("Instance id missing")

            objects = storage.all()
            key = "{}.{}".format(class_name, args[1])
            if key in objects:
                del objects[key]
                storage.save()
            else:
                raise KeyError("No instance found")

        except SyntaxError as e:
            print("** {} **".format(e))
        except NameError as e:
            print("** {} **".format(e))
        except IndexError as e:
            print("** {} **".format(e))
        except KeyError as e:
            print("** {} **".format(e))

    def do_all(self, line):
        """
        Display string representations of all instances of a given class.

        Usage: all <class> or all

        If no class is specified, displays all instantiated objects.
        """
        try:
            args = split(line)
            if len(args) > 0 and args[0] not in classes:
                raise NameError("Class doesn't exist")

            if len(args) == 0:
                objects = storage.all()
            else:
                objects = storage.all(classes[args[0]])

            print([str(obj) for obj in objects.values()])

        except NameError as e:
            print("** {} **".format(e))

    def do_update(self, line):
        """
        Update an instance by adding or updating attributes.

        Usage: update <class> <id> <attribute> <value>

        Updates the attribute of the instance with the given class, id, attribute, and value.
        """
        try:
            if not line:
                raise SyntaxError("Class name missing")

            args = split(line)
            class_name = args[0]
            if class_name not in classes:
                raise NameError("Class doesn't exist")
            if len(args) < 2:
                raise IndexError("Instance id missing")
            if len(args) < 3:
                raise AttributeError("Attribute name missing")
            if len(args) < 4:
                raise ValueError("Value missing")

            objects = storage.all()
            key = "{}.{}".format(class_name, args[1])
            if key in objects:
                obj = objects[key]
                try:
                    setattr(obj, args[2], eval(args[3]))
                except Exception:
                    setattr(obj, args[2], args[3])
                obj.save()
            else:
                raise KeyError("No instance found")

        except SyntaxError as e:
            print("** {} **".format(e))
        except NameError as e:
            print("** {} **".format(e))
        except IndexError as e:
            print("** {} **".format(e))
        except KeyError as e:
            print("** {} **".format(e))
        except AttributeError as e:
            print("** {} **".format(e))
        except ValueError as e:
            print("** {} **".format(e))


if __name__ == '__main__':
    HBNBCommand().cmdloop()
