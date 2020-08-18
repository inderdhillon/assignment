# assignment

This repository contains solution for assignment tasks as described in assignment.txt file.

1. TEST1:
Solution for TEST1 is present in TEST1 directory

First part of solution for TEST1 is implemented in healthcheck.py script. This script monitors apache2, rabbitMQ and postgreSQL processes running on same Linux VM (Ubuntu OS).

It has two key functions:

check_status()
This function checks status of apache2, postgresql and rabbitmq-server processes to capture whether processes are "UP" or "DOWN".

generate_json()
This function reads the current status of each process and creates a json object in below format with name{serviceName}-status-{@timestamp}.json

{ 
   "service_name":"apache2",
   "service_status":"UP",
   "host_name":"host1"
}

Example of generated files are placed under files/*json. 

apache2-status-20200818-012430.json
postgresql-status-20200818-012430.json
rabbitmq-server-status-20200818-012430.json

1.1. Write a simple Python REST webservice that: 

NOTES:
        Accepts the above created JSON file and writes it to Elasticsearch 
        Provide a second endpoint where the data can be retrieved, i.e 

POST /add  à Insert payload into Elasticsearch

GET /health_check à Return the Application status (“UP” or “DOWN”)

Sample calls

https://myservice.rbc.com/add

https://myservice.rbc.com/health_check



2. TEST2
Solution for TEST2 is present in TEST2 directory.

Below is directory structure of TEST2

inventory.ini               # inventory file for three servers (apache2, rabbitmq and postgresql servers)
                            # This file also contains common variables
                          
assignment.yml              # main playbook file for assignment

roles/                      # Contains four roles: apache, postgresql, rabbitmq and common
  apache/                   # this directory represents a apache "role"
     tasks/                 #
         main.yml           # <-- main tasks file includes two files verify_install.yml and check_disk.yml
         verify_install.yml #     This file contains tasks to verify packages, services required for apache
     vars/                  #
         main.yml           # <-- variables associated with this role
         
  postgresql/               # this directory represents a postgresql "role"
     tasks/                 #
         main.yml           # <-- main tasks file includes two files verify_install.yml and check_disk.yml
         verify_install.yml #     This file contains tasks to verify packages, services required for apache
     vars/                  #
         main.yml           # <-- variables associated with this role

  rabbitmq/                 # this directory represents a rabbitmq "role"
     tasks/                 #
         main.yml           # <-- main tasks file includes two files verify_install.yml and check_disk.yml
         verify_install.yml #     This file contains tasks to verify packages, services required for apache
     vars/                  #
         main.yml           #  <-- variables associated with this role 
  
  common/                   # this directory represents a common "role"
     tasks/                 #
         main.yml           # <-- main tasks file includes two files verify_install.yml and check_disk.yml
         check_disk.yml     #     This file contains tasks to check application status
         check_disk.yml     #     This file contains tasks to check disk space on all mounted volumes
     vars/                  #
         main.yml           #  <-- variables associated with this role          
    

Sample run:
ansible-playbook assignment.yml -I inventory -e action=verify_install 
#This is to verify if service packages are installed.

ansible-playbook assignment.yml -i inventory.ini -e action=check_status
#This is to check application status. Please update healthcheck service url

ansible-playbook assignment.yml -i inventory.ini -e action=check_disk
#This is to check disk space on all servers and sends email if disk utilization exceeds 80%.

Sample email Alert:
Subject: ALERT:- Low Disk Space on XXXXXXX
Body: Ansible Disk-report :- Please clean up disk space on system XXXXX

Validation Checks:
  NOTE: This playbook requires 'action' variable to be set, it will exit out if its not defined.

1. You'll receive below message if 'action' variable is not defined during playbook run
   msg="Exiting. this play requires 'action' to be defined"

2. You'll receive below message if 'action' is not chosen from one of these values: ['verify_install', 'check_status', 'check_disk']
   msg="Exiting. Please use valid option for 'action', choose from 'verify_install', 'check_status' or 'check_disk'"
      when: action not in ['verify_install', 'check_status', 'check_disk']