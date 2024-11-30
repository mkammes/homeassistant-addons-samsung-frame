ARG BUILD_FROM
FROM $BUILD_FROM

# Install required packages
RUN \
  apk add --no-cache \
  python3 \
  py3-pip \
  git

# Install Python dependencies
RUN pip3 install --no-cache-dir \
  Pillow \
  python-resize-image \
  aiohttp \
  websockets \
  git+https://github.com/NickWaterton/samsung-tv-ws-api.git

# Copy your scripts
COPY run.py /
COPY run.sh /

# Make scripts executable
RUN chmod a+x /run.sh

# Set proper S6 entrypoint
ENTRYPOINT ["/init"]
CMD [ "/run.sh" ]
