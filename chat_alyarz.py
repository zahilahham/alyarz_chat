import streamlit as st
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from cryptography.fernet import Fernet


with open("key.key", "rb") as key_file:
    key =  key_file.read()
with open("encrypted.key", "rb") as encrypted_message:
    encrypted_message =  encrypted_message.read()

fernet = Fernet(key)
decrypted_message = fernet.decrypt(encrypted_message)
OPENAI_API_KEY = decrypted_message.decode()

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://publicimagesbucket.s3.us-west-2.amazonaws.com/small_chat_alyarz.jpg");
             background-attachment: fixed;
             background-size: cover;
             color: black;
             padding: 10px;
         }}
         </style>  
         """,
         unsafe_allow_html=True
     )

add_bg_from_url()
st.markdown(
    """
    <style>
    .text-input-label {
        color: black; /* Set text color to black */
        margin-bottom: 10px; /* Remove bottom margin */
        margin-top: 50px; /* Add a top margin */
        font-size: 25px; /* Set font size to 25 pixels */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
    .text-input-label {
        color: black;
        margin-bottom: 10px;
        font-size: 25px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st_version = str(st.__version__)
st.write('<p class="text-input-label">Hi, I am your personalized YarzoBot, ask me something!</p>', unsafe_allow_html=True)

css = '''
    <style>
        .text-container {
            background-color: rgba(255, 255, 255, 0.8);
            padding: 20px;  # Increase the padding
            margin-bottom: 10px;
            color: red;  # Change the text color to red
        }

        .text-container span {
            color: blue;  # Change the span color to blue
        }
    </style>
'''

st.markdown(css, unsafe_allow_html=True)


try:
    index_name = 'v1-index-pinecone'
    text_field = "text"
    question = st.text_input('', value='', key=None, type='default', help=None)
    from langchain.chains import RetrievalQA
    import os
    from credentials_hander import OPENAI_API_KEY
    from langchain.chat_models import ChatOpenAI
    from langchain.vectorstores import Chroma
    from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    db3 = Chroma(persist_directory="./chroma_db", embedding_function=embedding_function)
    query = question
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    model_name = "gpt-3.5-turbo"
    llm = ChatOpenAI(model_name=model_name)
    retrieval_chain = RetrievalQA.from_chain_type(llm, chain_type="stuff", retriever=db3.as_retriever())
    response = retrieval_chain.run(query)
    if question:
        st.markdown(f'<div class="text-container"><span>You:</span> {question}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="text-container"><span>ChatLAU:</span> {response}</div>', unsafe_allow_html=True)

except Exception as e:
    response = None