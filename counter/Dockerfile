FROM balenalib/raspberrypi3-debian-python:3.7-buster-build

WORKDIR /usr/app/src
RUN pip install spidev RPi.GPIO influxdb smbus
COPY *.py ./

# Enable udevd so that plugged dynamic hardware devices show up in our container.
ENV UDEV=1

CMD ["python","counter.py"]