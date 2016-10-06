import json
import os
import pycurl

from StringIO import StringIO

from flask import Flask

from pylexa.app import alexa_blueprint
from pylexa.intent import handle_intent
from pylexa.response import PlainTextSpeech


BASIC_RESPONSES = {
    "Dyno": """
    A dyno is a lightweight Linux container that runs a single user-specified command.
    A dyno can run any command available in its default environment --
    which is what we supply in the Cedar stack --
    or in your app’s slug -- which is a compressed and pre-packaged copy of your
    application and its dependencies.
    """,
    "Addon": "Add-ons are great",
    "Connect": "Connect is great",
    "Private Spaces": "Spaces are great",
    "Apps": "Apps are great",
    "Pipelines": "Pipelines are great",
    "Heroku": "Heroku is great",
}

CONCEPT_RESPONSES = {
    "dyno": BASIC_RESPONSES["Dyno"],
    "dynos": BASIC_RESPONSES["Dyno"],
    "addon": BASIC_RESPONSES["Addon"],
    "add-on": BASIC_RESPONSES["Addon"],
    "addons": BASIC_RESPONSES["Addon"],
    "add-ons": BASIC_RESPONSES["Addon"],
    "aonnect": BASIC_RESPONSES["Connect"],
    "heroku connect": BASIC_RESPONSES["Connect"],
    "private space": BASIC_RESPONSES["Private Spaces"],
    "private spaces": BASIC_RESPONSES["Private Spaces"],
    "app": BASIC_RESPONSES["Apps"],
    "apps": BASIC_RESPONSES["Apps"],
    "pipeline": BASIC_RESPONSES["Pipelines"],
    "pipelines": BASIC_RESPONSES["Pipelines"],
    "heroku": BASIC_RESPONSES["Heroku"],
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
    concept = request.slots.get('Concept', 'Heroku').lower()
    try:
        response = CONCEPT_RESPONSES[concept]
    except Exception:
        response = CONCEPT_RESPONSES["heroku"]

    return PlainTextSpeech(response)


@handle_intent('HerokuBestCSA')
def handle_best_csa_intent(request):
    return PlainTextSpeech("Michelle Rawley is the best Customer Solutions Architect. True fact!")


if __name__ == '__main__':
    app.run(debug=True)
