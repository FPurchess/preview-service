FROM python:3.7
LABEL maintaner="Florian Purchess <florian@attacke.ventures>"

RUN apt-get update && \
  apt-get install -y zlib1g-dev libjpeg-dev python3-pythonmagick inkscape xvfb poppler-utils \
  libfile-mimeinfo-perl qpdf libimage-exiftool-perl ufraw-batch ffmpeg \
  scribus libreoffice \
  && rm -rf /var/lib/apt/lists/*

VOLUME /tmp/files/
VOLUME /tmp/cache/

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY docker-entrypoint.sh /app/
COPY app.py /app/

RUN groupadd -r previewservice && useradd -r -s /bin/false -g previewservice previewservice
RUN chown -R previewservice:previewservice /app
USER previewservice

EXPOSE 8000

CMD ["./docker-entrypoint.sh"]
