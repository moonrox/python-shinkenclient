#!/bin/bash

# these are the hostgroups used for compute hosts in fm1
opencloud-mon hostgroup create os-compute-node-servers
opencloud-mon hostgroup create os-servers
opencloud-mon hostgroup create collectd-servers
opencloud-mon hostgroup create linux-servers
opencloud-mon hostgroup create linux-physical-servers
opencloud-mon hostgroup create mysql-compute-node-servers
opencloud-mon hostgroup create os-controller-servers
opencloud-mon hostgroup create os-proxy-compute-servers
opencloud-mon hostgroup create os-virtualcenter-servers
opencloud-mon hostgroup create os-ttm-servers
opencloud-mon hostgroup create os-haproxy-servers
opencloud-mon hostgroup create os-services-haproxy-servers
opencloud-mon hostgroup create os-functional-test-server
opencloud-mon hostgroup create os-ism-servers

#commands for controllers
opencloud-mon command create check_keystone --command-line '$USER1$/check_keystone --auth_url $_HOSTOC_AUTH_URL$ --username $_HOSTOC_ADMIN_USERNAME$ --tenant $_HOSTOC_ADMIN_TENANT_NAME$ --password $_HOSTOC_ADMIN_PASSWORD$'
opencloud-mon command create check_glance_api --command-line '$USER1$/check_glance_api.py --auth_url $_HOSTOC_AUTH_URL$ --username $_HOSTOC_ADMIN_USERNAME$ --tenant $_HOSTOC_ADMIN_TENANT_NAME$ --password $_HOSTOC_ADMIN_PASSWORD$ --req_count 1'
opencloud-mon command create check_port_nova_rabbitmq --command-line '$USER1$/check_tcp -H $HOSTADDRESS$ -p 5673'
opencloud-mon command create check_port_keystone-service --command-line '$USER1$/check_tcp -H $HOSTADDRESS$ -p 5000'
opencloud-mon command create check_port_keystone-admin-service --command-line '$USER1$/check_tcp -H $HOSTADDRESS$ -p 35357'
opencloud-mon command create check_port_glance-api --command-line '$USER1$/check_tcp -H $HOSTADDRESS$ -p 9292'
opencloud-mon command create check_port_glance-registry --command-line '$USER1$/check_tcp -H $HOSTADDRESS$ -p 9191'
opencloud-mon command create check_nova_scheduler --command-line '$USER1$/check_nrpe -H $HOSTADDRESS$ -c check_nova_scheduler'
opencloud-mon command create check_nova_vncproxy --command-line '$USER1$/check_nrpe -H $HOSTADDRESS$ -c check_nova_vncproxy'
opencloud-mon command create check_nova_api --command-line '$USER1$/check_nrpe -H $HOSTADDRESS$ -c check_nova_api'
opencloud-mon command create check_nova_conductor --command-line '$USER1$/check_nrpe -H $HOSTADDRESS$ -c check_nova_conductor'
opencloud-mon command create check_nova_consoleauth --command-line '$USER$/check_nrpe -H $HOSTADDRESS$ -c check_nova_consoleauth'
opencloud-mon command create check_cinder-api --command-line '$USER1$/check_nrpe -H $HOSTADDRESS$ -c check_cinder-api -t 30'
opencloud-mon command create check_cinder-scheduler --command-line '$USER1$/check_nrpe -H $HOSTADDRESS$ -c check_cinder-scheduler -t 30'
opencloud-mon command create check_cinder-volume --command-line '$USER1$/check_nrpe -H $HOSTADDRESS$ -c check_cinder-volume -t 30'
opencloud-mon command create check_quantum_metadata --command-line '$USER1$/check_nrpe -H $HOSTADDRESS$ -c check_quantum_metadata'

