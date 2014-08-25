import logging
import json

from shinkenclient.common import util

from cliff.lister import Lister
from cliff.show import ShowOne
from cliff.command import Command

headers = {'content-type': 'application/json'}

class ReloadShinken(Command):
    """Reload shinken"""

    def take_action(self, parsed_args):
        self.app.restapi.get(self.app.options.shinken_url + "/v1/reload")


class ListHost(Lister):
    """Show a list of hosts.

    """

    log = logging.getLogger(__name__ + ".ListHost")
    columns = ["_id", "host_name", "use", "address", "alias", "hostgroups", "contacts","contact_groups"]
    def take_action(self, parsed_args):
        res = self.app.restapi.list(self.app.options.shinken_url + "/v1/hosts",
                                    response_key="hosts")
        #note: the filter below removes the generic host
        return util.list_table([i for i in res if "host_name" in i], self.columns)

class CreateHost(ShowOne):
    """Create a new host.

    """
    log = logging.getLogger(__name__ + '.CreateHost')
    columns = ["_id", "host_name", "use", "address", "alias", "hostgroups", "contacts", "contact_groups"]

    def get_parser(self, prog_name):
        parser = super(CreateHost, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<server name>',
            help='Name of server to be monitored')
        parser.add_argument(
            'ip',
            metavar='<ip>',
            help='IP of server to be monitored')
        parser.add_argument(
            '--alias',
            metavar='<alias name>',
            help='Alias for this server')
        parser.add_argument(
            '--use',
            metavar='<template name>',
            help='The host will inherit properties from the template')
        parser.add_argument(
            '--hostgroups',
            metavar='<hostgroup>',
            action='append',
            default=[],
            help='Name of hostgroup that this server should be a member of')
        parser.add_argument(
            '--contacts',
            metavar='<contact>',
            action='append',
            default=[],
            help='Name of contacts that this host should report to'
                 'repeat for multiple contacts')
	parser.add_argument(
	    '--contact-groups',
	    metavar='<contact_groups>',
	    action='append',
	    default=[],
	    help='Name of the contact_group that is used for this host')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        data = {"host_name": parsed_args.name, "address": parsed_args.ip}
        if parsed_args.alias:
            data["alias"] = parsed_args.alias
        if parsed_args.contacts:
            data["contacts"] = " ,".join(parsed_args.contacts)
        if parsed_args.hostgroups:
            data["hostgroups"] = " ,".join(parsed_args.hostgroups)
	if parsed_args.contact_groups:
	    data["contact_groups"] = " ,".join(parsed_args.contact_groups)
        if parsed_args.use:
            data["use"] = parsed_args.use

        payload = json.dumps({"hosts": [data]})
        headers = {'content-type': 'application/json'}
        res = self.app.restapi.create(self.app.options.shinken_url + "/v1/hosts",
                                      data=payload,
                                      response_key="hosts",
                                      headers=headers)

        return util.show_one_table(res, self.columns)

class DeleteHost(Lister):
    log = logging.getLogger(__name__ + ".DeleteHost")
    columns = ["_id", "host_name", "use", "address", "alias", "hostgroups", "contacts", "contact_groups"]
    def get_parser(self, prog_name):
        parser = super(DeleteHost, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<server name>',
            help='Name of server to be deleted')
        parser.add_argument(
            'id',
            metavar='<id>',
            help='ID of server to be deleted')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        res = self.app.restapi.delete(self.app.options.shinken_url + "/v1/hosts/" + parsed_args.id)
        print "Host: " + parsed_args.name + " with ID: " + parsed_args.id + " was successfully deleted!"
        return util.list_table([i for i in res if "200" in i],self.columns)

class UpdateHost(Lister):
    """Update an existing host.

    """
    log = logging.getLogger(__name__ + '.UpdateHost')
    columns = ["_id", "host_name", "use", "address", "alias", "hostgroups", "contacts", "contact_groups"]

    def get_parser(self, prog_name):
        parser = super(UpdateHost, self).get_parser(prog_name)
        parser.add_argument(
            '_id',
            metavar='<_id>',
            help='_id of the server to be updated')
        parser.add_argument(
            '--name',
            metavar='<server name>',
            help='Name of server to be updated')
        parser.add_argument(
            '--ip',
            metavar='<ip>',
            help='IP of server to be updated')
        parser.add_argument(
            '--alias',
            metavar='<alias name>',
            help='Alias for this server')
        parser.add_argument(
            '--use',
            metavar='<template name>',
            help='The host will inherit properties from the template')
        parser.add_argument(
            '--hostgroups',
            metavar='<hostgroup>',
            action='append',
            default=[],
            help='Name of hostgroup that this server should be a member of')
        parser.add_argument(
            '--contacts',
            metavar='<contact>',
            action='append',
            default=[],
            help='Name of contacts that this host should report to'
                 'repeat for multiple contacts')
        parser.add_argument(
            '--contact-groups',
            metavar='<contact_groups>',
            action='append',
            default=[],
            help='Name of the contact_group that is used for this host')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        data = {}
        if parsed_args._id:
            parsed_args._id = parsed_args._id
        if parsed_args.alias:
            data["alias"] = parsed_args.alias
        if parsed_args.name:
            data["host_name"] = parsed_args.name
        if parsed_args.ip:
            data["address"] = parsed_args.ip
        if parsed_args.contacts:
            data["contacts"] = " ,".join(parsed_args.contacts)
        if parsed_args.hostgroups:
            data["hostgroups"] = " ,".join(parsed_args.hostgroups)
        if parsed_args.contact_groups:
            data["contact_groups"] = " ,".join(parsed_args.contact_groups)
        if parsed_args.use:
            data["use"] = parsed_args.use

        payload = {"hosts": [data]}
        headers = {'content-type': 'application/json'}

        res = self.app.restapi.patch(self.app.options.shinken_url + "/v1/hosts" + "/" + parsed_args._id,
                                      json=payload)
        print "Host: " + parsed_args.name + " with ID: " + parsed_args._id + " was successfully updated!"
        return util.list_table([i for i in res if "200" in i],self.columns)

