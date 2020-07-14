from django_extensions.management.commands.shell_plus import Command as ShellPlusCommand
from .command import DjangoCommand

class Command(DjangoCommand, ShellPlusCommand):
    help = 'Interactive python shell with all models autoloaded'
