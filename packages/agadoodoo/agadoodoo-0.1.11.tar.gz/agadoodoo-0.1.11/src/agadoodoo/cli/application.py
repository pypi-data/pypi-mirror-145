import os
import importlib
from cleo.application import Application as BaseApplication
from cleo.loaders.factory_command_loader import FactoryCommandLoader
from agadoodoo.cli.commands import COMMANDS
from agadoodoo.__version__ import __version__


__BASE_DIR__ = os.path.dirname(os.path.abspath(__file__))


def load_command(name):
    def load():
        module = importlib.import_module('agadoodoo.cli.commands.' + name)
        klass = getattr(module, name.title() + 'Command')
        return klass
    return load


class Application(BaseApplication):
    def __init__(self):
        super().__init__('agadoodoo', __version__)
        
        loader = FactoryCommandLoader({ cmd: load_command(cmd) for cmd in COMMANDS })
        self.set_command_loader(loader)


def run():
    return Application().run()
