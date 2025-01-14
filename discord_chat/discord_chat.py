#!/usr/bin/env python3

import os

import click
from bottle import route, run, request, BaseRequest, HTTPError, default_app
from discord_webhook import DiscordWebhook

BaseRequest.MEMFILE_MAX = 1024 * 1024 * 100


global OUTPUT_DIRECTORY, WEBHOOK_URL


@route('/', method='POST')
def index():
    if 'filename' not in request.params:
        raise HTTPError(400, 'filename param is missing')
    filename = os.path.basename(request.params['filename'])

    fpath = os.path.join(OUTPUT_DIRECTORY, filename)
    with open(fpath, 'wb') as f:
        body = request.body
        while True:
            chunk = body.read(0xFFFF)
            if not chunk:
                break
            f.write(chunk)

    webhook = DiscordWebhook(url=WEBHOOK_URL)

    with open(fpath, "rb") as f:
        webhook.add_file(file=f.read(), filename=filename)

    response = webhook.execute()

    return 'OK'


@click.command()
@click.option('--host', '-h', envvar='HOST', default='0.0.0.0', type=str)
@click.option('--port', '-p', envvar='PORT', default=8080, type=int)
@click.option('--output', '-o', envvar='OUTPUT_DIR', default='output',
              type=click.Path(file_okay=False, writable=True, resolve_path=True))
@click.option('--webhook-url', '-w', envvar='WEBHOOK_URL', type=str)
def start(host, port, output, webhook_url):
    global OUTPUT_DIRECTORY, WEBHOOK_URL
    OUTPUT_DIRECTORY = output
    WEBHOOK_URL = webhook_url
    os.makedirs(output, exist_ok=True)
    run(host=host, port=port)


if __name__ == '__main__':
    start()

app = default_app()
