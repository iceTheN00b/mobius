import json
from enum import Enum

class kandiiAgent:
    def __init__(self):

        self.location = "playground"
        self.task = "idle"

        self.tasks = TASKS
        self.DATA = "renderData/kandii.json"
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

        #print("initiated kandii")

    def set_task(self, task):
        self.task = task

    def run(self):
        while True:
            self.save()


class TASKS(Enum):
    SLEEP = "sleep"
    PLAN = "plan"
    SEARCH = "search"
    WRITE = "write"
    THINK = "think"
    READ = "read"
    REVIEW = "review"
    UPLOAD = "UPLOAD"

class POSITIONS(Enum):
    BED = "bed"