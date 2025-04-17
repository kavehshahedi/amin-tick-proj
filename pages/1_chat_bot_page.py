import streamlit as st
import time
import numpy as np
import ollama
import logging

logger = logging.getLogger()
logging.basicConfig(encoding="UTF-8", level=logging.INFO)

# https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
st.set_page_config(
    page_title="TicketAssist - Q/A",
    page_icon="💬",
    initial_sidebar_state="expanded",  
)

# st.markdown("# Plotting Demo")

# st.sidebar.header("Plotting Demo")

# st.write(
#     """This demo illustrates a combination of plotting and animation with
# Streamlit. We're generating a bunch of random numbers in a loop for around
# 5 seconds. Enjoy!"""
# )

# progress_bar = st.sidebar.progress(0)
# status_text = st.sidebar.empty()
# last_rows = np.random.randn(1, 1)
# chart = st.line_chart(last_rows)

# for i in range(1, 101):
#     new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
#     status_text.text("%i%% Complete" % i)
#     chart.add_rows(new_rows)
#     progress_bar.progress(i)
#     last_rows = new_rows
#     time.sleep(0.05)

# progress_bar.empty()

# # Streamlit widgets automatically run the script from top to bottom. Since
# # this button is not connected to any other logic, it just causes a plain
# # rerun.
# st.button("Re-run")

# to load all API keys and env variables
# from dotenv import load_dotenv
# load_dotenv()

import time
import json
import shelve
import subprocess
import extra_streamlit_components as stx
from streamlit_float import *

# ollama run llama3
# python -m venv venv
# source venv/bin/activate
st.title("💬 TicketAssist Chatbot")

# https://github.com/pierrelouisbescond/streamlit-chat-ui-improvement/blob/main/main.py
cookie_manager = stx.CookieManager(key="cookie_manager")
# initialize float feature/capability
float_init()

# https://github.com/daveebbelaar/streamlit-chatbot-interface/blob/main/app.py
USER_AVATAR = "🧑‍💻"
BOT_AVATAR = "🤖"

# In case of rerun of the last question, we remove the last answer from st.session_state["messages"]
if "rerun" in st.session_state and st.session_state["rerun"]:
    print("Salam")
    st.session_state["messages"].pop(-1)
    
# Replicate Credentials
with st.sidebar:
    st.title('TicektAssist Chatbot')
    if 'REPLICATE_API_TOKEN' in st.secrets:
        st.success('Connected to ELI API', icon='✅')
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        pass
        replicate_api = st.text_input('Enter Replicate API token:', type='password')
        if not (replicate_api.startswith('r8_') and len(replicate_api)==40):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')

    # Refactored from https://github.com/a16z-infra/llama2-chatbot
    st.subheader('Models and parameters')
    selected_model = st.sidebar.selectbox('Choose a model', ['Llama3-8B', 'Llama2-13B'], key='selected_model')
    if selected_model == 'Llama3-8B':
        llm = 'llama3.1:8b'
    
    # output = subprocess.check_output(['ollama', 'list'], text=True)
    # models = [line.split()[0] for line in output.strip().split('\n')]
    # available_models = models
    # selected_model = st.selectbox('Choose a model', models, key='selected_model')

    temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=5.0, value=0.1, step=0.01)
    top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.sidebar.slider('max_length', min_value=64, max_value=4096, value=512, step=8)
    seed = st.number_input('Seed', min_value=0, max_value=10000, value=101, step=1)
        
    st.markdown('📖 Lear more [here]()!')

# os.environ['REPLICATE_API_TOKEN'] = replicate_api

# Load chat history from shelve file
def load_chat_history():
    with shelve.open("data/chat_history") as db:
        return db.get("messages", [])

# Save chat history to shelve file
def save_chat_history(messages):
    with shelve.open("data/chat_history") as db:
        db["messages"] = messages

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
    save_chat_history([])

