from langchain.agents import initialize_agent, AgentType
from langchain.agents import Tool
from langchain.chains import LLMChain, ConversationalRetrievalChain, RetrievalQA
from langchain.utilities.google_serper import GoogleSerperAPIWrapper
from langchain_core.prompts import PromptTemplate
from toolkit.Tasks import TASKS


#i would accomodate some changes to make this thing a bit more human readable
class bloggerTools:

    def __init__(self, soul, memory, render):
        self.render = render
        self.soul = soul
        self.memory = memory

        self.idea_module = self.define_idea_module()


    def define_idea_module(self):

        #change this to check for old ideas first, before coming up with a new one.
        prompt = PromptTemplate.from_template(template="""
        0. Search for relevant information pertaining to the latest innovations in Large language models.
        1. From this information, conclude what could be a compelling idqqea for a blogpost.
        2. Ensure you have not already done a similar blogpost. If it has, consider a new idea, otherwise continue.
        """)

        def search_(query =""):
            self.render.set_task()
            return GoogleSerperAPIWrapper().run(query)

        def recall_(idea =""):
            self.render.set_task()
            chain = RetrievalQA.from_llm(llm=self.soul, retriever=self.memory.as_retriever(search_kwargs={"k": 2}))

            return chain({"query":f"Have you executed something similar to this: {idea}"})["result"]

        def compell_(info =""):
            self.render.set_task()
            chain = LLMChain(llm = self.soul, prompt = PromptTemplate.from_template("Generate on idea for a blogpost based on this information:{info}"))
            output = chain(info)
            return output["text"]

        idea_module_tools = [

            Tool(
                name="search_",
                func = search_,
                description="to search for information. Input should be the query"
            ),
            Tool(
                name = "recall_",
                func = recall_,
                description="to ensure an idea has not been executed before. Input should be the idea."
            ),
            Tool(
                name = "compell_",
                func = compell_,
                description="to conclude on a compelling blogpost idea. Input should be the information to be used to generate the idea"
            )
        ]

        def idea_module(input = ""):
            idea_agent = initialize_agent(
                tools=idea_module_tools,
                llm = self.soul,
                agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                #agent_kwargs={"prefix" :"Implement "},
                verbose=True
            )
            idea_agent.run(prompt)

        return idea_module

        def define_research_module(input = ""):

            prompt = PromptTemplate.from_template(template="""
            
            
            
            """)
