import logging
import json
from shinkenclient.common import util

from cliff.lister import Lister
from cliff.show import ShowOne

headers = {'content-type': 'application/json'}

class ListContact(Lister):
    """Show a list of contact groups.

    """

    log = logging.getLogger(__name__ + ".ListContact")

    def take_action(self, parsed_args):
        columns = ["_id", "contact_name", "host_notifications_enabled", "service_notifications_enabled", "use", "email","contactgroups"]
        res = self.app.restapi.list(self.app.options.shinken_url + "/v1/contacts",
                                    response_key="contacts")
        #note: the filter below removes the generic contact
        return util.list_table([i for i in res if "contact_name" in i], columns)

class CreateContact(ShowOne):
    """Create a new contact group.

    """
    log = logging.getLogger(__name__ + '.CreateContact')

    def get_parser(self, prog_name):
        parser = super(CreateContact, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<contact name>',
            help='Name of contact')
        parser.add_argument(
            '--alias',
            metavar='<alias>',
            help='alias')
        parser.add_argument(
            '--email',
            metavar='<email>',
            help='email address')
        parser.add_argument(
            '--use',
            default="generic-contact",
            metavar='<contact name>',
            help='inherit properties from this contact [default: generic-contact]')
        parser.add_argument(
            '--contact-group',
            metavar='<contact group>',
            action='append',
            default=[],
            help='Name of contact group'
                 ' (repeat for multiple contact groups)')
        parser.add_argument(
            '--host_notifications_enabled',
            metavar='<1|0>',
            default='1',
            help='are host notifications enabled')
        parser.add_argument(
            '--service_notifications_enabled',
            metavar='<1|0>',
            default='1',
            help='are service notifications enabled')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        columns = ["_id", "contact_name", "host_notifications_enabled", "service_notifications_enabled", "use", "email"]
        data = {"contact_name": parsed_args.name,
                "host_notifications_enabled": parsed_args.host_notifications_enabled,
                "service_notifications_enabled": parsed_args.service_notifications_enabled}
        if parsed_args.alias:
            data["alias"] = parsed_args.alias
        if parsed_args.email:
            data["email"] = parsed_args.email
        if parsed_args.use:
            data["use"] = parsed_args.use
        if parsed_args.contact_group:
            data["contactgroups"] = " ,".join(parsed_args.contact_group)

        payload = json.dumps({"contacts": [data]})
        headers = {'content-type': 'application/json'}
        res = self.app.restapi.create(self.app.options.shinken_url + "/v1/contacts", data=payload, response_key="contacts", headers=headers)

        return util.show_one_table(res, columns)

class DeleteContact(Lister):
    log = logging.getLogger(__name__ + ".DeleteContact")
    columns = ["_id", "contact_name", "host_notifications_enabled", "service_notifications_enabled", "use", "email","contactgroups"]
    def get_parser(self, prog_name):
        parser = super(DeleteContact, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar='<id>',
            help='id of contact to be deleted')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        res = self.app.restapi.delete(self.app.options.shinken_url + "/v1/contacts/" + parsed_args.id)
        print "Contact with ID: " + parsed_args.id + " was successfully deleted!"
        return util.list_table([i for i in res if "200" in i],self.columns)

class UpdateContact(Lister):
    """Update an existing contact.

    """
    log = logging.getLogger(__name__ + '.UpdateContact')
    columns = ["_id", "contact_name", "contactgroups" ,"host_notifications_enabled", "service_notifications_enabled", "use", "email"]

    def get_parser(self, prog_name):
        parser = super(UpdateContact, self).get_parser(prog_name)
        parser.add_argument(
            '_id',
            metavar='<_id>',
            help='_id of the contact to be updated')
        parser.add_argument(
            '--name',
            metavar='<contact name>',
            help='Name of contact')
        parser.add_argument(
            '--alias',
            metavar='<alias>',
            help='alias')
        parser.add_argument(
            '--email',
            metavar='<email>',
            help='email address')
        parser.add_argument(
            '--use',
            default="generic-contact",
            metavar='<contact name>',
            help='inherit properties from this contact [default: generic-contact]')
        parser.add_argument(
            '--contact-group',
            metavar='<contact group>',
            action='append',
            default=[],
            help='Name of contact group'
                 ' (repeat for multiple contact groups)')
        parser.add_argument(
            '--host_notifications_enabled',
            metavar='host_notifications_enabled',
            help='are host notifications enabled')
        parser.add_argument(
            '--service_notifications_enabled',
            metavar='service_notifications_enabled',
            help='are service notifications enabled')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        data = {}
        if parsed_args._id:
            parsed_args._id = parsed_args._id
        if parsed_args.contact_group:
            data["contactgroups"] = " ,".join(parsed_args.contact_group)
        if parsed_args.alias:
            data["alias"] = parsed_args.alias
        if parsed_args.name:
            data["contact_name"] = parsed_args.name
        if parsed_args.email:
            data["email"] = parsed_args.email
        if parsed_args.use:
            data["use"] = parsed_args.use
        if parsed_args.service_notifications_enabled:
            data["service_notifications_enabled"] = parsed_args.service_notifications_enabled
        if parsed_args.host_notifications_enabled:
            data["host_notifications_enabled"] = parsed_args.host_notifications_enabled

        payload = {"contacts": [data]}
        headers = {'content-type': 'application/json'}
        res = self.app.restapi.patch(self.app.options.shinken_url + "/v1/contacts" + "/" + parsed_args._id,
                                      json=payload)

        print "Contact: " + parsed_args.name + " with ID: " + parsed_args._id + " was successfully updated!"
        return util.list_table([i for i in res if "200" in i],self.columns)
