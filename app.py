import streamlit as st
from chatbot.conversation import chat_bot
from chatbot.database import get_chat_history, save_chat


# Generate or retrieve session ID
from config import generate_session_id

if "session_id" not in st.session_state:
    st.session_state.session_id = generate_session_id()

st.title("AI Chatbot")
st.write("Ask me anything!")

# Display chat history
history = get_chat_history(st.session_state.session_id)
for user_msg, bot_resp in history:
    with st.chat_message("user"):
        st.write(user_msg)
    with st.chat_message("assistant"):
        st.write(bot_resp)

# User input
user_input = st.chat_input("Type your message...")
if user_input:
    response, session_id = chat_bot(user_input, st.session_state.session_id)
    
    # Display messages in chat
    with st.chat_message("user"):
        st.write(user_input)
    with st.chat_message("assistant"):
        st.write(response)
    
    # Save chat history
    save_chat(session_id, user_input, response)
