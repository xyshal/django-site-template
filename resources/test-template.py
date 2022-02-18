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
user = subprocess.check_output(["id","-un"]).rstrip().decode("UTF-8")
uid = subprocess.check_output(["id","-u"]).rstrip().decode("UTF-8")
gid = subprocess.check_output(["id","-g"]).rstrip().decode("UTF-8")

# We could just generate the site on the local machine, but doing it in a
# container ensures that our version of django matches.
subprocess.check_call(f"docker build -f environments/site/Dockerfile {emptyDir} -t tmp-deleteme --build-arg UNAME={user} --build-arg UID={uid} --build-arg GID={gid}", shell=True)

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

for f in ["urls.py", "models.py", "views.py", "tests.py"]:
    shutil.copyfile(os.path.join("resources","site",f"testapp-{f}"), os.path.join("testsite","testapp",f))

templatesDir = os.path.join("testsite", "testapp", "templates")
os.mkdir(templatesDir)
for f in ["index.html", "base_generic.html"]:
    shutil.copyfile(os.path.join("resources", "site", f), os.path.join(templatesDir, f))

os.mkdir(os.path.join("testsite", "testapp", "static"))
os.mkdir(os.path.join("testsite", "testapp", "static", "css"))
shutil.copyfile(os.path.join("resources", "site", "styles.css"), os.path.join("testsite", "testapp", "static", "css", "styles.css"))

# ------------------------------
print("Updating environment...")
# ------------------------------
# TODO: Why doesn't pointing to a file with env_file work in the docker-compose?
environmentFile = ".env"
if (os.path.exists(environmentFile)):
    os.remove(environmentFile)
shutil.copyfile(os.path.join("resources", "change.env"), environmentFile)
with open(environmentFile, "a") as f:
    f.write(f"UNAME={user}\n")
    f.write(f"UID={uid}\n")
    f.write(f"GID={gid}\n")

# -----------------------------
print("Spawning containers...")
# -----------------------------
subprocess.check_call("docker-compose up -d", shell=True)

# TODO: When the container gets a new enough version of docker, can just use
# `docker compose up -d --wait`
time.sleep(10)

# -----------------------
print("Running tests...")
# -----------------------
subprocess.check_call("python3 runtests.py", shell=True)

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

