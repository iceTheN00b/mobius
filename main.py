print("..importing dependencies")
import flask
import json
from agents.kandii.kandiiEngine import kandiiEngine
from agents.jenesis.jenesisEngine import jenesisEngine

E = flask.Flask("mobius")

print("..sculpting jenesis")
jenesis = jenesisEngine()

print("!running jenesis")
jenesis.enginate()

print("sculpting kandii..")
kandii = kandiiEngine(False)



@E.route("/kandii")

def returnKandiiAgentRender():
    action = flask.make_response()

    kandiiState = json.load(open(kandii.RENDER_DATA, "r"))
    action.headers["response"] = "true"
    action.headers["location"] = kandiiState["location"]
    action.headers["position"] = kandiiState["position"]
    action.headers["task"] = kandiiState["task"]

    return action


@E.route("/jenesis")

def returnJenesisAgentRender():
    action = flask.make_response()

    kandiiState = json.load(open(jenesis.RENDER_DATA, "r"))
    action.headers["response"] = "true"
    action.headers["location"] = kandiiState["location"]
    action.headers["position"] = kandiiState["position"]
    action.headers["task"] = kandiiState["task"]

    return action

#E.run(host="127.0.0.9",port=9999,debug=True)
