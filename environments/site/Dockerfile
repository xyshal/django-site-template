FROM python:3.10-bullseye

# User setup
# ----------
# Specify these parameters on the command line to be your own UID/GID so that,
# if you are mounting a local copy of the site for development purposes, they
# don't thrash the permissions.
ARG UNAME=www
ARG UID=1000
ARG GID=1000

RUN groupadd -g $GID -o $UNAME
RUN useradd -m -u $UID -g $GID -o -s /bin/bash $UNAME

# System packages
# ---------------
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -yf \
    postgresql-client \
    vim

# Copy site data and set permissions
# ----------------------------------
RUN mkdir -p /var/www
COPY . /var/www/
RUN chown -R $UID /var/www
RUN chgrp -R $GID /var/www


# Install Python packages
# -----------------------
USER $UNAME
ENV PATH=/home/$UNAME/.local/bin:$PATH
RUN pip3 install --upgrade pip
# TODO: This is where you would RUN pip3 install -r requirements.txt

# Timestamp the image
# -------------------
RUN touch /var/www/image-built-$(date +"%F-%T")

