FROM balenalib/%%BALENA_MACHINE_NAME%%-debian-python:3.7.4

# Enable systemd init system
ENV INITSYSTEM off

# Set the working directory
WORKDIR /usr/src/app

RUN install_packages git dbus gnome-common

RUN apt-get update
RUN apt install python3-gi python3-gi-cairo gir1.2-gtk-3.0

# Upgrade pip
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --user -r requirements.txt --no-cache-dir --disable-pip-version-check \
                --index-url https://www.piwheels.org/simple

# Copy everything into the container
COPY . ./
#Make sure scripts in .local are usable:
ENV PATH=/root/.local/bin:$PATH
ENV DBUS_SYSTEM_BUS_ADDRESS=unix:path=/host/run/dbus/system_bus_socket
# Start application
CMD ["python", "button.py"]