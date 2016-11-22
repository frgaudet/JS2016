#!/bin/bash
set -x
ID="6344e108-9ca0-41d3-acc7-0a70d9b3a838"
ceilometer sample-list	--meter cpu_util \
			--query "resource_id=$ID;timestamp>2016-11-11T23:00:00;timestamp<=2016-11-11T23:59:59"