# commands for linux-servers
opencloud-mon command create check_all_disks --command-line '$USER1$/check_nrpe -H $HOSTADDRESS$ -c check_all_disks'
opencloud-mon command create check_load --command-line '$USER1$/check_nrpe -H $HOSTADDRESS$ -c check_load'
opencloud-mon command create check_swap --command-line '$USER1$/check_nrpe -H $HOSTADDRESS$ -c check_swap'
opencloud-mon command create check_zombie_procs --command-line '$USER1$/check_nrpe -H $HOSTADDRESS$ -c check_zombie_procs'

# commands for virtualcenter servers
opencloud-mon command create check_vc_dc_cpu_util --command-line '$USER1$/check_vmware_api.pl -D $HOSTADDRESS$ -u $_HOSTVC_USERNAME$ -p $_HOSTVC_PASSWORD$ -l cpu -s usage -S /tmp/check_vmware_session -w ~:80 -c ~:90 -t 120'
opencloud-mon command create check_vc_dc_mem_util --command-line '$USER1$/check_vmware_api.pl -D $HOSTADDRESS$ -u $_HOSTVC_USERNAME$ -p $_HOSTVC_PASSWORD$ -l mem -s usage -S /tmp/check_vmware_session -w ~:80 -c ~:90 -t 120'
opencloud-mon command create check_vc_dc_io --command-line '$USER1$/check_vmware_api.pl -D $HOSTADDRESS$ -u $_HOSTVC_USERNAME$ -p $_HOSTVC_PASSWORD$ -l io -S /tmp/check_vmware_session -t 120'
opencloud-mon command create check_vc_dc_storage --command-line '$USER1$/check_vmware_api.pl -D $HOSTADDRESS$ -u $_HOSTVC_USERNAME$ -p $_HOSTVC_PASSWORD$ -l vmfs -o blacklistregexp -x local -S /tmp/check_vmware_session -t 120'
opencloud-mon command create check_vc_dc_status --command-line '$USER1$/check_vmware_api.pl -D $HOSTADDRESS$ -u $_HOSTVC_USERNAME$ -p $_HOSTVC_PASSWORD$ -l runtime -S /tmp/check_vmware_session -t 120'

# commands for proxy compute servers (vmware)
opencloud-mon command create check_proxy_compute --command-line '$USER1$/check_nrpe -H $HOSTADDRESS$ -c check_proxy_compute'

# functional openstack checks
opencloud-mon command create check_bootstrap_timeouts --command-line '$USER1$/check_bootstrap_timeouts.py --ttm-host $_HOSTOC_SERVICES$'
opencloud-mon command create check_nova-instance --command-line '$USER1$/cache_check.py -c "$USER1$/check_nova-instance.py --auth_url $_HOSTOC_AUTH_URL$ --username $_HOSTOC_MON_USERNAME$ --tenant $_HOSTOC_MON_TENANT_NAME$ --password $_HOSTOC_MON_PASSWORD$ --insecure --image_name=$_HOSTOC_MON_IMAGE_NAME$ --flavor_name=$_HOSTOC_MON_FLAVOR_NAME$ --network_id $_HOSTOC_MON_NETWORK_ID$" -e 1920 -d -t 185 -i 1680'
opencloud-mon command create check_cinder-volume-instance --command-line '$USER1$/check_cinder-volume.py --auth_url $_HOSTOC_AUTH_URL$ --username $_HOSTOC_MON_USERNAME$ --tenant $_HOSTOC_MON_TENANT_NAME$ --password $_HOSTOC_MON_PASSWORD$ --insecure'
opencloud-mon command create check_nova-service-list --command-line '$USER1$/check_nova-service-list.sh -H $_HOSTOC_AUTH_URL$ -T $_HOSTOC_ADMIN_TENANT_NAME$ -U $_HOSTOC_ADMIN_USERNAME$ -P $_HOSTOC_ADMIN_PASSWORD$'
opencloud-mon command create check_nova_vmware --command-line '$USER1$/check_nova_vmware.py --vc_host $_HOSTVC_HOST$ --vc_username $_HOSTVC_USERNAME$ --vc_password $_HOSTVC_PASSWORD$ --username $_HOSTOC_ADMIN_USERNAME$ --password $_HOSTOC_ADMIN_PASSWORD$ --auth_url $_HOSTOC_AUTH_URL$ --tenant $_HOSTOC_ADMIN_TENANT_NAME$  --insecure'

