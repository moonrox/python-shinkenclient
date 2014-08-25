#!/bin/bash

opencloud-mon host create prdegocicc01.icloud.intel.com 10.64.131.10 --alias prdegocicc01 --hostgroups os-controller-servers --hostgroups linux-servers --hostgroups os-functional-test-server --use generic-host
opencloud-mon host create prdegocicc02.icloud.intel.com 10.64.131.11 --alias prdegocicc02 --hostgroups os-controller-servers --hostgroups linux-servers --use generic-host
opencloud-mon host create prdegocicc03.icloud.intel.com 10.64.131.12 --alias prdegocicc03 --hostgroups os-controller-servers --hostgroups linux-servers --use generic-host
opencloud-mon host create prdegocivc01.icloud.intel.com 10.64.131.13 --alias qafm7ocivc01 --hostgroups os-proxy-compute-servers --hostgroups linux-servers --use generic-host
opencloud-mon host create egs02vcaigbn001.amr.corp.intel.com 10.9.225.252 --alias egs02vcaigbn001 --hostgroups os-virtualcenter-servers --use generic-host
opencloud-mon host create eg2services01.amr.corp.intel.com 10.64.152.11 --alias eg2services01 --hostgroups os-ttm-servers --hostgroups linux-servers --hostgroups os-ism-servers --use generic-host
opencloud-mon host create eg2services02.amr.corp.intel.com 10.64.152.25 --alias eg2services02 --hostgroups linux-servers --use generic-host
opencloud-mon host create eg2mon01.amr.corp.intel.com 10.64.152.12 --alias eg2mon01 --hostgroups linux-servers --use generic-host
opencloud-mon host create prdegint-horizon.icloud.intel.com 10.64.138.62 --alias prdegint-horizon --hostgroups os-haproxy-servers --use generic-host
opencloud-mon host create eg2lbservices01.amr.corp.intel.com 10.64.152.14 --alias eg2lbservices01 --hostgroups linux-servers --use generic-host
opencloud-mon host create eg2lbservices02.amr.corp.intel.com 10.64.152.25 --alias eg2lbservices02 --hostgroups linux-servers --use generic-host
opencloud-mon host create eg2services.amr.corp.intel.com 10.64.152.96 --alias eg2services --hostgroups os-services-haproxy-servers --use generic-host
