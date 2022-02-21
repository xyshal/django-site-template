#!/bin/bash
export DISPLAY=:0
if ! pgrep -x openbox > /dev/null; then
  Xvnc :0 -geometry 1280x1024 -SecurityTypes=None -AlwaysShared=1 & sleep 2 && openbox &
fi
