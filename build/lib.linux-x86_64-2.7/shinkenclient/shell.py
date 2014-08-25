import logging
import os
import sys

from cliff.app import App
from cliff.commandmanager import CommandManager

from shinkenclient.common import restapi
from shinkenclient.common import exceptions as exc

def env(*vars, **kwargs):
    """Search for the first defined of possibly many env vars

    Returns the first environment variable defined in vars, or
    returns the default defined in kwargs.

    """
    for v in vars:
        value = os.environ.get(v, None)
        if value:
            return value
        value = os.environ.get(v.lower(), None)
        if value:
            return value
    return kwargs.get('default', '')

class App(App):

    log = logging.getLogger(__name__)

    def __init__(self):
        super(App, self).__init__(
                description='OpenCloud Monitoring CLI',
                version='0.1',
                command_manager=CommandManager('opencloud.monitor'),
                )

    def initialize_app(self, argv):
        self.log.debug('initialize_app')
        self.restapi = restapi.RESTApi(
            debug=self.options.debug
        )

    def build_option_parser(self, description, version):
        parser = super(App, self).build_option_parser(
            description,
            version)

        # Global arguments
        parser.add_argument(
            '--shinken-url',
            metavar='<shinken-url>',
            default=env('SHINKEN_URL'),
            help='Shinken API URL (Env: SHINKEN_URL)')

        return parser

    def configure_logging(self):
        """Configure logging for the app

        Cliff sets some defaults we don't want so re-work it a bit
        """

        if self.options.debug:
            # --debug forces verbose_level 3
            # Set this here so cliff.app.configure_logging() can work
            self.options.verbose_level = 3

        super(App, self).configure_logging()
        root_logger = logging.getLogger('')

        # Requests logs some stuff at INFO that we don't want
        # unless we have DEBUG
        requests_log = logging.getLogger("requests")
        requests_log.setLevel(logging.ERROR)

        # Other modules we don't want DEBUG output for so
        # don't reset them below
        iso8601_log = logging.getLogger("iso8601")
        iso8601_log.setLevel(logging.ERROR)

        # Set logging to the requested level
        self.dump_stack_trace = False
        if self.options.verbose_level == 0:
            # --quiet
            root_logger.setLevel(logging.ERROR)
        elif self.options.verbose_level == 1:
            # This is the default case, no --debug, --verbose or --quiet
            root_logger.setLevel(logging.WARNING)
        elif self.options.verbose_level == 2:
            # One --verbose
            root_logger.setLevel(logging.INFO)
        elif self.options.verbose_level >= 3:
            # Two or more --verbose
            root_logger.setLevel(logging.DEBUG)
            requests_log.setLevel(logging.DEBUG)

        if self.options.debug:
            # --debug forces traceback
            self.dump_stack_trace = True

    def prepare_to_run_command(self, cmd):
        self.log.debug('prepare_to_run_command %s', cmd.__class__.__name__)
        self.log.debug('validating options')
        if not self.options.shinken_url:
            raise exc.CommandError(
                    "You must provide a Shinken API URL"
                    " either --shinken-url or env[SHINKEN_URL]")

    def clean_up(self, cmd, result, err):
        self.log.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.log.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    myapp = App()
    return myapp.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))