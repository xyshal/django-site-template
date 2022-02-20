import os
import shutil
import subprocess
import time

for cmd in ["docker container prune -f",
            "docker image rm site:latest -f"]:
  subprocess.check_call(cmd, shell=True)

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
subprocess.check_call("docker-compose up -d", shell=True)

# TODO: When the container gets a new enough version of docker, can just use
# `docker compose up -d --wait` [although not quite now that we need to wait
# for the database to spin up]
time.sleep(30)

subprocess.check_call("docker-compose logs", shell=True)

# -----------------------
print("Running tests...")
# -----------------------
subprocess.check_call("python3 runtests.py", shell=True)

# ---------------------
print("Cleaning up...")
# ---------------------
subprocess.check_call("docker-compose down", shell=True)
os.remove(environmentFile)
for cmd in ["docker container prune -f",
            "docker image rm tmp-deleteme:latest site:latest -f"]:
  subprocess.check_call(cmd, shell=True)

