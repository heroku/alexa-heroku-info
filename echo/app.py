import json
import os
import pycurl

from StringIO import StringIO

from flask import Flask

from pylexa.app import alexa_blueprint
from pylexa.intent import handle_intent
from pylexa.response import PlainTextSpeech


CONCEPT_RESPONSES = {
    "Dyno": "",
    "Add-on": "",
}

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

    message = "Production and Development are both green. All systems are nominal."

    prod_status = response["status"]["Production"]
    dev_status = response["status"]["Development"]

    if prod_status != 'green' or dev_status != 'green':
        message = "Production is {0} and Development is {1}.".format(dev_status, prod_status)
    
    if response['issues']:
        message += " The following issues are open: " + " ".join(response['issues'])

    return PlainTextSpeech(message)


@handle_intent('HerokuInfo')
def handle_info_intent(request):
    concept = request.slots.get('Concept', 'snizbag')

    return PlainTextSpeech(concept)


@handle_intent('HerokuBestCSA')
def handle_best_csa_intent(request):
    return PlainTextSpeech("Michelle Rawley is the best Customer Solutions Architect. True fact!")


if __name__ == '__main__':
    app.run(debug=True)
