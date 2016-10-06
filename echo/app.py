import json
import os
import pycurl

from StringIO import StringIO

from flask import Flask

from pylexa.app import alexa_blueprint
from pylexa.intent import handle_intent
from pylexa.response import PlainTextSpeech


BASIC_RESPONSES = {
    "Dyno": "Dynos are great",
    "Addon": "Add-ons are great",
    "Connect": "Connect is great",
    "Private Spaces": "Spaces are great",
    "Apps": "Apps are great",
    "Pipelines": "Pipelines are great",
    "Heroku": "Heroku is great",
}

CONCEPT_RESPONSES = {
    "Dyno": BASIC_RESPONSES["Dyno"],
    "Dynos": BASIC_RESPONSES["Dyno"],
    "Addon": BASIC_RESPONSES["Addon"],
    "Add-on": BASIC_RESPONSES["Addon"],
    "Addons": BASIC_RESPONSES["Addon"],
    "Add-ons": BASIC_RESPONSES["Addon"],
    "Connect": BASIC_RESPONSES["Connect"],
    "Heroku Connect", BASIC_RESPONSES["Connect"],
    "Private Space": BASIC_RESPONSES["Private Spaces"],
    "Private Spaces": BASIC_RESPONSES["Private Spaces"],
    "App": BASIC_RESPONSES["Apps"],
    "Apps": BASIC_RESPONSES["Apps"],
    "Pipeline": BASIC_RESPONSES["Pipelines"],
    "Pipelines": BASIC_RESPONSES["Pipelines"],
    "Heroku": BASIC_RESPONSES["Heroku"],
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
    concept = request.slots.get('Concept', 'Heroku')

    return PlainTextSpeech(concept)


@handle_intent('HerokuBestCSA')
def handle_best_csa_intent(request):
    return PlainTextSpeech("Michelle Rawley is the best Customer Solutions Architect. True fact!")


if __name__ == '__main__':
    app.run(debug=True)
