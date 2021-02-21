FROM balenalib/raspberrypi3-debian-python:3.7-buster-build

WORKDIR /usr/app/src

RUN install_packages jq curl python3-urwid python3-smbus 
RUN pip install spidev RPi.GPIO influxdb smbus

RUN wget https://github.com/PiSupply/PiJuice/raw/master/Software/Install/pijuice-base_1.6_all.deb && \
  dpkg -i pijuice-base_1.6_all.deb

RUN pip3 install smbus

COPY *.py ./

# Enable udevd so that plugged dynamic hardware devices show up in our container.
ENV UDEV=1

CMD ["python","counter.py"]




