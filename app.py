import streamlit as st

from option_llm_version import GPT_3_TURBO, GPT_4, GPT_4_TURBO

from ai import AIBot


def main():
    
    st.set_page_config(
        page_title='Agente de Estoque',
        page_icon='🤖',
    )

    st.header('Bem vindo ao Agente de Estoque!')

    llm_options = [
        GPT_3_TURBO,
        GPT_4,
        GPT_4_TURBO,
    ]

    llm = st.radio(
    label='Escolha a Versão:',
    options=llm_options,
    )
    if llm:
        bot_ai = AIBot(llm=llm)

    question = st.text_input(
        label='Digite Sua Pergunta...',
        max_chars=300,
    )
    ai_response = bot_ai._invoke(question)
    st.write(ai_response)
    print(llm)

main()