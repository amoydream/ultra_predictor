FROM python:3.7.5-slim-buster

RUN apt-get update
RUN apt-get --assume-yes install joe
WORKDIR /crawler
COPY /crawler/requirements.txt ./

COPY /crawler .

RUN pip install --no-cache-dir -r /crawler/requirements.txt

CMD tail -f /dev/null