FROM python:3.10-bullseye

COPY install-test-dependencies.sh /root
RUN /root/install-test-dependencies.sh

RUN pip3 install selenium

COPY launch-vnc.sh /root

ENV DISPLAY=:0
CMD /root/launch-vnc.sh && sleep 2 && python3 /data/integration-test.py

