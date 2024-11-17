# iPhoto Server

This is a simple web interface for searching iPhoto library.

## Imported Library

- https://code.google.com/archive/p/phoshare/

## Run iPhoto Server
```console
docker run -it -p 8000:8000 -v "$HOME/Pictures/iPhoto Library.photolibrary":/app/iPhotoLibrary -w /app moononournation/python:2.7-iphotoserver
```
