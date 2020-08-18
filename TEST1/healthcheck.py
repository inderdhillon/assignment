import json
import datetime
import subprocess
import socket

services = ["apache2", "rabbitmq-server", "postgresql"]
host=socket.gethostname()

def check_status (service):
    p=subprocess.Popen(["systemctl", "is-active",  service], stdout=subprocess.PIPE) 
    (output, err) = p.communicate()
    output = output.decode('utf-8')
    if output.rstrip() == 'active':
        status = "UP"
    else: 
        status = "DOWN"
    return status

def generate_json (service):
    status_json = {
      "service_name": service,
      "service_status": check_status(service),
      "host_name": host,
    }

    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    file_name="{0}-status-{1}.json".format(service,ts)
    print(file_name)
    f = open("files/" + file_name, "w")
    f.write(json.dumps(status_json, indent=4))
    f.close() 

for service in services:
    generate_json(service)
