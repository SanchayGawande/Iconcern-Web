
import PyPDF2
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOllama
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
import chainlit as cl
import redis
import asyncio
from langchain_groq import ChatGroq


# Establish a connection to the Redis server for caching responses.
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Load and read a PDF from a predefined path on your system.
pdf_path = 'data/diabetes_text_op.pdf'
pdf = PyPDF2.PdfReader(pdf_path)
pdf_text = ""
for page in pdf.pages:
    pdf_text += page.extract_text()

# Split the text from the PDF into manageable chunks for processing.
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.split_text(pdf_text)

# Create metadata for each text chunk to facilitate retrieval and indexing.
metadatas = [{"source": f"{i}-pl"} for i in range(len(texts))]

# Initialize text embeddings and create a vector store from the text chunks.
embeddings = OllamaEmbeddings(model="nomic-embed-text")
docsearch = Chroma.from_texts(texts, embeddings, metadatas=metadatas)

# Setup memory and history management for conversation continuity.
message_history = ChatMessageHistory()
memory = ConversationBufferMemory(
    memory_key="chat_history",
    output_key="answer",
    chat_memory=message_history,
    return_messages=True,
)

llm_groq = ChatGroq(
            #groq_api_key=groq_api_key,
            #model_name='llama2-70b-4096' 
            model_name='mixtral-8x7b-32768'
    )

# Configure the conversational chain with the text data and memory systems.
chain = ConversationalRetrievalChain.from_llm(
    # llm=ChatOllama(model="mistral:instruct"),
    llm=llm_groq,
    retriever=docsearch.as_retriever(),
    memory=memory,
    return_source_documents=True,
)

# Store the configured chain globally for application-wide access.
global_chain = chain

@cl.on_chat_start
async def on_chat_start():
    # Send a welcome message to the user when the chat session starts.
    msg = cl.Message(content="Welcome to Iconcern, your diabetes chat assistant. How may I help you today?", author="Iconcern")
    await msg.send()
    
@cl.on_message
async def main(message: cl.Message):
    user_query = message.content.strip().lower()

    # Check cache first
    cached_response = redis_client.get(user_query)
    if cached_response:
        await cl.Message(content=cached_response, author="Iconcern").send()
        return

    # Send an initial message to the user indicating that processing has started
    await cl.Message(content="Processing your request...", author="Iconcern").send()

    # Process the query using the conversational chain
    res = await global_chain.ainvoke(user_query)
    answer = res["answer"]
    source_documents = res["source_documents"]

    text_elements = []
    source_info = ""

    if source_documents:
        for source_idx, source_doc in enumerate(source_documents):
            source_name = f"source_{source_idx}"
            text_elements.append(cl.Text(content=source_doc.page_content, name=source_name))
        source_names = [text_el.name for text_el in text_elements]
        source_info = f"\nSources: {', '.join(source_names)}" if source_names else "\nNo sources found"

    full_response = answer + source_info
    redis_client.set(user_query, full_response)

    # Send the final response to the user
    await cl.Message(content=full_response, author="Iconcern", elements=text_elements).send()