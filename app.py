import streamlit as st

from option_llm_version import GPT_3_TURBO, GPT_4, GPT_4_TURBO

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
        
        message_history.append(question)
        ai_response = bot_ai._invoke(question)
        st.write('User: ',question)
        st.write('AI: ', ai_response)
        
if __name__ == '__main__':
    main()