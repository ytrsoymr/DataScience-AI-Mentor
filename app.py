import streamlit as st
from chatbot.conversation import chat_bot
from chatbot.database import get_chat_history, save_chat


# Generate or retrieve session ID
from config import generate_session_id

if "session_id" not in st.session_state:
    st.session_state.session_id = generate_session_id()

st.title("DataScience-AI-Mentor")
st.write("Your AI-powered Data Science Tutor. Ask me anything related to Data Science!")

st.markdown("""
### **How It Works**
1. **Start a Conversation**
   - Type any **data science-related** question in the chat box.
   - Example: *"What is machine learning?"* or *"How do I use Pandas for data analysis?"*
2. **Receive an AI-Powered Response**
   - The chatbot will **analyze your question** and provide a clear, step-by-step explanation.
3. **Memory-Based Learning**
   - The chatbot **remembers past interactions** within the same session for **context-aware discussions**.
4. **Chat History**
   - You can review your past questions and answers in the chat window.
### **Who Can Use It?**
- **Students & Beginners** → Learn the basics of data science interactively.
- **Aspiring Data Scientists** → Get help with coding, algorithms, and real-world applications.
- **Professionals & Researchers** → Ask about advanced techniques and best practices.
- **Anyone Curious About Data Science** → Explore AI, Machine Learning, SQL, Python, and more!
### **Why Use DataScience-AI-Mentor?**
✅ **User-Friendly Interface** – Just start chatting!  
✅ **Step-by-Step Explanations** – Learn in a structured way.  
✅ **Memory for Better Conversations** – Get answers based on previous messages.  
✅ **Saves Chat History** – Review past queries anytime.  
""")

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
