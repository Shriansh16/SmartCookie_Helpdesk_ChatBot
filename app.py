import os
import streamlit as st
from dotenv import load_dotenv
from streamlit_chat import message
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder
)
from utils1 import *
import base64

# Load environment variables
load_dotenv()
KEY = os.getenv("OPENAI_API_KEY")
#KEY=st.secrets["OPENAI_API_KEY"]

# Streamlit setup
st.subheader("HELPDESK CHAT")

# Initialize session state variables
if 'responses' not in st.session_state:
    st.session_state['responses'] = ["How can I assist you?"]
if 'requests' not in st.session_state:
    st.session_state['requests'] = []

# Initialize the language model
llm = ChatOpenAI(model_name="gpt-4o", openai_api_key=KEY,temperature=0.5)

# Initialize conversation memory
if 'buffer_memory' not in st.session_state:
    st.session_state.buffer_memory = ConversationBufferWindowMemory(k=3, return_messages=True)

# Define prompt templates
system_msg_template = SystemMessagePromptTemplate.from_template(template="""Answer the question in a friendly and helpful manner, as if you are a real helpdesk support agent. Use only the information provided in the context below, and avoid phrases like 'In the context of the provided documents' or similar. If the answer is not contained within the text, say 'I'm not sure about that, but I'm here to help with anything else you need!'""")
                                                                           #Answer the question in a friendly and helpful manner, as if you are a real helpdesk support agent. Use only the information provided in the context below, and avoid phrases like 'In the context of the provided documents' or similar. If the answer is not contained within the text, say 'I'm not sure about that, but I'm here to help with anything else you need!'
human_msg_template = HumanMessagePromptTemplate.from_template(template="{input}")

prompt_template = ChatPromptTemplate.from_messages([system_msg_template, MessagesPlaceholder(variable_name="history"), human_msg_template])
link='logo.png'
# Create conversation chain
conversation = ConversationChain(memory=st.session_state.buffer_memory, prompt=prompt_template, llm=llm, verbose=True)

# Container for chat history
response_container = st.container()
# Container for text box
text_container = st.container()

with text_container:
    query = st.text_input("Query: ", key="input")
    if query:
        with st.spinner("typing..."):
            conversation_string = get_conversation_string()
            refined_query = query_refiner(conversation_string, query)
            #st.subheader("Refined Query:")
            #st.write(refined_query)
            context = find_match(refined_query)
            response = conversation.predict(input=f"Context:\n{context}\n\nQuery:\n{query}")
        
        # Append the new query and response to the session state
        st.session_state.requests.append(query)
        st.session_state.responses.append(response)
st.markdown(
    """
    <style>
    [data-testid="stChatMessageContent"] p{
        font-size: 1.0rem;
    }
    </style>
    """, unsafe_allow_html=True
)


# Display chat history
with response_container:
    if st.session_state['responses']:
        for i in range(len(st.session_state['responses'])):
            with st.chat_message('Momos', avatar=link):
                st.write(st.session_state['responses'][i])
            if i < len(st.session_state['requests']):
                message(st.session_state["requests"][i], is_user=True, key=str(i) + '_user')

#message("Hey, \nwhat's a chatbot?", is_user=True, avatar="{URL}")
#message(st.session_state['responses'][i], key=str(i),avatar_style="😂")
#message(st.session_state["requests"][i], is_user=True, key=str(i) + '_user')
#"""Answer the question in a friendly and helpful manner, as if you are a real helpdesk support agent. Provide accurate information based on the context provided. If you don't know the answer, simply say 'I'm not sure, but I'll find out for you!' or offer to assist with something else."""