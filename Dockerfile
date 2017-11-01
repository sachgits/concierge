FROM python:3.6
MAINTAINER Bart Jeukendrup <bart@jeukendrup.nl>

# Install app dependencies
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app
RUN pip install -r requirements.txt

# Add app
ADD . /app

# Boot script
ADD docker/config.py /app/pleio_account/config.py
ADD docker/start.sh /start.sh
RUN chmod +x /start.sh

# HTTP port
EXPOSE 8000

# Define run script
CMD ["/start.sh"]
