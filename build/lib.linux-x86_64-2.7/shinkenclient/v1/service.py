import logging
import json

from shinkenclient.common import util

from cliff.lister import Lister
from cliff.show import ShowOne

headers = {'content-type': 'application/json'}

class ListService(Lister):
    """Show a list of services.

    """

    log = logging.getLogger(__name__ + ".ListService")
    columns = ["_id", "host_name", "use", "hostgroup_name", "service_description", "check_command","contact_groups"]
    def take_action(self, parsed_args):
        res = self.app.restapi.list(self.app.options.shinken_url + "/v1/services",
                                    response_key="services")
        #note: the filter below removes the generic host
        return util.list_table([i for i in res if "host_name" in i], self.columns)


class CreateService(ShowOne):
    """Create a new service.

    """
    log = logging.getLogger(__name__ + '.CreateService')
    columns = ["_id", "host_name", "use", "hostgroup_name", "service_description", "check_command", "event-handler","contact_groups"]

    def get_parser(self, prog_name):
        parser = super(CreateService, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<server name>',
            help='Name of server to be monitored')
        parser.add_argument(
            '--hostgroup-name',
            action='append',
            default=[],
            metavar='<hostgroup name>',
            help='Hostgroup names'
                 'repeat for multiple hostgroups')
        parser.add_argument(
            '--service-description',
            metavar='<description>',
            help='Service description')
        parser.add_argument(
            '--check-command',
            metavar='<check command>',
            help='Check command')
        parser.add_argument(
            '--use',
            metavar='<template>',
            help='Service template to inherit props from')
        parser.add_argument(
            '--custom',
            action='append',
            default=[],
            metavar="<key_value_pair>",
            help="Custom key and value (e.g. foo=bar)"
                 " repeat for multiple key value pairs")
        parser.add_argument(
            '--contact-groups',
            metavar="<contact_groups>",
            help='Contact Group to add')
        parser.add_argument(
            '--event-handler',
            metavar='<handler>',
            help='Event handler')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        data = {"host_name": parsed_args.name}
        if parsed_args.hostgroup_name:
            data["hostgroup_name"] = " ,".join(parsed_args.hostgroup_name)
        if parsed_args.service_description:
            data["service_description"] = parsed_args.service_description
        if parsed_args.check_command:
            data["check_command"] = parsed_args.check_command
        if parsed_args.use:
            data["use"] = parsed_args.use
        if parsed_args.contact_groups:
            data["contact_groups"] = parsed_args.contact_groups
        if parsed_args.event_handler:
            data["event_handler"] = parsed_args.event_handler
        if parsed_args.custom:
            import re
            r = re.compile('.*=.*')
            for custom in parsed_args.custom:
                if r.match(custom) is None:
                    raise("custom argument error.  ''{0}'' is invalid."
                          "custom argument value must be in form key=value")
                (key,value) = custom.split('=')
                data[key] = value

        payload = json.dumps({"services": [data]})
        headers = {'content-type': 'application/json'}
        res = self.app.restapi.create(self.app.options.shinken_url + "/v1/services",
                                      data=payload,
                                      response_key="services",
                                      headers=headers)

        return util.show_one_table(res, self.columns)

class DeleteService(Lister):
    log = logging.getLogger(__name__ + ".DeleteService")
    columns = ["_id", "host_name", "use", "address", "alias", "hostgroups", "contacts", "contact_groups"]
    def get_parser(self, prog_name):
        parser = super(DeleteService, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar='<id>',
            help='ID of service to be deleted')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        res = self.app.restapi.delete(self.app.options.shinken_url + "/v1/services/" + parsed_args.id)
        print "Service with ID: " + parsed_args.id + " was successfully deleted!"
        return util.list_table([i for i in res if "200" in i],self.columns)

