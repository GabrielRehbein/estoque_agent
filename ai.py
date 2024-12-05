import os
from decouple import config

os.environ['OPENAI_API_KEY'] = config('OPENAI_API_KEY')

from langchain.agents import create_react_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from langchain.prompts import PromptTemplate
from prompt import default_prompt


class AIBot:
    
    def __init__(self, llm) -> None:
        self.__llm = ChatOpenAI(
           model=llm,
        )
        self.__db = SQLDatabase.from_uri('sqlite:///estoque.db')
        self.my_prompt = default_prompt

    def __get_prompt_template(self):
        prompt_template = PromptTemplate.from_template(
            self.my_prompt
        )
        print(f'Prompt T {prompt_template}')
        return prompt_template
    
    def _invoke(self, question):
        return self.__llm.invoke(question).content

    def __get_system_prompt(self):
        #ok
        system_prompt = hub.pull('hwchase17/react')
        print(f'Sys Prompt {system_prompt}')
        return system_prompt

    def __get_sql_toolkit(self):
        sql_toolkit = SQLDatabaseToolkit(
            db=self.__db,
            llm=self.__llm,
        )
        print(f'sql_toolkit {sql_toolkit}')
        return sql_toolkit

    def __create_agent(self):
        #ok
        created_agent = create_react_agent(
            llm=self.__llm,
            tools=self.__get_sql_toolkit().get_tools(),
            prompt=self.__get_system_prompt(),
        )
        print(f'created_agent {created_agent}')
        return created_agent
    
    def __agent_executor_configuration(self):
        sql_toolkit = self.__get_sql_toolkit()
        agent_executor = AgentExecutor(
            agent=self.__create_agent(),
            tools=sql_toolkit.get_tools(),
            verbose=True,
        )
        print(f'agent_executor {agent_executor}')
        return agent_executor
    
    def format_prompt(self, user_question):
        prompt_template = self.__get_prompt_template()
        formatted_prompt = prompt_template.format(input=user_question)
        return formatted_prompt

    def genarator_ai_response(self, formatted_prompt):
        agent_executed = self.__agent_executor_configuration()
        response = agent_executed.invoke({"input": formatted_prompt})
        print(f'response {response}')
        return response


if __name__ == '__main__':
    botai = AIBot('gpt-3.5-turbo-0125')
    q = botai.format_prompt(default_prompt)
    botai.genarator_ai_response(q)