class CreateHostGroup(ShowOne):
    """Create a new hostgroup.

    """
    log = logging.getLogger(__name__ + '.CreateHostGroup')
    columns = ["_id", "hostgroup_name", "alias" ]

    def get_parser(self, prog_name):
        parser = super(CreateHostGroup, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<hostgroup name>',
            help='Name of hostgroup')
        parser.add_argument(
            '--alias',
            metavar='<alias>',
            help='Alias for this hostgroup')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        data = {"hostgroup_name": parsed_args.name}
        if parsed_args.alias:
            data["alias"] = parsed_args.alias

        payload = json.dumps({"hostgroups": [data]})
        headers = {'content-type': 'application/json'}
        res = self.app.restapi.create(self.app.options.shinken_url + "/v1/hostgroups",
                                      data=payload,
                                      response_key="hostgroups",
                                      headers=headers)

        return util.show_one_table(res, self.columns)

class DeleteHostGroup(Lister):
    log = logging.getLogger(__name__ + ".DeleteHostGroup")
    columns = ["_id", "host_name", "use", "address", "alias", "hostgroups", "contacts", "contact_groups"]
    def get_parser(self, prog_name):
        parser = super(DeleteHostGroup, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar='<id>',
            help='ID of HostGroup to be deleted')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        res = self.app.restapi.delete(self.app.options.shinken_url + "/v1/hostgroups/" + parsed_args.id)
        print "HostGroup  with ID: " + parsed_args.id + " was successfully deleted!"
        return util.list_table([i for i in res if "200" in i],self.columns)

class ListHostGroup(Lister):
    """Show a list of hostgroups.

    """

    log = logging.getLogger(__name__ + ".ListHostGroup")
    columns = ["_id", "hostgroup_name", "alias"]

    def take_action(self, parsed_args):
        res = self.app.restapi.list(self.app.options.shinken_url + "/v1/hostgroups",
                                    response_key="hostgroups")
        return util.list_table(res, self.columns)


class CreateGenericHost(ShowOne):
    """Create a new generic host.

    define host{
        name                            generic-host    ; The name of this host template
        notifications_enabled           1               ; Host notifications are enabled
        event_handler_enabled           1               ; Host event handler is enabled
        max_check_attempts              3               ; Check each Linux host 10 times (max)
        flap_detection_enabled          1               ; Flap detection is enabled
        failure_prediction_enabled      1               ; Failure prediction is enabled
        process_perf_data               1               ; Process performance data
        retain_status_information       1               ; Retain status information across program restarts
        retain_nonstatus_information    1               ; Retain non-status information across program restarts
        notification_period             24x7            ; Send host notifications at any time
        register                        0               ; DONT REGISTER THIS DEFINITION - ITS NOT A REAL HOST, JUST A TEMPLATE!
        }

    """
    log = logging.getLogger(__name__ + '.CreateGenericHost')
    columns = ["_id", "name", "notifications_enabled", "event_handler_enabled", "max_check_attempts",
               "flap_detection_enabled", "failure_prediction_enabled", "process_perf_data", "retain_status_information",
               "retain_nonstatus_information", "notification_period", "register"]

    def get_parser(self, prog_name):
        parser = super(CreateGenericHost, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<template name>',
            help='Name of generic host template')
        parser.add_argument(
            '--notifications-enabled',
            metavar='<1|0>',
            default='1',
            help='Host notifications are enabled [default: 1]')
        parser.add_argument(
            '--event-handler-enabled',
            metavar='<1|0>',
            default='1',
            help='Host event handler is enabled [default: 1]')
        parser.add_argument(
            '--max-check-attempts',
            metavar='<1-10>',
            default='3',
            help='Check each Linux host 10 times [default: 3]')
        parser.add_argument(
            '--flap-detection-enabled',
            metavar='<1|0>',
            default='1',
            help='Flap detection is enabled [default: 1]')
        parser.add_argument(
            '--failure-prediction-enabled',
            metavar='<1|0>',
            default='1',
            help='Failure prediction is enabled [default: 1]')
        parser.add_argument(
            '--process-perf-data',
            metavar='<1|0>',
            default='1',
            help='Process performance data [default: 1]')
        parser.add_argument(
            '--retain-status-information',
            metavar='<1|0>',
            default='1',
            help='Retain status information across program restarts [default: 1]')
        parser.add_argument(
            '--retain-nonstatus-information',
            metavar='<1|0>',
            default='1',
            help='Retain non-status information across program restarts [default: 1]')
        parser.add_argument(
            '--notification-period',
            default="24x7",
            help='Send host notifications at any time [default: 24x7]')

        return parser


    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        data = {key: getattr(parsed_args, key) for key in self.columns if key not in ("_id", "register")}
        data["register"] = "0"
        payload = json.dumps({"hosts": [data]})
        headers = {'content-type': 'application/json'}
        res = self.app.restapi.create(self.app.options.shinken_url + "/v1/hosts",
                                      data=payload,
                                      response_key="hosts",
                                      headers=headers)

        return util.show_one_table(res, self.columns)


