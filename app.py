import sys
from io import BytesIO

import telegram

import urllib3.request

from flask import Flask, request, send_file

from fsm import TocMachine



API_TOKEN = '360674186:AAExbZkdvA_HjN-BpWkOhdMlKCFQqG_9x2k'
WEBHOOK_URL = 'https://0ae3afee.ngrok.io/hook'

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)
machine = TocMachine(
    states=[
        'user',
        'article',
        'works',
        'reference',
        'w_music',
        'w_drama',
        'fb',
        'search',
        'profile',
        'other',
        'youtube',
        'wiki'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'article',
            'conditions': 'article'
        },
        {
            'trigger': 'advance',
            'source': 'article',
            'dest': 'search',
            'conditions': 'search'
        },
        {
            'trigger': 'advance',
            'source': 'search',
            'dest': 'works',
            'conditions': 'works'
        },
        {
            'trigger': 'advance',
            'source': 'search',
            'dest': 'reference',
            'conditions': 'reference'
        },
        {
            'trigger': 'advance',
            'source': 'search',
            'dest': 'other',
            'conditions': 'other'
        },
        {
            'trigger': 'advance',
            'source': 'reference',
            'dest': 'profile',
            'conditions': 'profile'
        },
        {
            'trigger': 'advance',
            'source': 'reference',
            'dest': 'fb',
            'conditions': 'fb'
        },
        {
            'trigger': 'advance',
            'source': 'works',
            'dest': 'w_music',
            'conditions': 'w_music'
        },
        {
            'trigger': 'advance',
            'source': 'works',
            'dest': 'w_drama',
            'conditions': 'w_drama'
        },
        {
            'trigger': 'advance',
            'source': 'other',
            'dest': 'youtube',
            'conditions': 'youtube'
        },
        {
            'trigger': 'advance',
            'source': 'other',
            'dest': 'wiki',
            'conditions': 'wiki'
        },
        {
            'trigger': 'go_back',
            'source': [
                          'works',
                          'profile',
                          'award',
                          'w_music',
                          'w_drama',
                          'w_show',
                          'data',
                          'fb',
                          'news',
                          'a_music',
                          'a_drama',
                          'other',
                          'youtube',
                          'wiki'
            ],
            'dest': 'article'
        }
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)


def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    machine.advance(update)
    return 'ok'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')


if __name__ == "__main__":
    _set_webhook()
    app.run()
