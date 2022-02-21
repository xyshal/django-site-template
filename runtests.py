import os
import shutil
import subprocess

siteImage = "site:latest"

# -----------------------------------
# Find the container ID for the image
# -----------------------------------
container = ""
containers = subprocess.check_output(["docker","container", "ls"]).rstrip().decode("UTF-8")
for line in containers.split("\n"):
    if siteImage in line:
        container = line.split(" ")[0]
assert container != ""


# ------------------
# Run a sanity check
# ------------------
requestOutput = "testindex.html"
requestCmd = ""
if (shutil.which("wget") is not None):
  requestCmd = f"wget -O {requestOutput} http://127.0.0.1"
elif (shutil.which("curl") is not None):
  requestCmd = f"curl -o {requestOutput} http://127.0.0.1 --connect-timeout 5"
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


# -------------------------
# Run the integration tests
# -------------------------
testImage = "example-test:latest"
subprocess.check_call(f"docker build environments/test -t {testImage}", shell=True)
subprocess.check_call(f"docker run --network=host -v {os.path.join(os.getcwd(), 'test')}:/data {testImage}", shell=True)

