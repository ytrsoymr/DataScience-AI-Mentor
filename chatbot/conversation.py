import uuid
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_google_genai import GoogleGenerativeAI  # Update based on your model
from langchain_core.output_parsers  import StrOutputParser
from config import DB_PATH  # Import database path
import config

# Generate a unique session ID
def generate_session_id():
    return str(uuid.uuid4())

# Fetch session message history from the database
def get_session_message_history_from_db(session_id):
    chat_message_history = SQLChatMessageHistory(session_id=session_id, connection=f"sqlite:///{DB_PATH}")
    return chat_message_history

# Define a chat template
chat_template = ChatPromptTemplate(
    messages=[
        ("system", """You are DataScience-AI-Mentor, a conversational AI tutor specializing in data science. Your goal is to assist users by providing clear, concise, and accurate explanations for data science concepts, techniques, and tools. Maintain a friendly yet professional tone, ensuring responses are context-aware by leveraging memory.
                      For technical queries, offer step-by-step explanations with examples. If a question is unclear, ask for clarification. Keep responses engaging, relevant, and aligned with the user’s learning journey. If unsure, acknowledge it rather than guessing, and guide users toward reliable resources."""), 
        MessagesPlaceholder(variable_name="history"), 
        ("human", "{human_input}")
    ]
)

# Define the AI model (Update based on your API key and provider)
model = GoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=config.GOOGLE_API_KEY)


# Define output parser
output_parser = StrOutputParser()

# Create the conversation chain
chain = chat_template | model | output_parser

# Use RunnableWithMessageHistory to manage chat history
conversation_chain = RunnableWithMessageHistory(
    chain, 
    get_session_message_history_from_db,
    input_messages_key="human_input", 
    history_messages_key="history"
)

# Function to interact with the chatbot
def chat_bot(prompt, session_id=None):
    if session_id is None:
        session_id = generate_session_id()  # Generate a new session ID if not provided

    config = {"configurable": {"session_id": session_id}}
    input_prompt = {"human_input": prompt}

    response = conversation_chain.invoke(input_prompt, config=config)

    return response, session_id  # Return both response and session ID