class UpdateService(Lister):
    """Update an existing Service.

    """
    log = logging.getLogger(__name__ + '.UpdateService')
    columns = ["_id", "host_name", "use", "hostgroup_name", "service_description", "check_command", "event-handler", "contact_groups"]

    def get_parser(self, prog_name):
        parser = super(UpdateService, self).get_parser(prog_name)
        parser.add_argument(
            '_id',
            metavar='<_id>',
            help='_id of the server to be updated')
        parser.add_argument(
            '--name',
            metavar='<server name>',
            help='Name of server to be monitored')
        parser.add_argument(
            '--hostgroup-name',
            action='append',
            default=[],
            metavar='<hostgroup name>',
            help='Hostgroup names'
                 'repeat for multiple hostgroups')
        parser.add_argument(
            '--service-description',
            metavar='<description>',
            help='Service description')
        parser.add_argument(
            '--check-command',
            metavar='<check command>',
            help='Check command')
        parser.add_argument(
            '--use',
            metavar='<template>',
            help='Service template to inherit props from')
        parser.add_argument(
            "--contact-groups",
            metavar="<contact_groups>",
            help='Contact Groups to add')
        parser.add_argument(
            '--event-handler',
            metavar='<handler>',
            help='Event handler')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        data = {"service_name": parsed_args.name}
        if parsed_args.hostgroup_name:
            data["hostgroup_name"] = " ,".join(parsed_args.hostgroup_name)
        if parsed_args.service_description:
            data["service_description"] = parsed_args.service_description
        if parsed_args.name:
            data["host_name"] = parsed_args.name
        if parsed_args.check_command:
            data["check_command"] = parsed_args.check_command
        if parsed_args.use:
            data["use"] = parsed_args.use
        if parsed_args.event_handler:
            data["event_handler"] = parsed_args.event_handler
        if parsed_args.contact_groups:
            data["contact_groups"] = parsed_args.contact_groups

        payload = {"services": [data]}
        headers = {'content-type': 'application/json'}

        res = self.app.restapi.patch(self.app.options.shinken_url + "/v1/services" + "/" + parsed_args._id,
                                      json=payload)

        print "Service with ID: " + parsed_args.id + " was successfully updated!"
        return util.list_table([i for i in res if "200" in i],self.columns)
