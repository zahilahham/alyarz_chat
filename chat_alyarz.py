from langchain.vectorstores import Pinecone
import pinecone
from credentials_hander import OPENAI_API_KEY
from langchain.embeddings.openai import OpenAIEmbeddings
import streamlit as st
from cryptography.fernet import Fernet
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

index_name = 'alyarz-pinecone-index'
text_field = "text"
st.set_page_config(page_title='YarzoBot', page_icon='https://publicimagesbucket.s3.us-west-2.amazonaws.com/alyarz_logo.png')

with open("key.key", "rb") as key_file:
    key =  key_file.read()
with open("encrypted.key", "rb") as encrypted_message:
    encrypted_message =  encrypted_message.read()

fernet = Fernet(key)
decrypted_message = fernet.decrypt(encrypted_message)
OPENAI_API_KEY = decrypted_message.decode()


st.markdown(
    """
    <style>
    .title {
        color: white; /* Set text color to white */
        font-size: 75px; /* Set font size */
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown('<h1 class="title">YarzoBot</h1>', unsafe_allow_html=True)

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://publicimagesbucket.s3.us-west-2.amazonaws.com/small_chat_alyarz.jpg");
             background-attachment: fixed;
             background-size: cover;
             color: white;  /* Set text color to white */
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
        color: white; /* Set text color to white */
        margin-bottom: 0; /* Remove bottom margin */
        font-size: 18px; /* Set font size to 18 pixels */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st_version = str(st.__version__)
st.write('<p class="text-input-label">Ask me anything...</p>', unsafe_allow_html=True)

css = '''
    <style>
        .text-container {
            background-color: rgba(255, 255, 255, 0.8);
            padding: 2px;
            margin-bottom: 2px;
            color: black; /* Set the text color to black */
        }

        .text-container span {
            color: black;
        }
    </style>
'''
# Set page configuration
st.markdown(css, unsafe_allow_html=True)
question = st.text_input('', value='', key=None, type='default', help=None)
try:
    index = pinecone.Index(index_name)
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY,model_name="ada")
    import pinecone
    pinecone.init(
        api_key="46b0be1d-d884-49da-a32b-e774dd426b72",
        environment="asia-southeast1-gcp-free"
    )
    vectorstore = Pinecone(
            index, embeddings.embed_query, text_field
        )
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
    
    response = qa.run(question)
    if question:
        st.markdown(f'<div class="text-container"><span>You:</span> {question}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="text-container"><span>YarzoBot:</span> {response}</div>', unsafe_allow_html=True)

except Exception as e:
    response = None
    print("error = " + str(e))