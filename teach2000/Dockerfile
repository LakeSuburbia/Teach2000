
# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.9-alpine

LABEL maintainer="PostGIS Project - https://postgis.net"

ENV POSTGIS_MAJOR 3
ENV POSTGIS_VERSION 3.2.1+dfsg-1.pgdg110+1
ENV NODE_VERSION lts

RUN apt-get update \
      && apt-cache showpkg postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR \
      && apt-get install -y --no-install-recommends \
           postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR=$POSTGIS_VERSION \
           postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR-scripts \
           git-core curl build-essential openssl libssl-dev \
           python3-pip python3-setuptools python3-dev \
      && rm -rf /var/lib/apt/lists/*

# create root directory for our project in the container
RUN mkdir /teach2000

# Set the working directory to /teach2000
WORKDIR /teach2000

# Copy the current directory contents into the container at /teach2000
ADD . /teach2000/

# Install any needed packages specified in requirements.txt
RUN apk add zlib-dev jpeg-dev gcc musl-dev
RUN pip3 install --upgrade psycopg2-binary
RUN pip3 install --upgrade pillow
RUN pip3 install -r requirements.txt