# commands for ttm servers
opencloud-mon command create check_ttm_api --command-line '$USER1$/check_nrpe -H $HOSTADDRESS$ -c check_ttm_api'
opencloud-mon command create check_ttm --command-line '$USER1$/check_nrpe -H $HOSTADDRESS$ -c check_ttm'

# commands for os-haproxy-servers
opencloud-mon command create check_haproxy --command-line '$USER1$/check_haproxy.rb -u "http://$HOSTADDRESS$/haproxy?stats;csv" -e horizon'

# commands for services haproxy
opencloud-mon command create check_services_haproxy --command-line '$USER1$/check_haproxy.rb -u "http://$HOSTADDRESS$/haproxy?stats;csv" -U admin -P admin'

# commands for ISM
opencloud-mon command create check_ism --command-line '$USER1$/check_nrpe -H $HOSTADDRESS$ -c check_ism'
opencloud-mon command create check_dtw --command-line '$USER1$/check_nrpe -H $HOSTADDRESS$ -c check_dtw'

# services for os-ism-servers
opencloud-mon service create '!localhost' --service-description "Check ISM worker" --check-command 'check_ism' --hostgroup-name os-ism-servers --use generic-service
opencloud-mon service create '!localhost' --service-description "Check DTW worker" --check-command 'check_dtw' --hostgroup-name os-ism-servers --use generic-service

# services for os-haproxy-servers
opencloud-mon service create '!localhost' --service-description "Check haproxy" --check-command 'check_haproxy' --hostgroup-name os-haproxy-servers --use generic-service

# services for services haproxy
opencloud-mon service create '!localhost' --service-description "Check haproxy" --check-command 'check_services_haproxy' --hostgroup-name os-services-haproxy-servers --use generic-service


# services for os-ttm-servers
#opencloud-mon service create '!localhost' --service-description "Check ttm api" --check-command 'check_ttm_api' --hostgroup-name os-ttm-servers --use generic-service
opencloud-mon service create '!localhost' --service-description "Check ttm" --check-command 'check_ttm' --hostgroup-name os-ttm-servers --use generic-service

# services for os-virtualcenters-servers
opencloud-mon service create '!localhost' --service-description "Check VC datacenter cpu utilization" --check-command 'check_vc_dc_cpu_util' --hostgroup-name os-virtualcenter-servers --use generic-service
opencloud-mon service create '!localhost' --service-description "Check VC datacenter mem utilization" --check-command 'check_vc_dc_mem_util' --hostgroup-name os-virtualcenter-servers --use generic-service
opencloud-mon service create '!localhost' --service-description "Check VC datacenter io" --check-command 'check_vc_dc_io' --hostgroup-name os-virtualcenter-servers --use generic-service
#opencloud-mon service create '!localhost' --service-description "Check VC datacenter datastore capacity" --check-command 'check_vc_dc_storage' --hostgroup-name os-virtualcenter-servers --use generic-service
opencloud-mon service create '!localhost' --service-description "Check VC health" --check-command 'check_vc_dc_status' --hostgroup-name os-virtualcenter-servers --use generic-service

# openstack functional tests
opencloud-mon service create '!localhost' --service-description "Check nova instance" --check-command 'check_nova-instance' --hostgroup-name 'os-functional-test-server' --use generic-service
opencloud-mon service create '!localhost' --service-description "Check cinder volume instance" --check-command 'check_cinder-volume-instance' --hostgroup-name 'os-functional-test-server' --use generic-service
opencloud-mon service create '!localhost' --service-description "Check nova service list" --check-command 'check_nova-service-list' --hostgroup-name 'os-functional-test-server' --use generic-service
opencloud-mon service create '!localhost' --service-description "Check bootstrap is finishing" --check-command 'check_bootstrap_timeouts' --hostgroup-name 'os-functional-test-server' --use generic-service
opencloud-mon service create '!localhost' --service-description "Check vcenter and nova synch" --check-command 'check_nova_vmware' --hostgroup-name 'os-functional-test-server' --use generic-service


