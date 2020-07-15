import os
from .command import BaseCommand


class Command(BaseCommand):

    help = 'Display rested version'

    def execute(self, args):
        file_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(file_dir, '../version.txt')) as file:
            print(file.read().strip())
