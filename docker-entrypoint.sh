#!/usr/bin/env bash

set -ex

mkdir -p /tmp/files
mkdir -p /tmp/cache

uvicorn --host 0.0.0.0 --port 80 main:app