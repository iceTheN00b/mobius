print("handling imports..")
import flask
import json
from kandiiEngine import kandiiEngine


E = flask.Flask("mobius")

print("sculpting kandii..")
kandii = kandiiEngine()

#Thread(target=kandii.run).start()

kandii.run()

@E.route("/kandii")

def returnkandiiagentRender():
    action = flask.make_response()

    kandiiState = json.load(open(kandii.DATA,"r"))
    action.headers["response"] = "true"
    action.headers["location"] = kandiiState["location"]
    action.headers["position"] = kandiiState["position"]
    action.headers["task"] = kandiiState["task"]

    return action


#E.run(host="127.0.0.9",port=9999,debug=True)
