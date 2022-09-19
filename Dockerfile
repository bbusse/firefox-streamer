ARG SWAYVNC_VERSION=latest
ARG GECKODRIVER_VERSION=0.31.0
FROM ghcr.io/bbusse/swayvnc:${SWAYVNC_VERSION}
LABEL maintainer="Björn Busse <bj.rn@baerlin.eu>"
LABEL org.opencontainers.image.source https://github.com/bbusse/firefox-streamer

ARG GECKODRIVER_VERSION

ENV ARCH="x86_64" \
    USER="firefox-user" \
    APK_ADD="gcompat libgcc python3 py3-pip gstreamer gstreamer-tools gst-plugins-good python3 firefox py3-pip wf-recorder" \
    APK_DEL=""

USER root

RUN \
# Use edge repos - needed for firefox
echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" > /etc/apk/repositories && \
echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories && \
echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories

# Add application user and application
# Cleanup: Remove files and users
RUN addgroup -S $USER && adduser -S $USER -G $USER -G abuild \
    # https://gitlab.alpinelinux.org/alpine/aports/-/issues/11768
    && sed -i -e 's/https/http/' /etc/apk/repositories \
    && apk add --no-cache ${APK_ADD} \
    && apk del --no-cache ${APK_DEL} \
    && rm -rf \
      /usr/share/man/* \
      /usr/includes/* \
      /var/cache/apk/* \
    && deluser --remove-home daemon \
    && deluser --remove-home adm \
    && deluser --remove-home lp \
    && deluser --remove-home sync \
    && deluser --remove-home shutdown \
    && deluser --remove-home halt \
    && deluser --remove-home postmaster \
    && deluser --remove-home cyrus \
    && deluser --remove-home mail \
    && deluser --remove-home news \
    && deluser --remove-home uucp \
    && deluser --remove-home operator \
    && deluser --remove-home man \
    && deluser --remove-home cron \
    && deluser --remove-home ftp \
    && deluser --remove-home sshd \
    && deluser --remove-home at \
    && deluser --remove-home squid \
    && deluser --remove-home xfs \
    && deluser --remove-home games \
    && deluser --remove-home vpopmail \
    && deluser --remove-home ntp \
    && deluser --remove-home smmsp \
    && deluser --remove-home guest \

    # Get geckodriver
    && wget https://github.com/mozilla/geckodriver/releases/download/v${GECKODRIVER_VERSION}/geckodriver-v${GECKODRIVER_VERSION}-linux64.tar.gz \
    && tar -xzf geckodriver-v${GECKODRIVER_VERSION}-linux64.tar.gz -C /usr/bin \
    && rm geckodriver-v${GECKODRIVER_VERSION}-linux64.tar.gz \
    && geckodriver --version \

    # Add latest webdriver-util script for firefox automation
    && wget -P /usr/local/bin https://raw.githubusercontent.com/bbusse/webdriver-util/main/webdriver_util.py \
    && chmod +x /usr/local/bin/webdriver_util.py \

    # Add stream-controller for stream handling
    && wget -P /usr/local/bin https://raw.githubusercontent.com/bbusse/stream-controller/main/controller.py \
    && chmod +x /usr/local/bin/controller.py \

    # Add controller.py to startup
    && echo "exec controller.py --debug=$DEBUG" >> /etc/sway/config.d/controller

# Add entrypoint
USER $USER
COPY requirements.txt /
RUN pip3 install --user -r requirements.txt
COPY entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]
