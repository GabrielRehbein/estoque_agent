import os
from decouple import config

os.environ['OPENAI_API_KEY'] = config('OPENAI_API_KEY')

from langchain_openai import ChatOpenAI


class AIBot:
    def __init__(self, llm) -> None:
       self.__llm = ChatOpenAI(
           model=llm,
       )

    def _invoke(self, question):
        return self.__llm.invoke(question).content


if __name__ == '__main__':
    ...