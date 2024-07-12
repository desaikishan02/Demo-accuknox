FROM ubuntu:latest
LABEL authors="kdesai"

ENTRYPOINT ["top", "-b"]