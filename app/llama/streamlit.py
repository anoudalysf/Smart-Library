import streamlit as st
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from fastapi import FastAPI
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


app = FastAPI()

st.header("Books Books Books!")

embeddings = OllamaEmbeddings(model="nomic-embed-text")
db = Chroma(persist_directory="./Users/aalyousef001/My_Smart_Library/Smart-Library/app/llama/chromadb", embedding_function=embeddings)
llm = Ollama(model="llama3.1")


prompt_template = """
As a highly knowledgeable librarian good at searching documents, your role is to accurately answer book questions with only the use of the data given to you 
from the collection of book titles and descriptions using our specialized book database.
Do not suggest any books outside of our database 

have it get context from the queries

Book Query:
{context}

Question: {question}

Answer:
"""

# prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             "You're a helpful AI assistant that answers based on the question: {question}.",
#             # "Question: {question}"
#         ),
#         MessagesPlaceholder(variable_name="history"),
#         ("human", "{question}"),
#     ]
# )

# prompt_template = """
# You are a helpfull AI assistant
# Question: {question}

# Answer:
# """

# runnable = prompt | llm


store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

custom_prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

rag_chain = RetrievalQA.from_chain_type(
    llm=llm, 
    chain_type="stuff", 
    retriever=db.as_retriever(top_k=3), 
    chain_type_kwargs={"prompt": prompt_template})

# with_message_history = RunnableWithMessageHistory(
#     runnable,
#     get_session_history,
#     input_messages_key="question",
#     history_messages_key="history",
#     # output_messages_key="answer",
# )


# def get_response(question):
#     result = rag_chain({"query": question})
#     response_text = result["result"]
#     answer_start = response_text.find("Answer:") + len("Answer:")
#     answer = response_text[answer_start:].strip()
#     return answer

def get_response(question, filters=None):
    retriever = db.as_retriever(top_k=3)
    
    if filters:
        retriever = retriever.with_filters(filters)

    rag_chain = RetrievalQA.from_chain_type(
        llm=llm, 
        chain_type="stuff", 
        retriever=retriever, 
        chain_type_kwargs={"prompt": custom_prompt}
    )
    
    result = rag_chain({"query": question})
    response_text = result["result"]
    answer_start = response_text.find("Answer:") + len("Answer:")
    answer = response_text[answer_start:].strip()
    return answer


with st.chat_message("user"):
    st.write("Hello 👋")

prompt = st.chat_input("Say something")
if prompt:
    response=get_response(prompt)
    st.write(f"User: {prompt}")
    # with_message_history.invoke(
    #     {"question": {prompt}},
    #     config={"configurable": {"session_id": 1}},
    #     )
    with st.chat_message("user"):
        st.write(response)

