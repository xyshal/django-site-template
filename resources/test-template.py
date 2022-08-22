import os
import shutil
import subprocess
import time

onGithubActionMachine = os.path.exists(os.path.join("/", "home", "runner"))

# ------------------------------
print("Updating environment...")
# ------------------------------
user = subprocess.check_output(["id","-un"]).rstrip().decode("UTF-8")
uid = subprocess.check_output(["id","-u"]).rstrip().decode("UTF-8")
gid = subprocess.check_output(["id","-g"]).rstrip().decode("UTF-8")

# TODO: Why doesn't pointing to a file with env_file work in the docker-compose?
environmentFile = ".env"
if (not os.path.exists(environmentFile)):
  shutil.copyfile(os.path.join("resources", "change.env"), environmentFile)
  with open(environmentFile, "a") as f:
      f.write(f"UNAME={user}\n")
      f.write(f"UID={uid}\n")
      f.write(f"GID={gid}\n")

# -----------------------------
print("Spawning containers...")
# -----------------------------
subprocess.check_call("docker-compose up --build -d", shell=True)
# TODO: When the container gets a new enough version of docker, can just use
# `docker compose up -d --wait` [although not quite now that we need to wait
# for the database to spin up]

# For now, just sleep until everything is probably done with initial setup
sleepTime = 40 if onGithubActionMachine else 15
time.sleep(sleepTime)

subprocess.check_call("docker-compose logs", shell=True)

# -----------------------
print("Running tests...")
# -----------------------
subprocess.check_call("python3 runtests.py", shell=True)

# ---------------------
print("Cleaning up...")
# ---------------------
subprocess.check_call("docker-compose down", shell=True)

