import logging
import json

from shinkenclient.common import util

from cliff.lister import Lister
from cliff.show import ShowOne

headers = {'content-type': 'application/json'}

class ListCommand(Lister):
    """Show a list of commands.

    """

    log = logging.getLogger(__name__ + ".ListCommand")
    columns = ["_id", "command_name", "command_line", "module_type"]
    def take_action(self, parsed_args):
        res = self.app.restapi.list(self.app.options.shinken_url + "/v1/commands",
                                    response_key="commands")
        return util.list_table(res, self.columns)


class CreateCommand(ShowOne):
    """Create a new command.

    """
    log = logging.getLogger(__name__ + '.CreateCommand')
    columns = ["_id", "command_name", "command_line", "module_type"]

    def get_parser(self, prog_name):
        parser = super(CreateCommand, self).get_parser(prog_name)
        parser.add_argument(
            'command_name',
            metavar='<command name>',
            help='Name of the command')
        parser.add_argument(
            '--command-line',
            required=True,
            metavar='<command line>',
            help='Command line')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        data = {"command_name": parsed_args.command_name, "command_line": parsed_args.command_line}
        if "nrpe" in parsed_args.command_line:
            data["module_type"] = "nrpe_poller"

        payload = json.dumps({"commands": [data]})
        headers = {'content-type': 'application/json'}
        res = self.app.restapi.create(self.app.options.shinken_url + "/v1/commands",
                                      data=payload,
                                      response_key="commands",
                                      headers=headers)

        return util.show_one_table(res, self.columns)

class UpdateCommand(Lister):
    """Update an existing Command.

    """
    log = logging.getLogger(__name__ + '.UpdateCommand')
    columns = ["_id", "command_name", "command_line", "module_type"]

    def get_parser(self, prog_name):
        parser = super(UpdateCommand, self).get_parser(prog_name)
        parser.add_argument(
            '_id',
            metavar='<_id>',
            help='_id of the server to be updated')
        parser.add_argument(
            '--command-name',
            metavar='<command_name>',
            help='Name of command to be updated')
        parser.add_argument(
            '--command-line',
            metavar='<command_line>',
            help='Command Line that is to be updated')

        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        data = {}
        if parsed_args._id:
            parsed_args._id = parsed_args._id
        if parsed_args.command_name:
            data["command_name"] = parsed_args.command_name
        if parsed_args.command_line:
            data["command_line"] = parsed_args.command_line

        payload = {"commands": [data]}
        headers = {'content-type': 'application/json'}

        res = self.app.restapi.patch(self.app.options.shinken_url + "/v1/commands" + "/" + parsed_args._id,
                                      json=payload)

        print "Command with ID: " + parsed_args.id + " was successfully updated!"
        return util.list_table([i for i in res if "200" in i],self.columns)

class DeleteCommand(Lister):
    log = logging.getLogger(__name__ + ".DeleteCommand")
    columns = ["_id", "command_name", "command_line", "module_type"]

    def get_parser(self, prog_name):
        parser = super(DeleteCommand, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar='<id>',
            help='id of command to be deleted')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        res = self.app.restapi.delete(self.app.options.shinken_url + "/v1/commands/" + parsed_args.id)
        print "Command with ID: " + parsed_args.id + " was successfully deleted!"
        return util.list_table([i for i in res if "200" in i],self.columns)
 
