import sys
from subprocess import call
from .command import BaseCommand


class Command(BaseCommand):

    help = 'Run background task worker'

    def add_arguments(self, parser):
        parser.add_argument('-b', '--beats', action='store_true', help='Run beats sheduler with worker')

    def execute(self, args):
        print(args)
        arguments = ''
        if args.beats: arguments = '-B'
        try:
            sys.exit(call(f'celery -A rested.worker worker {arguments} --loglevel=info', shell=True))
        except KeyboardInterrupt:
            pass # should pass these interruprs to subprocess, right now parent closes before subprocess
