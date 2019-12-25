FROM python:3.7
LABEL maintaner="Florian Purchess <florian@attacke.ventures>"

RUN apt-get update -y && \
    apt-get install -y zlib1g-dev libjpeg-dev python3-pythonmagick inkscape xvfb poppler-utils \
    libfile-mimeinfo-perl qpdf libimage-exiftool-perl ufraw-batch ffmpeg

VOLUME /tmp/files/
VOLUME /tmp/cache/

WORKDIR /app

RUN pip install uvicorn

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY docker-entrypoint.sh /app/
COPY main.py /app/

EXPOSE 80

CMD ["./docker-entrypoint.sh"]
