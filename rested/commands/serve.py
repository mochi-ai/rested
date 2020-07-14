from channels.management.commands.runserver import Command as RunServerCommand
from .command import DjangoCommand

class Command(DjangoCommand, RunServerCommand):
    default_addr = '0.0.0.0'
    default_addr_ipv6 = '::'
