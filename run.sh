#!/bin/sh

#
# use this for development
#
# docker run -it -p 8000:8000 \
# -v `pwd`/bin:/app/bin \
# -v `pwd`/favicon.ico:/app/favicon.ico \
# -v `pwd`/index.html:/app/index.html \
# -v ~/Pictures/iPhotoLibrary/:/app/iPhotoLibrary \
# -w /app python:2.7-slim python bin/iphotoserver.py

#
# use prebuilt container
#
docker run -it -p 8000:8000 \
-v ~/Pictures/iPhotoLibrary/:/app/iPhotoLibrary \
moononournation/python:2.7-iphotoserver
