ARG GECKODRIVER_VERSION=0.31.0
FROM alpine:3.16.2
LABEL maintainer="Björn Busse <bj.rn@baerlin.eu>"
LABEL org.opencontainers.image.source https://github.com/bbusse/firefox-streamer

ARG GECKODRIVER_VERSION

ENV BUILD_PACKAGES build-base

RUN \
# Use edge repos - needed for firefox
echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" > /etc/apk/repositories && \
echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories && \
echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories

# Update and install base packages
RUN apk update && apk upgrade && apk add bash $BUILD_PACKAGES

# We need gcompat for glibc
# libcap for setcap
RUN apk add gcompat firefox libcap sway mesa

# Selenium
RUN apk add libgcc python3 py3-pip && \
    pip3 install selenium

RUN apk --no-cache add ca-certificates wget
RUN wget https://github.com/mozilla/geckodriver/releases/download/v${GECKODRIVER_VERSION}/geckodriver-v${GECKODRIVER_VERSION}-linux64.tar.gz
RUN tar -zxf geckodriver-v${GECKODRIVER_VERSION}-linux64.tar.gz -C /usr/bin

# GStreamer
RUN apk add gstreamer gstreamer-tools gst-plugins-good

# Sway
RUN setcap cap_sys_admin=eip /usr/bin/sway

COPY ./stream-screenshots.py /usr/local/bin/

ENTRYPOINT "/usr/local/bin/stream-screenshots.py"
