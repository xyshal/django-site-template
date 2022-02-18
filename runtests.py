import os
import shutil
import subprocess

image = "site:latest"

# -----------------------------------
# Find the container ID for the image
# -----------------------------------
container = ""
containers = subprocess.check_output(["docker","container", "ls"]).rstrip().decode("UTF-8")
for line in containers.split("\n"):
    if image in line:
        container = line.split(" ")[0]
assert container != ""


# ------------------
# Run a sanity check
# ------------------
requestOutput = "testindex.html"
requestCmd = ""
if (shutil.which("wget") is not None):
  requestCmd = f"wget -O {requestOutput} http://127.0.0.1:8000"
elif (shutil.which("curl") is not None):
  requestCmd = f"curl -o {requestOutput} http://127.0.0.1:8000 --connect-timeout 5"
else:
  # TODO: Use the python requests library in this case?
  raise Exception("Don't know how to make a request")

if (os.path.exists(requestOutput)):
    os.remove(requestOutput)
subprocess.check_call(requestCmd, shell=True)
os.remove(requestOutput)


# ------------------
# Run the unit tests
# ------------------
subprocess.check_call(f"docker exec {container} /bin/bash -c \"cd /var/www && python3 manage.py test\"", shell=True)


# Run the integration tests
# TODO: This takes a long time; should we provide a mechanism to cache this container?
subprocess.check_call(f"docker cp environments/site/install-test-dependencies.sh {container}:/root", shell=True)
subprocess.check_call(f"docker cp environments/site/launch-vnc.sh {container}:/var/www", shell=True)
subprocess.check_call(f"docker exec --user root {container} /bin/bash /root/install-test-dependencies.sh", shell=True)

subprocess.check_call(f"docker exec -d {container} /bin/bash /var/www/launch-vnc.sh", shell=True)
subprocess.check_call(f"docker exec {container} pip3 install selenium", shell=True)

subprocess.check_call(f"docker cp test/integration-test.py {container}:/var/www", shell=True)
subprocess.check_call(f"docker exec {container} /bin/bash -c \"DISPLAY=:0 python3 /var/www/integration-test.py\"", shell=True)

