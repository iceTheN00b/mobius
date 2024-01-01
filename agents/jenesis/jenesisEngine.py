from langchain.globals import set_llm_cache
from langchain_community.cache import SQLiteCache
from langchain_community.chat_models import ChatOpenAI
from agents.jenesis.jenesisAgent import jenesisAgent
from agents.jenesis.jenesisMind import jenesisMind

class jenesisEngine:
    def __init__(self):
        self.soul = self.setupSoul()
        self.agent = self.setupAgent()
        self.mind = self.setupMind()
        self.setupCache()

        self.RENDER_DATA = "data/renderData/jenesis.json"

    def setupSoul(self):
        return ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")

    def setupCache(self):
        set_llm_cache(SQLiteCache(database_path="data/cache/jenesisCache.db"))

    def setupAgent(self):
        return jenesisAgent()

    def setupMind(self):
        return jenesisMind(self.soul, self.agent)
