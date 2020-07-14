import os
import shutil
from .command import BaseCommand


class Command(BaseCommand):

    help = 'Create an empty rested django project'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str, help='project name / directory to create')

    def execute(self, args):
        working_dir = os.getcwd()
        file_dir = os.path.dirname(os.path.abspath(__file__))
        destination = os.path.join(working_dir, args.name)
        source = os.path.normpath(os.path.join(file_dir, '../templates/default'))
        try:
            shutil.copytree(source, destination)
            print(f"Project {args.name} successfully created at {destination}")
        except FileExistsError:
            print(f"Unable to create project, the specified path '{destination}' already exists.")
