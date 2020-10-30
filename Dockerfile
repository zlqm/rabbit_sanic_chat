FROM python:3.7-buster

RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get upgrade -y
ADD requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt -i https://pypi.douban.com/simple
