import os

from flask import Flask

from pylexa.app import alexa_blueprint
from pylexa.intent import handle_intent
from pylexa.response import PlainTextSpeech


app = Flask(__name__)
app.config['app_id'] = os.getenv('ALEXA_APP_ID')
app.register_blueprint(alexa_blueprint)


@handle_intent('Echo')
def handle_echo_intent(request):
    print(request)
    return PlainTextSpeech(request.slots.get('message', 'Nothing to echo'))


if __name__ == '__main__':
    app.run(debug=True)
