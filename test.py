import os
import shutil
import subprocess

siteDir = os.path.join(os.getcwd(), "site")

if (os.path.isdir(siteDir)):
    raise Exception("You don't want to be running this script with an existing site.")
os.mkdir(siteDir)

# -------------------------------------
print("Generating test django site...")
# -------------------------------------
uid = subprocess.check_output(["id","-u"]).rstrip().decode("UTF-8")
gid = subprocess.check_output(["id","-g"]).rstrip().decode("UTF-8")

# We could just generate the site on the local machine, but doing it in a
# container ensures that our version of django matches.
subprocess.check_call(f"docker build -f environments/site/Dockerfile site -t tmp-deleteme --build-arg UID={uid} --build-arg GID={gid}", shell=True)
subprocess.check_call(f"docker run --user={uid}:{gid} -v {siteDir}:/var/www tmp-deleteme bash -c \"cd /var/www && pip install django && django-admin startproject testsite\"", shell=True)

# Cleanup
shutil.rmtree(siteDir)
