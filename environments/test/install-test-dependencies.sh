#!/bin/bash
apt-get update && apt-get install -yf firefox-esr tigervnc-standalone-server openbox

uname -a | grep -q arm64
if [ $? -eq 0 ]; then
  wget http://launchpadlibrarian.net/583757436/firefox-geckodriver_97.0+build2-0ubuntu0.18.04.1_arm64.deb
  ar x firefox-geckodriver_97.0+build2-0ubuntu0.18.04.1_arm64.deb
  tar xf data.tar.xz
else
  wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz
  tar xf geckodriver-v0.30.0-linux64.tar.gz -C /usr/bin
fi
