#!/usr/bin/env python
# coding=utf-8
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    <http://www.gnu.org/licenses/>.
#
# F-Gaudet 2016

import os
import ceilometerclient.client 
from novaclient import client
from prettytable import PrettyTable 

allServerCpu = PrettyTable(["uuid","Name","Last CPU_UTIL Sample (%)"])
allServerCpu.align["uuid"] = "l" 
allServerCpu.padding_width = 1

os_username = os.environ.get('OS_USERNAME')
os_password = os.environ.get('OS_PASSWORD')
os_regionname = os.environ.get('OS_REGION_NAME')
os_project_name = os.environ.get('OS_PROJECT_NAME')
os_auth_url = os.environ.get('OS_AUTH_URL')

novaclient = client.Client("2.0",
	os_username,
	os_password, 
	os_project_name, 
	os_auth_url, 
	service_type="compute", 
	region_name=os_regionname)

servers = novaclient.servers.list(detailed=True)

ceilometerclient = ceilometerclient.client.get_client(2, os_username=os_username, 
										os_password=os_password, 
										os_tenant_name=os_project_name, 
										os_auth_url=os_auth_url,
										region_name=os_regionname)

# Print last CPU check for all running server within a project
for server in servers:
    query = [dict(field='resource_id', op='eq', value=server.id)]
    cpu_util = ceilometerclient.samples.list(meter_name='cpu_util', limit=1, q=query)    
    try:
    	allServerCpu.add_row([server.id,server.name,cpu_util[0].counter_volume])
    except:
    	pass
print allServerCpu
