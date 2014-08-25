# Contact Groups
opencloud-mon contactgroup create dbaas-contacts 

# Contacts
opencloud-mon contact create Tom --email tom.petersen@intel.com --contact-group dbaas-contacts --use generic-contact
opencloud-mon contact create Munir --email munir.ghamrawi@intel.com --contact-group dbaas-contacts --use generic-contact

# Host Groups
opencloud-mon hostgroup create dbaas-mongo-servers
opencloud-mon hostgroup create dbaas-mysql-servers
opencloud-mon hostgroup create dbaas-mongo-vips
opencloud-mon hostgroup create dbaas-mysql-vips

# Commands
opencloud-mon command create check_dbaas_api --command-line '$USER1$/check_http -N -H $HOSTNAME$'

# Services
opencloud-mon service create '!localhost' --service-description "Check DBaaS API" --check-command 'check_dbaas_api' --hostgroup-name dbaas-mongo-vips,dbaas-mysql-vips --use generic-service

# Hosts

# Reload
opencloud-mon reload
