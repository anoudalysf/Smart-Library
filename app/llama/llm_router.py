import uuid
from fastapi import APIRouter, Depends, HTTPException
from langchain_ollama import ChatOllama
from sqlalchemy.orm import Session
import pandas as pd
from app.common.config.database import get_db
from app.Books import books_crud  
from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from app.Books import books_model, books_schema
from langchain_core.output_parsers import StrOutputParser
import re
import asyncio
from fastapi.responses import StreamingResponse
from typing_extensions import TypedDict
from testintent import app as intent_app


class CustomStrOutputParser(StrOutputParser):
     def parse(self, text: str) -> str:
        cleaned_text = text.strip('"')
        cleaned_text = cleaned_text.replace('\\n', '<br>')
        cleaned_text = re.sub(r'["*]', '', cleaned_text)
        cleaned_text = cleaned_text.strip()
        return cleaned_text

embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = Chroma(persist_directory="./Smart-Library/app/llama/chromadb", embedding_function=embeddings)
llm = ChatOllama(model="llama3.1", temperature=0)
retriever = vectorstore.as_retriever(top_k=3)


prompt = PromptTemplate(
    template="""
    As a highly knowledgeable librarian good at searching documents, your role is to accurately answer book questions 
    with only the use of the data given to you from the collection of book titles and descriptions using our specialized book database. \n
    Make the user feel comfortable and lightly converse when needed. \n
    You are an expert at routing a user question to a vectorstore. \n
    You do not need to be stringent with the keywords in the question related to these topics. \n
    Otherwise, tell the user you don't have what they're looking for. \n
    Do not suggest any books outside of our database \n
    Provide the results in plain text without any additional formatting or special characters unless it's part of the book information. \n

    Book Query:
    {context}

    Question to route: 
    {question}""",
    input_variables=["context","question"],
)

# async def stream_response(question: str):
#     async for chunk in rag_chain.astream({"query": question}):
#         yield chunk["result"] + "AAAA"

async def stream_response(question: str):
    async for chunk in rag_chain.astream({"query": question}):
        text = chunk["result"]
        for i in range(0, len(text), 100):
            yield text[i:i +100] + "AAAA"

custom_parser = CustomStrOutputParser()

rag_chain = RetrievalQA.from_chain_type(
    llm=llm, 
    chain_type="stuff", 
    retriever=retriever, 
    chain_type_kwargs={"prompt": prompt})

async def get_response(question):
    result = rag_chain({"query": question})
    response_text = result["result"]
    # async for chunk in llm.astream(result["result"]):
    #             print(chunk.content)
    parsed_text = custom_parser.parse(response_text)
    print(parsed_text)
    return parsed_text
    # answer_start = response_text.find("Answer:") + len("Answer:")
    # answer = parsed_text[answer_start:].strip()
    # return answer


app = APIRouter()

@app.post("/add-books")
def add_books_to_db_and_chroma(file_path: str, db: Session = Depends(get_db)):
    try:
        df = pd.read_csv(file_path)
        
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        chroma_db = Chroma(persist_directory="/Users/aalyousef001/My_Smart_Library/Smart-Library/app/llama/chromadb", embedding_function=embeddings)
        
        for _, row in df.iterrows():
            book_data = row.to_dict()
            books_crud.create_book(db, book_data, embeddings, persist_directory='/Users/aalyousef001/My_Smart_Library/Smart-Library/app/llama/chromadb')
        
        return {"message": "Books added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/similarity", response_model=list[books_schema.Books], tags=["chat"])
def similarity_search(query: str,  db: Session = Depends(get_db)):
    # return retriever.invoke(query)
    vector_results = retriever.invoke(query)
    titles = [result.metadata["title"] for result in vector_results]
    books = db.query(books_model.Book).filter(books_model.Book.title.in_(titles)).all()
    return books


@app.get("/chat_with_bot", response_model=str, tags=["chat"])
async def chat_with_bot_endpoint(user_query: str, db: Session = Depends(get_db)):
    # response_text = get_response(user_query)
    # return response_text
    return StreamingResponse(stream_response(user_query), media_type="text/plain", headers={"Content-Encoding": "identity"})

async def simple_stream_response():
    for i in range(5):
        yield f"Chunk {i}\n"
        await asyncio.sleep(1)  # Simulate delay between chunks

@app.get("/test_stream")
async def test_stream():
    return StreamingResponse(simple_stream_response(), media_type="text/plain")


def generate_session_id():
    return str(uuid.uuid4())

@app.post("/chat_with_intents", response_model=str, tags=["chat"])
async def chat_with_intents(user_query: str, session_id: str = Depends(generate_session_id)):
    state = {"question": user_query, "generation": "", "documents": []}
    config = {"configurable": {"thread_id": session_id}}

    for output in intent_app.stream(state, config):
        final_state = output
        # print("Final State:", final_state)

    generation = None
    for key, value in final_state.items():
        if isinstance(value, dict) and "generation" in value:
            generation = value["generation"]
            break
    
    if not generation:
        raise HTTPException(status_code=500, detail="No generation found in the final state.")
    
    #ensure the generation is a string, check if its a dict if it is get the result part from it only
    if isinstance(generation, dict) and "result" in generation:
        generation = generation["result"]

    async def stream_chunks():
        chunk_size = 20  # Adjust this to control the size of each chunk
        for i in range(0, len(generation), chunk_size):
            yield generation[i:i + chunk_size]
            await asyncio.sleep(0.1)

    # return generation
    return StreamingResponse(stream_chunks(), media_type="text/plain", headers={"Content-Encoding": "identity"})
