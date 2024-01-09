from langchain.agents import initialize_agent, AgentType
from langchain.agents import Tool
from langchain.chains import LLMChain, RetrievalQA
from langchain.utilities.google_serper import GoogleSerperAPIWrapper
from langchain_core.prompts import PromptTemplate
from toolkit.Tasks import TASKS


#i would accomodate some changes to make this thing a bit more human readable
class bloggerArchitecture:

    def __init__(self, soul, memory, render):
        self.render = render
        self.soul = soul
        self.memory = memory

        self.idea_module = self.define_idea_module()
        self.research_module = self.define_research_module()
        self.outline_module = self.define_outline_module()


    def define_idea_module(self):

        #TODO: change this to check for old ideas first, before coming up with a new one.

        subtask = PromptTemplate.from_template(template="""
        0. Search for relevant information pertaining to the latest advances in tech.
        1. From this information, conclude what could be a compelling topic for a blogpost.
        2. Ensure you have not executed a similar topic before. If so, conclude on a new topic.
        """)

        def search_(query =""):
            self.render.set_task()
            return GoogleSerperAPIWrapper(type = "news").run(query)

        def recall_(idea =""):
            self.render.set_task()
            chain = RetrievalQA.from_llm(llm=self.soul, retriever=self.memory.as_retriever(search_kwargs={"k": 2}))

            return chain({"query":f"Have you written on this topic before? If so what was the name of the topic.: {idea}"})["result"]

        def compell_(info =""):
            self.render.set_task()
            chain = LLMChain(llm = self.soul, prompt = PromptTemplate.from_template("What is a compelling topic for a blogpost based on recent news:{info}"))
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
                description="to ensure a topic has not been executed before. Input should be the compelling blogpost topic."
            ),
            Tool(
                name = "compell_",
                func = compell_,
                description="to conclude on a compelling blogpost topic. Input should be information."
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
            result = idea_agent.invoke({"input":subtask})

            return result

        return idea_module

    def define_research_module(self):

        self.notepad : list = [] #takes note of things the agent has learnt.

        #TODO: implement conditional recursive searching ladies and gentlemen i.e make it such that the system continues to generate queries based until a satisfactory condition is met.
        #TODO: generally, i think iterative loops are neccessary

        subtask = PromptTemplate.from_template(template="""
        0. Generate 3 queries that can be used to investigate this idea: {idea}
        1. For each of these queries, search for information and take notes of the main facts.
        """)

        def querier_(topic =""):
            self.render.set_task()
            chain = LLMChain(llm = self.soul, prompt = PromptTemplate.from_template("generate 3 queries to investigate {idea}."))
            return chain.run(topic)

        def noter_(query = ""):
            self.render.set_task()
            result = GoogleSerperAPIWrapper().run(query)
            self.notepad.append(result)
            return f"!notes on {query} has been successfully taken"

        research_module_tools = [

            Tool(
                name = "querier_",
                func = querier_,
                description= "Useful for when you need to investigate an idea by generating queries. Input ought to be the topic"
            ),

            Tool(
                name = "noter_",
                func = noter_,
                description = "for when you need to research and then take notes of main facts and points. Input ought to query to search"
            )
        ]

        def research_module(input =""):
            research_agent = initialize_agent(
                tools= research_module_tools,
                llm = self.soul,
                agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                verbose=True
            )
            result = research_agent.run(subtask)

            return result


        return research_module

    def define_outline_module(self):
        pass