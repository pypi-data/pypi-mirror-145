from cleo.commands.command import Command


class TestCommand(Command):
    """
    test command
    
    test
    """
    
    def handle(self):
        print('test')
