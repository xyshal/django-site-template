import os
import shutil
import subprocess
import time

for cmd in ["docker container prune -f",
            "docker image rm tmp-deleteme:latest site:latest -f"]:
  subprocess.check_call(cmd, shell=True)

siteDir = os.path.join(os.getcwd(), "testsite")
emptyDir = os.path.join(os.getcwd(), "emptydir")

for d in [siteDir, emptyDir]:
    if (os.path.isdir(d)):
        shutil.rmtree(d)
os.mkdir(emptyDir)

# -------------------------------------
print("Generating test django site...")
# -------------------------------------
uid = subprocess.check_output(["id","-u"]).rstrip().decode("UTF-8")
gid = subprocess.check_output(["id","-g"]).rstrip().decode("UTF-8")

# We could just generate the site on the local machine, but doing it in a
# container ensures that our version of django matches.
subprocess.check_call(f"docker build -f environments/site/Dockerfile {emptyDir} -t tmp-deleteme --build-arg UID={uid} --build-arg GID={gid}", shell=True)

siteGenerationCommands = ["cd /var/www",
                          "pip install django",
                          "django-admin startproject testsite",
                          "cd /var/www/testsite",
                          "python manage.py startapp testapp"]

subprocess.check_call(f"docker run --user={uid}:{gid} -v {os.getcwd()}:/var/www tmp-deleteme bash -c \"{' && '.join(siteGenerationCommands)}\"", shell=True)


# -------------------------------------
print("Copying test site resources...")
# -------------------------------------
for f in ["settings.py", "urls.py"]:
    shutil.copyfile(os.path.join("resources", "site", f), os.path.join("testsite", "testsite", f))

for f in ["urls.py", "models.py", "views.py"]:
    shutil.copyfile(os.path.join("resources","site",f"testapp-{f}"), os.path.join("testsite","testapp",f))

templatesDir = os.path.join("testsite", "testapp", "templates")
os.mkdir(templatesDir)
for f in ["index.html", "base_generic.html"]:
    shutil.copyfile(os.path.join("resources", "site", f), os.path.join(templatesDir, f))

os.mkdir(os.path.join("testsite", "testapp", "static"))
os.mkdir(os.path.join("testsite", "testapp", "static", "css"))
shutil.copyfile(os.path.join("resources", "site", "styles.css"), os.path.join("testsite", "testapp", "static", "css", "styles.css"))

# TODO: Maybe this here is the time to split the file; put this file in resources and call files in the root that would actually be used in production.

# ------------------------------
print("Updating environment...")
# ------------------------------
# TODO: Why doesn't pointing to a file with env_file work in the docker-compose?
environmentFile = ".env"
if (os.path.exists(environmentFile)):
    os.remove(environmentFile)
shutil.copyfile(os.path.join("resources", "change.env"), environmentFile)

# -----------------------------
print("Spawning containers...")
# -----------------------------
subprocess.check_call("docker-compose up -d", shell=True)

# TODO: Parse docker-compose logs instead
time.sleep(10)

# -----------------------
print("Running tests...")
# -----------------------
# Run a sanity check
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

# TODO: Run a unit test (through a docker exec?)

# TODO: Run an integration test.

# ---------------------
print("Cleaning up...")
# ---------------------
subprocess.check_call("docker-compose down", shell=True)
shutil.rmtree(siteDir)
shutil.rmtree(emptyDir)
os.remove(environmentFile)
for cmd in ["docker container prune -f",
            "docker image rm tmp-deleteme:latest site:latest -f"]:
  subprocess.check_call(cmd, shell=True)

