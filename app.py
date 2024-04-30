# pip install streamlit langchain bs4 
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
import assistant_response
import time
import pandas as pd

def context_is_needed(query):
    list_of_keys = pd.read_csv("page_index.csv")
    list_of_keys = list_of_keys['title'].tolist()
    for key in list_of_keys:
        if key in query:
            return True
    return False

def get_response(user_query):
    start = time.time()
    user_query = user_query.lower()
    need_context = context_is_needed(user_query)
    response = assistant_response.get_response(user_query, need_context)
    end = time.time()
    print("Answer is generated in {}s".format(end-start))
    return response

# app configs
st.set_page_config(page_title="Chat with iRobin", page_icon=r".\icon\OIP.ico")
st.title("Chat with iRobin")

name = ''

# side bar
with st.sidebar:
    st.header("Chat History")
    st.write("Insert your access token to start the chat.")
    name=st.text_input("Your access token.")
    print("Ready to chat.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content=f"Hello, {name}! I'm iRobin. How can I assist you?"),
    ]


if name is None or name == "":
    st.info("Please enter a valid token of your access.")
else: 
    with st.sidebar:
        st.write(name)
    # User input
    user_query = st.chat_input("Tell me about RAG?")
    if user_query is not None and user_query != "":
        if "sing" in user_query:
            response = "This is my song for you~ <3"
            #embed_youtube_video()

        else:
            response = get_response(user_query)
        st.session_state.chat_history.append(HumanMessage(user_query))
        st.session_state.chat_history.append(AIMessage(response))


    with st.sidebar:
        for i in range(len(st.session_state.chat_history)):
            if isinstance(st.session_state.chat_history[i], AIMessage):
                st.write("<< iRobin >>:", st.session_state.chat_history[i].content)
            else:
                st.write("<< You >>:", st.session_state.chat_history[i].content)


    # Conversation
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                if message == st.session_state.chat_history[0]:
                    st.image(r".\icon\OIP.ico", caption=r"iRobin")
                else: 
                    st.image(r".\icon\89a98bb21a59482af84118874509086a.jpg", width=250, caption=r"iRobin")
                st.write(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.write(message.content)
