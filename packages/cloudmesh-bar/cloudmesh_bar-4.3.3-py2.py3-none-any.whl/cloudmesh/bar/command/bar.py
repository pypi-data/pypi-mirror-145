from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.bar.api.manager import Manager
from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from pprint import pprint
from cloudmesh.common.debug import VERBOSE
from cloudmesh.shell.command import map_parameters
from cloudmesh.common.parameter import Parameter

class BarCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_bar(self, args, arguments):
        """
        ::

          Usage:
                bar --file=FILE
                bar --parameter=PARAMETER
                bar run COMMAND...
                bar list

          This command does some useful things.

          Arguments:
              FILE   a file name
              PARAMETER  a parameterized parameter of the form "a[0-3],a5"

          Options:
              -f      specify the file

          Description:

            > cms bar --parameter="a[1-2,5],a10"
            >    prints the expanded parameter as a list
            >    ['a1', 'a2', 'a3', 'a4', 'a5', 'a10']

        """


        # arguments.FILE = arguments['--file'] or None

        map_parameters(arguments, "file", "parameter")

        VERBOSE(arguments)

        m = Manager()

        if arguments.file:
            print("option a")
            m.list(path_expand(arguments.file))

        elif arguments.list:
            print("option b")
            m.list("just calling list without parameter")

        elif arguments.parameter:
            print ("parameter")
            print (Parameter.expand(arguments.parameter))

        elif arguments.run:

            print ("run")
            print("showcasing to define a command with parameters as COMMAND...")
            print (arguments.COMMAND)
            print("this will return an array, which we simply can join to get the command. or keep as array")
            arguments.COMMAND_str = ' '.join(arguments.COMMAND)
            print(arguments.COMMAND_str)
            print(arguments.COMMAND)

        Console.error("This is just a sample of an error")
        Console.warning("This is just a sample of a warning")
        Console.info("This is just a sample of an info")

        Console.info(" You can witch debugging on and off with 'cms debug on' or 'cms debug off'")

        return ""
