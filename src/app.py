import streamlit as st

from llm_version_options import GPT_3_TURBO, GPT_4, GPT_4_TURBO

from ai import AIBot


def main():
    message_history = []

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

    st.sidebar.title("GPT'S")
    llm = st.sidebar.radio(
        label='Selecione o Modelo:',
        options=llm_options
    )

    if llm:
        bot_ai = AIBot(llm=llm)

    if message_history:
        for message in message_history:
            st.write(message)

    question = st.chat_input(placeholder='Consulte...')

    if question:
        with st.spinner('Consultando o Banco de Dados'):
            formatted_question = bot_ai.format_prompt(question)
            ai_response = bot_ai.generate_ai_response(formatted_question)
            st.image("media/ai-ai-svgrepo-com.svg", width=30)
            st.markdown(ai_response)


if __name__ == '__main__':
    main()
