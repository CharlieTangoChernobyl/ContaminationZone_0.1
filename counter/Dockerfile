FROM balenalib/raspberrypi3-debian-python:3.7-buster-build

WORKDIR /usr/app/src

RUN install_packages jq curl python3-urwid python3-smbus 
RUN pip install spidev RPi.GPIO influxdb smbus

RUN wget https://github.com/PiSupply/PiJuice/raw/master/Software/Install/pijuice-base_1.6_all.deb && \
  dpkg -i pijuice-base_1.6_all.deb

RUN pip3 install smbus

# Copy requirements.txt first for better cache on later pushes
COPY requirements.txt requirements.txt

# pip install python deps from requirements.txt on the resin.io build server
RUN pip install -r requirements.txt

# This will copy all files in our root to the working  directory in the container
COPY . ./

# Enable udevd so that plugged dynamic hardware devices show up in our container.
ENV UDEV=1

CMD ["python","counter.py"]




