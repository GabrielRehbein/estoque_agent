import os
from decouple import config
from langchain.agents import create_react_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from langchain.prompts import PromptTemplate
from prompt import default_prompt


os.environ['OPENAI_API_KEY'] = config('OPENAI_API_KEY')


class AIBot:

    def __init__(self, llm) -> None:
        self.__llm = ChatOpenAI(
            model=llm,
        )
        self.__db = SQLDatabase.from_uri('sqlite:///estoque.db')
        self.my_prompt = default_prompt

    def __get_system_prompt(self):
        system_prompt = hub.pull('hwchase17/react')
        return system_prompt

    def __get_sql_toolkit(self):
        sql_toolkit = SQLDatabaseToolkit(
            db=self.__db,
            llm=self.__llm,
        )
        return sql_toolkit

    def __create_agent(self):
        created_agent = create_react_agent(
            llm=self.__llm,
            tools=self.__get_sql_toolkit().get_tools(),
            prompt=self.__get_system_prompt(),
        )
        return created_agent

    def __agent_executor_configuration(self):
        sql_toolkit = self.__get_sql_toolkit()
        agent_executor = AgentExecutor(
            agent=self.__create_agent(),
            tools=sql_toolkit.get_tools(),
            verbose=True,
        )
        return agent_executor

    def __get_prompt_template(self):
        prompt_template = PromptTemplate.from_template(
            self.my_prompt
        )
        return prompt_template

    def format_prompt(self, user_question):
        prompt_template = self.__get_prompt_template()
        formatted_prompt = prompt_template.format(q=user_question)
        return formatted_prompt

    def generate_ai_response(self, formatted_prompt):
        agent_executed = self.__agent_executor_configuration()
        response = agent_executed.invoke({"input": formatted_prompt})
        return response.get('output')
