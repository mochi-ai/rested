import sys
import pytest
from subprocess import call
from .command import BaseCommand
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from rested.test import plugin


class TestEventHandler(PatternMatchingEventHandler):
    def __init__(self):
        super().__init__(ignore_directories=True, ignore_patterns=[
            '*.pytest_cache*',
            '*__pycache__*',
            '*.cache',
            '*.sqlite3',
            '*.pyc'])
        self.changed = True

    def check(self, handler):
        if self.changed:
            self.changed = False
            handler()

    def on_any_event(self, event):
        # print(event)
        self.changed = True

def watch(on_change, path='.'):
    path = '.'
    handler = TestEventHandler()
    observer = Observer()
    observer.schedule(handler, path, recursive=True)
    observer.start()
    try:
        while observer.isAlive():
            handler.check(on_change)
            observer.join(0.25)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


class Command(BaseCommand):

    help = 'Discover and run tests in the specified modules or the current directory'

    def add_arguments(self, parser):
        parser.add_argument('pattern', type=str, nargs='?', help='all tests matching this pattern will be run')
        parser.add_argument('-f', '--failfast', action='store_true', help='stop tests after first failure')
        parser.add_argument('-k', '--keepdb', action='store_true', help='keep db between tests')
        parser.add_argument('-w', '--watch', action='store_true', help='rerun tests when files change')

    def execute(self, args):
        # setup tests
        argv = []
        if args.pattern:
            argv += ['-k', args.pattern]
        if args.failfast:
            argv.append('--exitfirst')
        if args.keepdb:
            argv.append('--reuse-db')

        # run tests (with or without watcher)
        if args.watch:
            return watch(lambda: call([arg for arg in sys.argv if arg not in ['-w', '--watch']]))
        return pytest.main(argv, plugins=[plugin])
