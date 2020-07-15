import os
import sys
import argparse
import django
from rested import commands


# main
def main():
    # set environment variable if we are running tests
    if len(sys.argv) >= 2 and sys.argv[1] == 'test':
        os.environ['RESTED_TESTING'] = 'yes'

    # setup django
    sys.path.append(os.getcwd())
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    try:
        django.setup()
    except ModuleNotFoundError:
        pass

    # arguments
    parser = argparse.ArgumentParser(description='')
    subparsers = parser.add_subparsers(help='')

    # commands.register('create', commands.create, subparsers)
    commands.register('serve', commands.serve.Command(), subparsers)
    commands.register('shell', commands.shell.Command(), subparsers)
    commands.register('test', commands.test.Command(), subparsers)
    commands.register('manage', commands.manage.Command(), subparsers)
    commands.register('create', commands.create.Command(), subparsers)
    commands.register('worker', commands.worker.Command(), subparsers)
    commands.register('version', commands.version.Command(), subparsers)
    # # commands.register('sockets', commands.create, subparsers)
    # # commands.register('pipeline', commands.create, subparsers)

    try:
        # hijack the command line and run django's default manage.py script if manage is the second argument
        if commands.manage.inject(): return

        # parse args and execute command
        args = parser.parse_args()
        if hasattr(args, 'cmd'):
            sys.exit(args.cmd(args))
        else:
            parser.print_help()
    except ModuleNotFoundError as exc:
        if "No module named 'settings'" not in str(exc): raise exc
        print('Warning: Unable to detect rested/django project in current directory. Failed to load settings.')
