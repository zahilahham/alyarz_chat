import streamlit as st
from langchain.vectorstores import Pinecone
import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from cryptography.fernet import Fernet

# Define the main color from the logo as the background color
background_color = "#98FB98"  # Light green background color

# Streamlit page configuration
st.set_page_config(page_title="YarzoBot", page_icon=":shamrock:")

# Load encryption key and encrypted message
with open("key.key", "rb") as key_file:
    key = key_file.read()
with open("encrypted.key", "rb") as encrypted_message:
    encrypted_message = encrypted_message.read()

fernet = Fernet(key)
decrypted_message = fernet.decrypt(encrypted_message)
OPENAI_API_KEY = decrypted_message.decode()

# Custom CSS for the Streamlit app to match the logo theme
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {background_color}; /* Light green background */
    }}
    
    .title {{
        color: black; /* Set title text color to black */
        font-size: 75px; /* Set font size */
        text-align: center; /* Center the title */
    }}
    
    .text-input-label {{
        color: black; /* Set text color to black */
        margin-bottom: 0; /* Remove bottom margin */
        font-size: 18px; /* Set font size to 18 pixels */
    }}

    /* Style for the text input and responses */
    .text-container {{
        background-color: rgba(255, 255, 255, 0.8); /* Semi-transparent white */
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 5px; /* Rounded corners */
        color: black; /* Text color black for readability */
    }}

    .stTextInput > input {{
        color: black;
    }}

    .stButton > button {{
        color: {background_color}; /* Green text color for buttons */
        background-color: white; /* White background for buttons */
        border: 2px solid white; /* White border for buttons */
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Display the logo and title
st.image('logo.png', width=300, use_column_width=True)  # Adjust path and width as needed
st.markdown('<h1 class="title">YarzoBot</h1>', unsafe_allow_html=True)

# Initialize Pinecone
try:
    index_name = 'alyarz-pinecone'
    text_field = "text"
    question = st.text_input('', value='', key=None, type='default', help=None)

    index = pinecone.Index(index_name)
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    pinecone.init(api_key="741ade23-d552-477b-8026-72f95d81e04e", environment="northamerica-northeast1-gcp")

    vectorstore = Pinecone(
        index, embeddings.embed_query, text_field
    )

    query = question

    llm = ChatOpenAI(
        openai_api_key=OPENAI_API_KEY,
        model_name='gpt-3.5-turbo',
        temperature=0.0
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )
    # Retrieve and display the chatbot response
    response = qa.run(query)
    if question:
        st.markdown(f'<div class="text-container">You: {question}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="text-container">YarzoBot: {response}</div>', unsafe_allow_html=True)
except Exception as e:
    st.error(f"An error occurred: {e}")