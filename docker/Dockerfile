FROM python:3.7.6

# Build-time metadata as defined at http://label-schema.org
ARG BUILD_DATE
ARG VCS_REF
ARG VERSION
LABEL org.label-schema.build-date=$BUILD_DATE \
      org.label-schema.name="Planet porder" \
      org.label-schema.description="Built from Python official uses Planet Labs Orders v2 API" \
      org.label-schema.url="https://planet.com" \
      org.label-schema.vcs-ref=$VCS_REF \
      org.label-schema.vcs-url="e.g. https://github.com/tyson-swetnam/porder" \
      org.label-schema.vendor="University of Arizona" \
      org.label-schema.version=$VERSION \
      org.label-schema.schema-version="1.0"

MAINTAINER "Tyson Lee Swetnam <tswetnam@cyverse.org>"

ENV DEBIAN_FRONTEND=noninteractive 
RUN apt update && apt install --assume-yes --no-install-recommends \
       software-properties-common \
       gnupg \
       curl \
       wget \
       git \
       libcurl4-openssl-dev \
       libssl-dev \
       docker.io && \
    rm -rf /var/lib/apt/lists/*

RUN add-apt-repository "deb https://qgis.org/debian `lsb_release -c -s` main" && \
    wget -qO - https://qgis.org/downloads/qgis-2020.gpg.key | gpg --no-default-keyring --keyring gnupg-ring:/etc/apt/trusted.gpg.d/qgis-archive.gpg --import && \
    chmod a+r /etc/apt/trusted.gpg.d/qgis-archive.gpg && \   
    apt update && \
    apt install -y gdal-bin python3-gdal

RUN git clone https://github.com/tyson-swetnam/porder --branch 0.7.8 --single-branch && \
    cd porder && \
    python setup.py install
