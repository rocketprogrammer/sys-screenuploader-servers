#!/usr/bin/env python3

import os

import click
from bottle import route, run, request, BaseRequest, HTTPError, default_app
from discord_webhook import DiscordWebhook, DiscordEmbed

BaseRequest.MEMFILE_MAX = 1024 * 1024 * 100


global OUTPUT_DIRECTORY, WEBHOOK_URL
ICON_URL = 'https://media.comicbook.com/2020/04/nintendo-switch-1216348-1280x0.jpeg'

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

    webhook = DiscordEmbed(url=WEBHOOK_URL, title='Switch', description = "Screenshots from Rocket's Switch", color='03b2f8')
    webhook.set_author(name='Nintendo Switch', url='https://nintendo.com', icon_url=ICON_URL)

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
def start(host, port, output):
    global OUTPUT_DIRECTORY, WEBHOOK_URL
    OUTPUT_DIRECTORY = output
    os.makedirs(output, exist_ok=True)
    run(host=host, port=port)


if __name__ == '__main__':
    start()

app = default_app()