# This function logs the last question and answer in the chat messages
def log_feedback(icon):
    # We retrieve the last question and answer
    last_messages = json.dumps(st.session_state["messages"][-2:])

    # We record the timestamp
    activity = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": "

    # And include the messages
    activity += "positive" if icon == "👍" else "negative"
    activity += ": " + last_messages

    # And log everything
    logger.info(activity)
    
    # We display a nice toast
    st.toast("Thanks for your feedback!", icon="👌")

# Initialize or load chat history
if "messages" not in st.session_state.keys():
    st.session_state.messages = load_chat_history()
    # st.session_state.messages = [{"role": "assistant", "content": "How can I help you?"}]

# Sidebar with a button to delete chat history
# with st.sidebar:
#     if st.button("Clear Chat History"):
#         st.session_state.messages = []
#         save_chat_history([])
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Display chat history messages
### Write Message History
for message in st.session_state.messages:
    avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
    st.chat_message(message["role"], avatar=avatar).write(message["content"])

# if "messages" not in st.session_state:
#     st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

## Generator for Streaming Tokens
# Function for generating LLaMA2 response
def generate_llama3_response():
    # string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    # for dict_message in st.session_state.messages:
    #     if dict_message["role"] == "user":
    #         string_dialogue += "User: " + dict_message["content"] + "\n\n"
    #     else:
    #         string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    
    # output = replicate.run(llm, 
    #                        input={"prompt": f"{string_dialogue} {prompt_input} Assistant: ",
    #                               "temperature":temperature, "top_p":top_p, "max_length":max_length, "repetition_penalty":1})
    
    response = ollama.chat(model='llama3.1:8b', stream=True, messages=st.session_state.messages)
    for partial_resp in response:
        token = partial_resp["message"]["content"]
        st.session_state["full_message"] += token
        yield token

# # #  := (walrus-operator) a way to assign to variables within an expression
# Main chat interface
# if prompt := st.chat_input("How can I help?"):
if prompt := st.chat_input("Ask anything", max_chars=150, disabled=not replicate_api):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user", avatar=USER_AVATAR).write(prompt)
    with st.spinner("Thinking..."):
        st.session_state["full_message"] = ""
        st.chat_message("assistant", avatar=BOT_AVATAR).write_stream(generate_llama3_response)
        st.session_state.messages.append({"role": "assistant", "content": st.session_state["full_message"]}) 

# Generate a new response if last message is not from assistant
# if st.session_state.messages[-1]["role"] != "assistant":
#     with st.chat_message("assistant"):
#         with st.spinner("Thinking..."):
#             response = generate_llama3_response(prompt)
#             placeholder = st.empty()
#             full_response = ''
#             for item in response:
#                 full_response += item
#                 placeholder.markdown(full_response)
#             placeholder.markdown(full_response)
#     message = {"role": "assistant", "content": full_response}
#     st.session_state.messages.append(message)

from streamlit_feedback import streamlit_feedback
# https://github.com/trubrics/streamlit-feedback
# https://blog.streamlit.io/trubrics-a-user-feedback-tool-for-your-ai-streamlit-apps/
if st.session_state.messages:
    #TODO: we should put it after answer generation 
    feedback = streamlit_feedback(
        # feedback_type="thumbs",
        feedback_type="faces",
        optional_text_label="[Optional] Please provide an explanation",
        key=f"feedback_{len(st.session_state.messages)}",
    )
    st.toast("Feedback recorded!", icon="📝")
    # This app is logging feedback to Trubrics backend, but you can send it anywhere.
    # The return value of streamlit_feedback() is just a dict.
    # print(feedback)
    
# # Save chat history after each interaction
save_chat_history(st.session_state.messages)


#TODO: Pause generating the answer
#TODO: disable the prompt during answer generation
#TODO: check the chat history when we are sending a new prompt to the model
#TODO: Save the model parameter history
#TODO: Send model parameters to ollama
#TODO: Do not show feedback after the first prompt (at the beginning)