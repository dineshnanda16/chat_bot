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

    llm = ChatCohere(COHERE_API_KEY="r6H0r9mAApORRZgBIUJqgMT4I3EwYYpZtqOtyEKI")

    chain= prompt | llm | StrOutputParser()

    return chain.invoke({
        "chat_history":chat_history,
        "user_question":query
    })

if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            AIMessage("How may i help you")
        ]
        
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)
            


user_query = st.chat_input("Type your message here...")
if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))

    with st.chat_message("Human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        response = get_response(user_query, st.session_state.chat_history)
        st.write(response)

    st.session_state.chat_history.append(AIMessage(content=response))