import json
import os
import pycurl

from StringIO import StringIO

from flask import Flask

from pylexa.app import alexa_blueprint
from pylexa.intent import handle_intent
from pylexa.response import PlainTextSpeech


BASIC_RESPONSES = {
    "Dyno": "A dyno is a lightweight Linux container that runs a single user-specified command. Apps are run inside dynos on the Heroku Platform.",
    "Addon": "Add-ons are tools and services for developing, extending, and operating your Heroku app. Some add-ons are built and maintained by Heroku. Others are offered by third party vendors.",
    "Connect": "HerokuConnect is an add-on that synchronizes data between your Salesforce organization and a Heroku Postgres database. Using HerokuConnect with Heroku Postgres, you can build applications that interact with your Salesforce data.",
    "Private Spaces": "Private Spaces are dedicated environments for running dynos and certain types of add-ons enclosed within an isolated network. Access to apps in a Private Space can be controlled at the network level.",
    "Apps": "An app is a collection of source code along some dependency description that tells Heroku how to build and run the application.",
    "Pipelines": "A pipeline is a group of Heroku apps that share the same codebase. Apps in a pipeline are grouped into stages that represent different deployment steps in a continuous delivery workflow. Michelle will show you a Pipelines demo if you ask her.",
    "Heroku": "Heroku lets you deploy, run, and manage applications written in Ruby, Node.js, Java, Python, Clojure, Scala, Go and PHP.",
    "Unsure": "You can ask me about dynos, add-ons, apps, pipelines, private spaces or Herokuconnect."
}

CONCEPT_RESPONSES = {
    "dyno": BASIC_RESPONSES["Dyno"],
    "dynos": BASIC_RESPONSES["Dyno"],
    "dino": BASIC_RESPONSES["Dyno"],
    "dinos": BASIC_RESPONSES["Dyno"],
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
    "unsure": BASIC_RESPONSES["Unsure"],
    "michelle": "Michelle Rawley is a Customer Solutions Architect at Heroku.",
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
    concept = request.slots.get('Concept', 'Unsure').lower()

    try:
        response = CONCEPT_RESPONSES[concept]
    except Exception:
        response = CONCEPT_RESPONSES["unsure"]

    return PlainTextSpeech(response)


@handle_intent('HerokuBestCSA')
def handle_best_csa_intent(request):
    return PlainTextSpeech("Michelle Rawley is the best Customer Solutions Architect. True fact!")


if __name__ == '__main__':
    app.run(debug=True)
