# contains function to clear screen
from ngoto.util.command import Command
import os

class Clear(Command):

    def getDescription(self):
        return "Command to clear screen"

    def getActions(self):
        return ["cls", "clear"]

    def performAction(self, *args):
        os.system('cls' if os.name in ('nt', 'dos') else 'clear') 
        args[2].debug(f'Clearing screen', program='Clear')
        return args[0]