class CreateGenericService(ShowOne):
    """Create a new generic host.

    name                            generic-service         ; The 'name' of this service template
    active_checks_enabled           1                       ; Active service checks are enabled
    passive_checks_enabled          1                       ; Passive service checks are enabled/accepted
    parallelize_check               1                       ; Active service checks should be parallelized (disabling this can lead to major performance problems)
    obsess_over_service             1                       ; We should obsess over this service (if necessary)
    check_freshness                 0                       ; Default is to NOT check service 'freshness'
    notifications_enabled           1                       ; Service notifications are enabled
    event_handler_enabled           1                       ; Service event handler is enabled
    flap_detection_enabled          1                       ; Flap detection is enabled
    failure_prediction_enabled      1                       ; Failure prediction is enabled
    process_perf_data               1                       ; Process performance data
    retain_status_information       1                       ; Retain status information across program restarts
    retain_nonstatus_information    1                       ; Retain non-status information across program restarts
    is_volatile                     0                       ; The service is not volatile
    check_period                    24x7                    ; The service can be checked at any time of the day
    max_check_attempts              3                       ; Re-check the service up to 3 times in order to determine its final (hard) state
    check_interval                  5                       ; Check the service every 10 minutes under normal conditions
    retry_interval                  2                       ; Re-check the service every two minutes until a hard state can be determined
    contact_groups                  admins,event_publisher  ; Notifications get sent out to everyone in the 'admins' group
    notification_options            w,u,c,r                 ; Send notifications about warning, unknown, critical, and recovery events
    notification_interval           60                      ; Re-notify about service problems every hour
    notification_period             24x7                    ; Notifications can be sent out at any time
    register                        0                      ; DONT REGISTER THIS DEFINITION - ITS NOT A REAL SERVICE, JUST A TEMPLATE!


    """
    log = logging.getLogger(__name__ + '.CreateGenericHost')
    columns = ["_id", "name", "active_checks_enabled", "passive_checks_enabled", "parallelize_check",
               "obsess_over_service", "check_freshness", "notifications_enabled", "event_handler_enabled",
               "flap_detection_enabled", "failure_prediction_enabled", "process_perf_data", "retain_status_information",
               "retain_nonstatus_information", "is_volatile", "check_period", "max_check_attempts",
               "check_interval", "retry_interval", "contact_groups", "notification_options", "notification_interval",
               "notification_period", "register"]


    def get_parser(self, prog_name):
        parser = super(CreateGenericService, self).get_parser(prog_name)
        #region options
        parser.add_argument(
            'name',
            metavar='<template name>',
            help='Name of generic service template')
        parser.add_argument(
            '--active_checks_enabled',
            metavar='<1|0>',
            default='1',
            help='Active service checks are enabled [default: 1]')
        parser.add_argument(
            '--passive_checks_enabled',
            metavar='<1|0>',
            default='1',
            help='Passive service checks are enabled/accepted [default: 1]')
        parser.add_argument(
            '--parallelize_check',
            metavar='<1|0>',
            default='1',
            help='Active service checks should be parallelized (disabling this can lead to major performance problems) [default: 1]')
        parser.add_argument(
            '--obsess_over_service',
            metavar='<1|0>',
            default='1',
            help='We should obsess over this service (if necessary) [default: 1]')
        parser.add_argument(
            '--check_freshness',
            metavar='<1|0>',
            default='0',
            help='Default is to NOT check service "freshness" [default: 0]')
        parser.add_argument(
            '--notifications_enabled',
            metavar='<1|0>',
            default='1',
            help='Service notifications are enabled [default: 1]')
        parser.add_argument(
            '--event_handler_enabled',
            metavar='<1|0>',
            default='1',
            help='Service event handler is enabled [default: 1]')
        parser.add_argument(
            '--flap_detection_enabled',
            metavar='<1|0>',
            default='1',
            help='Flap detection is enabled [default: 1]')
        parser.add_argument(
            '--failure_prediction_enabled',
            metavar='<1|0>',
            default='1',
            help='Failure prediction is enabled [default: 1]')
        parser.add_argument(
            '--process_perf_data',
            metavar='<1|0>',
            default='1',
            help='Process performance data [default: 1]')
        parser.add_argument(
            '--retain_status_information',
            metavar='<1|0>',
            default='1',
            help='Retain status information across program restarts [default: 1]')
        parser.add_argument(
            '--retain_nonstatus_information',
            metavar='<1|0>',
            default='1',
            help='Retain nonstatus information across program restarts [default: 1]')
        parser.add_argument(
            '--is_volatile',
            metavar='<1|0>',
            default='0',
            help='The service is not volatile [default: 0]')
        parser.add_argument(
            '--check_period',
            metavar='<period>',
            default='24x7',
            help='The service can be checked at any time of the day [default: 24x7]')
        parser.add_argument(
            '--max_check_attempts',
            metavar='<attempts>',
            default='3',
            help='Re-check the service up to 3 times in order to determine its final (hard) state [default: 3]')
        parser.add_argument(
            '--check_interval',
            metavar='<interval>',
            default='5',
            help='Check the service every x minutes under normal conditions [default: 5]')
        parser.add_argument(
            '--retry_interval',
            metavar='<interval>',
            default='2',
            help='Re-check the service every x minutes until a hard state can be determined [default: 2]')
        parser.add_argument(
            '--contact_groups',
            metavar='<groups>',
            default='admins',
            help='Notifications get sent out to everyone in the "admins" group [default: admins]'
                 'comma seperate for multiple values')
        parser.add_argument(
            '--notification_options',
            metavar='<options>',
            default='w,u,c,r',
            help='Send notifications about warning, unknown, critical, and recovery events [default: "w,u,c,r"]')
        parser.add_argument(
            '--notification_interval',
            metavar='<interval>',
            default='60',
            help='Re-notify about service problems every x minutes [default: 60]')
        parser.add_argument(
            '--notification_period',
            metavar='<period>',
            default='24x7',
            help='Notifications can be sent out on this period [default: 24x7]')
        #endregion

        return parser


    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        data = {key: getattr(parsed_args, key) for key in self.columns if key not in ("_id", "register")}
        data["register"] = "0"
        payload = json.dumps({"services": [data]})
        headers = {'content-type': 'application/json'}
        res = self.app.restapi.create(self.app.options.shinken_url + "/v1/services",
                                      data=payload,
                                      response_key="services",
                                      headers=headers)

        return util.show_one_table(res, self.columns)


class ListGenericService(Lister):
    """Show a list of generic services.

    """

    log = logging.getLogger(__name__ + ".ListService")
    columns = ["_id", "name", "active_checks_enabled", "passive_checks_enabled", "parallelize_check",
               "obsess_over_service", "check_freshness", "notifications_enabled", "event_handler_enabled",
               "flap_detection_enabled", "failure_prediction_enabled", "process_perf_data", "retain_status_information",
               "retain_nonstatus_information", "is_volatile", "check_period", "max_check_attempts",
               "check_interval", "retry_interval", "contact_groups", "notification_options", "notification_interval",
               "notification_period", "register"]
    def take_action(self, parsed_args):
        res = self.app.restapi.list(self.app.options.shinken_url + "/v1/services",
                                    response_key="services")
        #note: the filter below removes the 'normal' hosts
        return util.list_table([i for i in res if "name" in i], self.columns)