# services for os-controller-servers
opencloud-mon service create '!localhost' --service-description "Check nova conductor" --check-command 'check_nova_conductor' --hostgroup-name os-controller-servers --use generic-service
opencloud-mon service create '!localhost' --service-description "Check nova consoleauth" --check-command 'check_nova_consoleauth' --hostgroup-name os-controller-servers --use generic-service
opencloud-mon service create '!localhost' --service-description "Check keystone" --check-command 'check_keystone' --hostgroup-name os-controller-servers --use generic-service
opencloud-mon service create '!localhost' --service-description "Check glance api" --check-command 'check_glance_api' --hostgroup-name os-controller-servers --use generic-service
opencloud-mon service create '!localhost' --service-description "Port check for nova mq" --check-command 'check_port_nova_rabbitmq' --hostgroup-name os-controller-servers --use generic-service
opencloud-mon service create '!localhost' --service-description "Port check for keystone" --check-command 'check_port_keystone-service' --hostgroup-name os-controller-servers --use generic-service
opencloud-mon service create '!localhost' --service-description "Port check for keystone-admin-service" --check-command 'check_port_keystone-admin-service' --hostgroup-name os-controller-servers --use generic-service
opencloud-mon service create '!localhost' --service-description "Port check for glance-api" --check-command 'check_port_glance-api' --hostgroup-name os-controller-servers --use generic-service
opencloud-mon service create '!localhost' --service-description "Port check for glance-registry" --check-command 'check_port_glance-registry' --hostgroup-name os-controller-servers --use generic-service
opencloud-mon service create '!localhost' --service-description "Check nova scheduler" --check-command 'check_nova_scheduler' --hostgroup-name os-controller-servers --use generic-service
opencloud-mon service create '!localhost' --service-description "Check nova vncproxy" --check-command 'check_nova_vncproxy' --hostgroup-name os-controller-servers --use generic-service
opencloud-mon service create '!localhost' --service-description "Check nova api" --check-command 'check_nova_api' --hostgroup-name os-controller-servers --use generic-service
opencloud-mon service create '!localhost' --service-description "Check cinder api" --check-command 'check_cinder-api' --hostgroup-name os-controller-servers --use generic-service
opencloud-mon service create '!localhost' --service-description "Check cinder scheduler" --check-command 'check_cinder-scheduler' --hostgroup-name os-controller-servers --use generic-service
opencloud-mon service create '!localhost' --service-description "Check cinder volume" --check-command 'check_cinder-volume' --hostgroup-name os-controller-servers --use generic-service
opencloud-mon service create '!localhost' --service-description "Check quantum metadata" --check-command 'check_quantum_metadata' --hostgroup-name os-controller-servers --use generic-service

# services for linux-servers
opencloud-mon service create '!localhost' --service-description "Check disk" --check-command 'check_all_disks' --hostgroup-name linux-servers --use generic-service
opencloud-mon service create '!localhost' --service-description "Check load" --check-command 'check_load' --hostgroup-name linux-servers --use generic-service
opencloud-mon service create '!localhost' --service-description "Check swap" --check-command 'check_swap' --hostgroup-name linux-servers --use generic-service
opencloud-mon service create '!localhost' --service-description "Check for zombies" --check-command 'check_zombie_procs' --hostgroup-name linux-servers --use generic-service

# services for proxy compute servers (vmware)
opencloud-mon service create '!localhost' --service-description "Check nova compute proxy" --check-command 'check_proxy_compute' --hostgroup-name os-proxy-compute-servers --use generic-service


opencloud-mon reload
