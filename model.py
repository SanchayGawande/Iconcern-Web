# import PyPDF2
# from langchain_community.embeddings import OllamaEmbeddings
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import Chroma
# from langchain.chains import ConversationalRetrievalChain
# from langchain_community.chat_models import ChatOllama
# from langchain_groq import ChatGroq
# from langchain.memory import ChatMessageHistory, ConversationBufferMemory
# import chainlit as cl

# # for chainlit, .env is loaded automatically
# #from dotenv import load_dotenv
# #load_dotenv()  #
# #groq_api_key = os.environ['GROQ_API_KEY']

# llm_local = ChatOllama(model="mistral:instruct")
# llm_groq = ChatGroq(
#             #groq_api_key=groq_api_key,
#             #model_name='llama2-70b-4096' 
#             model_name='mixtral-8x7b-32768'
#     )

# @cl.on_chat_start
# async def on_chat_start():
    
#     files = None #Initialize variable to store uploaded files

#     # Wait for the user to upload a file
#     while files is None:
#         files = await cl.AskFileMessage(
#             content="Please upload a pdf file to begin!",
#             accept=["application/pdf"],
#             max_size_mb=100,
#             timeout=180, 
#         ).send()

#     file = files[0] # Get the first uploaded file
    
#     # Inform the user that processing has started
#     msg = cl.Message(content=f"Processing `{file.name}`...")
#     await msg.send()

#     # Read the PDF file
#     pdf = PyPDF2.PdfReader(file.path)
#     pdf_text = ""
#     for page in pdf.pages:
#         pdf_text += page.extract_text()
        

#     # Split the text into chunks
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#     texts = text_splitter.split_text(pdf_text)

#     # Create a metadata for each chunk
#     metadatas = [{"source": f"{i}-pl"} for i in range(len(texts))]

#     # Create a Chroma vector store
#     embeddings = OllamaEmbeddings(model="nomic-embed-text")
#     #embeddings = OllamaEmbeddings(model="llama2:7b")
#     docsearch = await cl.make_async(Chroma.from_texts)(
#         texts, embeddings, metadatas=metadatas
#     )
    
#     # Initialize message history for conversation
#     message_history = ChatMessageHistory()
    
#     # Memory for conversational context
#     memory = ConversationBufferMemory(
#         memory_key="chat_history",
#         output_key="answer",
#         chat_memory=message_history,
#         return_messages=True,
#     )

#     # Create a chain that uses the Chroma vector store
#     chain = ConversationalRetrievalChain.from_llm(
#         llm = llm_local,
#         chain_type="stuff",
#         retriever=docsearch.as_retriever(),
#         memory=memory,
#         return_source_documents=True,
#     )

#     # Let the user know that the system is ready
#     msg.content = f"Processing `{file.name}` done. You can now ask questions!"
#     await msg.update()
#     #store the chain in user session
#     cl.user_session.set("chain", chain)


# @cl.on_message
# async def main(message: cl.Message):
        
#      # Retrieve the chain from user session
#     chain = cl.user_session.get("chain") 
#     #call backs happens asynchronously/parallel 
#     cb = cl.AsyncLangchainCallbackHandler()
    
#     # call the chain with user's message content
#     res = await chain.ainvoke(message.content, callbacks=[cb])
#     answer = res["answer"]
#     source_documents = res["source_documents"] 

#     text_elements = [] # Initialize list to store text elements
    
#     # Process source documents if available
#     if source_documents:
#         for source_idx, source_doc in enumerate(source_documents):
#             source_name = f"source_{source_idx}"
#             # Create the text element referenced in the message
#             text_elements.append(
#                 cl.Text(content=source_doc.page_content, name=source_name)
#             )
#         source_names = [text_el.name for text_el in text_elements]
        
#          # Add source references to the answer
#         if source_names:
#             answer += f"\nSources: {', '.join(source_names)}"
#         else:
#             answer += "\nNo sources found"
#     #return results
#     await cl.Message(content=answer, elements=text_elements).send()

import PyPDF2
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ChatOllama
from langchain.memory import ChatMessageHistory, ConversationBufferMemory
import chainlit as cl
import redis

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

# Configure the conversational chain with the text data and memory systems.
chain = ConversationalRetrievalChain.from_llm(
    llm=ChatOllama(model="mistral:instruct"),
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
    # Normalize the user's query to improve cache hit rate.
    user_query = message.content.strip().lower()

    # Attempt to retrieve a cached response for the query.
    cached_response = redis_client.get(user_query)
    if cached_response:
        # Send the cached response back to the user.
        await cl.Message(content=cached_response, author="Iconcern").send()
        return

    # If no cache hit, process the query using the conversational chain.
    res = await global_chain.ainvoke(user_query)
    answer = res["answer"]
    source_documents = res["source_documents"]

    text_elements = []  # Prepare to display any related documents.
    source_info = ""

    # If documents are related to the answer, format them for display.
    if source_documents:
        for source_idx, source_doc in enumerate(source_documents):
            source_name = f"source_{source_idx}"
            text_elements.append(cl.Text(content=source_doc.page_content, name=source_name))
        source_names = [text_el.name for text_el in text_elements]
        source_info = f"\nSources: {', '.join(source_names)}" if source_names else "\nNo sources found"

    # Combine the answer and source information.
    full_response = answer + source_info
    # Cache the new response to handle future identical queries efficiently.
    redis_client.set(user_query, full_response)

    # Send the final response to the user.
    await cl.Message(content=full_response, author="Iconcern", elements=text_elements).send()
