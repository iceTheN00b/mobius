from langchain.globals import set_llm_cache
from langchain_community.cache import SQLiteCache
from langchain_community.chat_models import ChatOpenAI


class jenesisEngine:
    def __init__(self):
        self.soul = self.setupSoul()
        self.mind = self.setupMind()
        self.agent = self.setupAgent()
        self.setupCache()
        self.TO_DO_LIST = "renderData/to_do_list.txt"


    def setupSoul(self):
        return ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613", openai_api_key=os.environ["egg"])

    def setupCache(self):
        set_llm_cache(SQLiteCache(database_path="../../data/cache/kandiCache.db"))

    def setupAgent(self):
        return jenesisAgent()

    def setupMind(self):
        return jenesisMind(self.soul, self.agent)
