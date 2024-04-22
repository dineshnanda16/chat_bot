import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage,AIMessage
from langchain_core.prompts import ChatPromptTemplate     
from langchain_core.output_parsers import StrOutputParser  
from langchain_cohere  import ChatCohere
load_dotenv()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.set_page_config(page_title="chatwith_me", page_icon=":rocket:")
st.title("Chat_bot")

def get_response(query,chat_history):
    template = """
    I am a bot, I don't know how to respond to that.

    chat_history: {chat_history}

    user question: {user_question}
    
"""
    prompt=ChatPromptTemplate.from_template(template)

    llm = ChatCohere()

    chain= prompt | llm | StrOutputParser()

    return chain.stream({
        "chat_history":chat_history,
        "user_question":query
    })


for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)
    else:
        with st.chat_message("AI"):
            st.markdown(message.content)
            
user_query = st.chat_input("Enter your query here:")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        ai_response=st.write_stream(get_response(user_query,st.session_state.chat_history))

    st.session_state.chat_history.append(AIMessage(ai_response))