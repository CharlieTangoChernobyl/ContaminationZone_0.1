FROM balenalib/raspberrypi3-debian-python:3.7-buster-build

WORKDIR /usr/app/src

RUN pip install spidev RPi.GPIO smbus

# This will copy all files in our root to the working  directory in the container
COPY . ./

CMD ["python","power.py"]




