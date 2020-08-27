FROM python:3.7.6

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
