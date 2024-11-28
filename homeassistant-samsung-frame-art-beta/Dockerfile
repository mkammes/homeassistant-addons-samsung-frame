ARG BUILD_FROM
FROM $BUILD_FROM

RUN \
  apk add --no-cache \
    python3 py3-pip
RUN \
  git clone https://github.com/NickWaterton/samsung-tv-ws-api.git \
  pip install "./samsung-tv-ws-api"
# Copy data for add-on
COPY run.sh /
COPY art.py /


RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
