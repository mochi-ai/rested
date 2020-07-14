# register a command
def register(name, command, subparsers):
    parser = subparsers.add_parser(name, help=command.help)
    parser.set_defaults(cmd=command.execute)
    command.add_arguments(parser)

# rested command patterned after django command
class BaseCommand:
    help = ''

    def add_arguments(self, parser):
        pass

    def execute(self, args):
        pass

# mixin that enables us to execute django commands from rested command line
class DjangoCommand:
    def execute(self, args):
        options = vars(args)
        args = options.pop('args', ())
        base_options = {'verbosity': 1, 'force_color': False, 'no_color': False, 'skip_checks': False}
        super().execute(*args, **{**options, **base_options})
