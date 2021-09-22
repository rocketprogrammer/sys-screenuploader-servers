FROM python:3.6.4-alpine3.7

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

WORKDIR /opt

RUN mkdir -p sys-screenuploader-discord_chat
WORKDIR /opt/sys-screenuploader-discord_chat

COPY . .

RUN ["chmod", "+x", "entrypoint.sh"]

ENTRYPOINT ["./entrypoint.sh"]
