import json

#this class is neccessary in order to have the agent's behaviour be visualizable for any rendering application, a feature i think will become
#more common place were llm based agents turned towards consumers
class jenesisRender:
    def __init__(self):

        self.location = "playground"
        self.task = "idle"
        self.DATA = "renderData/jenesis.json"
        self.last_save = ""

    def save(self):
        dat = {
            "location":self.location,
            "position":self.position,
            "task":self.task
            }

        if dat != self.last_save:
            print("new update")
            self.last_save = dat
            open(self.DATA,"w").write(json.dumps(dat,indent=2))


    def setup(self):
        dat = json.load(open(self.DATA,"r"))
        self.location = dat["location"]
        self.position = dat["position"]
        self.task = dat["task"]

    def set_task(self, task = "IDLE"):
        self.task = task

    def run(self):
        while True:
            self.save()
