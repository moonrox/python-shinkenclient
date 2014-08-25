#!/bin/bash

# Contact Groups

opencloud-mon contactgroup create paas-contacts 
opencloud-mon contactgroup create bower-contacts

# Contacts

opencloud-mon contact create Aaron --email aaron.m.huber@intel.com --contact-group paas-contacts --use generic-contact
opencloud-mon contact create Jon --email jon.price@intel.com --contact-group paas-contacts --use generic-contact

opencloud-mon contact create Brandon --email Brandon.bohling@intel.com --contact-group bower-contacts --use generic-contact

# Host Groups

opencloud-mon hostgroup create paas-api-servers
opencloud-mon hostgroup create paas-cf-servers
opencloud-mon hostgroup create paas-bowerregistry

# Commands

opencloud-mon command create check_paas_api --command-line '$USER1$/check_http -t 30 -N -H $HOSTNAME$ -u /v2/info'
opencloud-mon command create check_users --command-line '$USER1$/check_nrpe -H $HOSTADDRESS$ -c check_users'
opencloud-mon command create check_disk --command-line '$USER1$/check_nrpe -H $HOSTADDRESS$ -c check_disk'
opencloud-mon command create check_total_procs --command-line '$USER1$/check_nrpe -H $HOSTADDRESS$ -c check_total_procs'
opencloud-mon command create check_io_que --command-line '$USER1$/check_nrpe -H $HOSTADDRESS$ -c check_io_que'
opencloud-mon command create check_paas_services --command-line '$USER1$/check_nrpe -H $HOSTADDRESS$ -c check_paas_services'
opencloud-mon command create check_mem --command-line '$USER1$/check_nrpe -H $HOSTADDRESS$ -c check_mem'

opencloud-mon command create check_paas_bower --command-line '$USER1$/check_http -t 30 -N -H $HOSTNAME$ -u /packages'

# Services

opencloud-mon service create '!localhost' --service-description "Check PaaS API" --check-command 'check_paas_api' --hostgroup-name paas-api-servers --use generic-service
opencloud-mon service create '!localhost' --service-description "Check Paas Bower Registry" --check-command 'check_paas_bower' --hostgroup-name paas-bowerregistry --use generic-service

opencloud-mon service create '!localhost' --service-description "Check Users" --check-command 'check_users' --hostgroup-name paas-cf-servers --use generic-service
opencloud-mon service create '!localhost' --service-description "Check Load" --check-command 'check_load' --hostgroup-name paas-cf-servers --use generic-service
opencloud-mon service create '!localhost' --service-description "Check Disk /dev/vda1" --check-command 'check_disk' --hostgroup-name paas-cf-servers --use generic-service
opencloud-mon service create '!localhost' --service-description "Check Zombie Processes" --check-command 'check_zombie_procs' --hostgroup-name paas-cf-servers --use generic-service
opencloud-mon service create '!localhost' --service-description "Check Total Processes" --check-command 'check_total_procs' --hostgroup-name paas-cf-servers --use generic-service
opencloud-mon service create '!localhost' --service-description "Check IO Queue" --check-command 'check_io_que' --hostgroup-name paas-cf-servers --use generic-service
opencloud-mon service create '!localhost' --service-description "Check CF Services" --check-command 'check_paas_services' --hostgroup-name paas-cf-servers --use generic-service
opencloud-mon service create '!localhost' --service-description "Check Memory" --check-command 'check_mem' --hostgroup-name paas-cf-servers --use generic-service

# Hosts

opencloud-mon host create api.paas1.icloud.intel.com 10.64.12.13 --alias api.paas1 --hostgroups paas-api-servers --contacts Jon --contacts Aaron --use generic-host
opencloud-mon host create gorgon-float9.icloud.intel.com 10.9.177.23 --alias microbosh --hostgroups paas-cf-servers --contacts Jon --contacts Aaron --use generic-host
opencloud-mon host create bowerregistry.paas1.icloud.intel.com 10.64.12.13 --alias bowerregistry --hostgroups paas-api-servers --contacts Brandon --use generic-host

# Reload

opencloud-mon reload