class CreateGenericContact(ShowOne):
    """Create a generic contact group.

         name                            generic-contact         ; The name of this contact template
         service_notification_period     24x7                    ; service notifications can be sent anytime
         host_notification_period        24x7                    ; host notifications can be sent anytime
         service_notification_options    w,u,c,r,f,s             ; send notifications for all service states, flapping events, and scheduled downtime events
         host_notification_options       d,u,r,f,s               ; send notifications for all host states, flapping events, and scheduled downtime events
         service_notification_commands   notify-service-by-email ; send service notifications via email
         host_notification_commands      notify-host-by-email    ; send host notifications via email
    """
    log = logging.getLogger(__name__ + '.CreateGenericContact')
    columns = ["_id", "name", "service_notification_period", "host_notification_period",
                   "service_notification_options", "host_notification_options", "service_notification_commands",
                   "host_notification_commands", "register"]

    def get_parser(self, prog_name):
        parser = super(CreateGenericContact, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<template name>',
            help='Name of generic contact template')
        parser.add_argument(
            '--service_notification_period',
            metavar='<service notification period>',
            default='24x7',
            help='Service notifications can be sent anytime [default: 24x7]')
        parser.add_argument(
            '--host_notification_period',
            metavar='<host notification period>',
            default='24x7',
            help='Host notifications can be sent anytime [default: 24x7]')
        parser.add_argument(
            '--service_notification_options',
            metavar='<service notification options>',
            default='w,u,c,r,f,s',
            help='Service notifications options [default: "w,u,c,r,f,s"]')
        parser.add_argument(
            '--host_notification_options',
            metavar='<host notification options>',
            default='d,u,r,f,s',
            help='Host notifications options [default: "d,u,r,f,s"]')
        parser.add_argument(
            '--service_notification_commands',
            metavar='<service notification command>',
            default='notify-service-by-email',
            help='Service notification command [default: "notify-service-by-email"]')
        parser.add_argument(
            '--host_notification_commands',
            metavar='<host notification command>',
            default='notify-host-by-email',
            help='Host notification command [default: "notify-host-by-email"]')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        data = {key: getattr(parsed_args, key) for key in self.columns if key not in ("_id", "register")}
        data["register"] = "0"
        payload = json.dumps({"contacts": [data]})
        headers = {'content-type': 'application/json'}
        res = self.app.restapi.create(self.app.options.shinken_url + "/v1/contacts", data=payload, response_key="contacts", headers=headers)

        return util.show_one_table(res, self.columns)

class DeleteContactGroup(Lister):
    log = logging.getLogger(__name__ + ".DeleteContactGroup")
    columns = ["_id", "contactgroup_name", "alias" ]
    def get_parser(self, prog_name):
        parser = super(DeleteContactGroup, self).get_parser(prog_name)
        parser.add_argument(
            'id',
            metavar='<id>',
            help='id of contactgroup to be deleted')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        res = self.app.restapi.delete(self.app.options.shinken_url + "/v1/contactgroups/" + parsed_args.id)
        print "ContactGroup with ID: " + parsed_args.id + " was successfully deleted!"
        return util.list_table([i for i in res if "200" in i],self.columns)

class ListGenericContact(Lister):
    """Show a list of generic contact groups.

    """

    log = logging.getLogger(__name__ + ".ListContact")

    def take_action(self, parsed_args):
        columns = ["_id", "name", "service_notification_period", "host_notification_period",
                   "service_notification_options", "host_notification_options", "service_notification_commands",
                   "host_notification_commands", "register"]
        res = self.app.restapi.list(self.app.options.shinken_url + "/v1/contacts",
                                    response_key="contacts")
        #note: the filter below removes the generic contact
        return util.list_table([i for i in res if "name" in i], columns)


class CreateContactGroup(ShowOne):
    """Create a new contactgroup.

    """
    log = logging.getLogger(__name__ + '.CreateContactGroup')
    columns = ["_id", "contactgroup_name", "alias" ]

    def get_parser(self, prog_name):
        parser = super(CreateContactGroup, self).get_parser(prog_name)
        parser.add_argument(
            'name',
            metavar='<contactgroup name>',
            help='Name of contactgroup')
        parser.add_argument(
            '--alias',
            metavar='<alias>',
            help='Alias for this contactgroup')
        return parser

    def take_action(self, parsed_args):
        self.log.debug('take_action(%s)', parsed_args)
        data = {"contactgroup_name": parsed_args.name}
        if parsed_args.alias:
            data["alias"] = parsed_args.alias

        payload = json.dumps({"contactgroups": [data]})
        headers = {'content-type': 'application/json'}
        res = self.app.restapi.create(self.app.options.shinken_url + "/v1/contactgroups",
                                      data=payload,
                                      response_key="contactgroups",
                                      headers=headers)

        return util.show_one_table(res, self.columns)


class ListContactGroup(Lister):
    """Show a list of contactgroups.

    """

    log = logging.getLogger(__name__ + ".ListContactGroup")
    columns = ["_id", "contactgroup_name", "alias"]

    def take_action(self, parsed_args):
        res = self.app.restapi.list(self.app.options.shinken_url + "/v1/contactgroups",
                                    response_key="contactgroups")
        return util.list_table(res, self.columns)
