FROM python:3.11-bookworm
LABEL maintaner="Florian Purchess <florian@attacke.ventures>"

RUN apt-get update && \
  apt-get install -y poppler-utils qpdf libfile-mimeinfo-perl libimage-exiftool-perl ghostscript libsecret-1-0 zlib1g-dev libjpeg-dev \
  libreoffice inkscape ffmpeg xvfb \
  libnotify4 libappindicator3-1 curl \
  scribus inkscape \
  && rm -rf /var/lib/apt/lists/*

ENV DRAWIO_VERSION="12.6.5"
RUN curl -LO https://github.com/jgraph/drawio-desktop/releases/download/v${DRAWIO_VERSION}/draw.io-amd64-${DRAWIO_VERSION}.deb && \
  dpkg -i draw.io-amd64-${DRAWIO_VERSION}.deb && \
  rm draw.io-amd64-${DRAWIO_VERSION}.deb

WORKDIR /app

RUN pip install pipenv vtk
COPY Pipfile* /app/
RUN pipenv install --system

COPY docker-entrypoint.sh /app/
COPY app.py /app/

RUN groupadd -r previewservice && useradd -r -s /bin/false -g previewservice previewservice
RUN chown -R previewservice:previewservice /app
USER previewservice

EXPOSE 8000

CMD ["./docker-entrypoint.sh"]
