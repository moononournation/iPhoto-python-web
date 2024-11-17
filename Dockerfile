FROM python:2.7-slim
WORKDIR /app

COPY bin ./bin
COPY favicon.ico index.html ./

ENTRYPOINT ["python", "bin/iphotoserver.py"]
