from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage
from typing import TypedDict, List
from pydantic import BaseModel, ValidationError, Field

class HumanMessageModel(BaseModel):
    content: str

class StateSchema(BaseModel):
    messages: List[HumanMessageModel] = Field(...)

embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = Chroma(persist_directory="./Smart-Library/app/llama/chromadb", embedding_function=embeddings)
llm = Ollama(model="llama3.1", temperature=0)
retriever = vectorstore.as_retriever(top_k=3)


prompt = PromptTemplate(
    template="""
    As a highly knowledgeable librarian good at searching documents, your role is to accurately answer book questions 
    with only the use of the data given to you from the collection of book titles and descriptions using our specialized book database. \n
    You are an expert at routing a user question to a vectorstore. \n
    Use the vectorstore for questions on LLM  agents, prompt engineering, and adversarial attacks. \n
    You do not need to be stringent with the keywords in the question related to these topics. \n
    Otherwise, tell the user you don't have what they're looking for. \n
    Do not suggest any books outside of our database \n

    Book Query:
    {context}

    Question to route: 
    {question}""",
    input_variables=["context","question"],
)

question_router = prompt | llm


store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

retriever=vectorstore.as_retriever(top_k=3)

rag_chain = RetrievalQA.from_chain_type(
    llm=llm, 
    chain_type="stuff", 
    retriever=retriever, 
    chain_type_kwargs={"prompt": prompt})

conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",
)


def get_response(question):
    result = rag_chain({"query": question})
    response_text = result["result"]
    answer_start = response_text.find("Answer:") + len("Answer:")
    answer = response_text[answer_start:].strip()
    return answer

# define intents as tools

@tool
def book_recommendation_chat(state: StateSchema):
    """Provides a book recommendation in chat format."""
    question = state.messages[-1].content
    answer = get_response(question)
    return {"messages": [HumanMessageModel(content=answer)]}

@tool
def book_recommendation_json(state: StateSchema):
    """Provides a book recommendation in JSON format."""
    question = state.messages[-1].content
    docs = retriever.get_relevant_documents(question)
    books_info = [{"title": doc.metadata['title'], "author": doc.metadata['authors']} for doc in docs]
    return {"messages": [HumanMessageModel(content=str(books_info))]}

@tool
def books_by_author(state: StateSchema):
    """Provides a list of books by a specific author."""
    author = state.messages[-1].content
    docs = retriever.get_relevant_documents(f"author: {author}")
    books_info = [{"title": doc.metadata['title'], "author": doc.metadata['authors']} for doc in docs]
    return {"messages": [HumanMessageModel(content=str(books_info))]}

@tool
def books_by_year(state: StateSchema):
    """Provides a list of books published in a specific year."""
    year = state.messages[-1].content
    docs = retriever.get_relevant_documents(f"published year: {year}")
    books_info = [{"title": doc.metadata['title'], "author": doc.metadata['authors']} for doc in docs]
    return {"messages": [HumanMessageModel(content=str(books_info))]}

@tool
def books_by_rating(state: StateSchema):
    """Provides a list of books with a specific rating."""
    rating = state.messages[-1].content
    docs = retriever.get_relevant_documents(f"rating: {rating}")
    books_info = [{"title": doc.metadata['title'], "author": doc.metadata['authors']} for doc in docs]
    return {"messages": [HumanMessageModel(content=str(books_info))]}

@tool
def determine_intent(state: StateSchema):
    """Determines the user's intent based on the message content."""
    message = state.messages[-1].content.lower()
    if "chat" in message:
        return "book_recommendation_chat"
    elif "json" in message:
        return "book_recommendation_json"
    elif "author" in message:
        return "books_by_author"
    elif "year" in message:
        return "books_by_year"
    elif "rating" in message:
        return "books_by_rating"
    elif "add" in message:
        return "add_book"
    else:
        return END

# defining the workflow and nodes
workflow = StateGraph(StateSchema)
    
workflow.add_node("determine_intent", determine_intent)
workflow.add_node("book_recommendation_chat", book_recommendation_chat)
workflow.add_node("book_recommendation_json", book_recommendation_json)
workflow.add_node("books_by_author", books_by_author)
workflow.add_node("books_by_year", books_by_year)
workflow.add_node("books_by_rating", books_by_rating)
    
workflow.set_entry_point("determine_intent")
workflow.add_conditional_edges("determine_intent", determine_intent)

checkpointer = MemorySaver()
app = workflow.compile(checkpointer=checkpointer)

# question = "books about magic"
# context= retriever
# docs = get_response(question)
# # doc_txt = docs[1].page_content
# print(question_router.invoke({"context": context,"question": question}))

initial_state = StateSchema(messages=[HumanMessageModel(content="I want a book recommendation chat about magic")])
try:
    final_state = app.invoke(initial_state, config={"configurable": {"thread_id": 42}})
    print(final_state["messages"][-1].content)
except ValidationError as e:
    print(f"Validation error: {e}")
