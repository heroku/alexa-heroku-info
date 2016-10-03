import json
import os
import pycurl

from StringIO import StringIO

from flask import Flask

from pylexa.app import alexa_blueprint
from pylexa.intent import handle_intent
from pylexa.response import PlainTextSpeech


app = Flask(__name__)
app.config['app_id'] = os.getenv('ALEXA_APP_ID')
app.register_blueprint(alexa_blueprint)


@handle_intent('HerokuStatus')
def handle_status_intent(request):
    buffer = StringIO()
    c = pycurl.Curl()
    c.setopt(c.URL, "https://status.heroku.com/api/v3/current-status")
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()

    response = json.loads(buffer.getvalue())

    prod_status = response["status"]["Production"]
    dev_status = response["status"]["Development"]

    if prod_status != 'green' or dev_status != 'green':
        message = "Production is {0} and Development is {1}".format(dev_status, prod_status)
    else:
        message = "Production and Development are green"

    return PlainTextSpeech(message, 'Nothing to echo')


@handle_intent('HerokuInfo')
def handle_info_intent(request):
    return PlainTextSpeech("Michelle Rowley is the best Customer Solutions Architect. True fact!")


if __name__ == '__main__':
    app.run(debug=True)
