#!/usr/bin/env bash

set -ex

Xvfb :99 -screen 0 1x1x16 > /dev/null 2>&1 &

mkdir -p /tmp/files
mkdir -p /tmp/cache

DISPLAY=:99.0 uvicorn --host 0.0.0.0 --port 8000 app:app