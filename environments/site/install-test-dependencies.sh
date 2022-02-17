#!/bin/bash
apt-get update && apt-get install -yf firefox-esr tigervnc-standalone-server openbox
wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz
tar xf geckodriver-v0.30.0-linux64.tar.gz -C /usr/bin
