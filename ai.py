import os
from decouple import config

os.environ['OPENAI_API_KEY'] = config('OPENAI_API_KEY')

from langchain.agents import create_react_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from langchain.prompts import PromptTemplate
from prompt import DEFAULT_PROMPT


class AIBot:
    def __init__(self, llm) -> None:
        self.__llm = ChatOpenAI(
           model=llm,
        )
        self.__db = SQLDatabase.from_uri('sqlite:///estoque.db')
        self.my_prompt = DEFAULT_PROMPT

    def __get_prompt_template(self):
        prompt_template = PromptTemplate.from_template(
            self.my_prompt
        )
        return prompt_template
    
    def _invoke(self, question):
        return self.__llm.invoke(question).content

    def __get_system_prompt(self):
        return hub.pull('hwchase17/react')

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
        agent_executor = AgentExecutor(
            agent=self.__create_agent(),
            tools=self.__get_sql_toolkit(),
            verbose=True,
        )
        return agent_executor
    
    def format_prompt(self, user_question):
        formatted_prompt:PromptTemplate = self.__get_prompt_template().format(
        question=user_question)
        return formatted_prompt

    def genarator_ai_response(self, formatted_prompt):
        agent_executed = self.__agent_executor_configuration()
        response = agent_executed.invoke(formatted_prompt)
        return response


if __name__ == '__main__':
    ...