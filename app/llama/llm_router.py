from fastapi import APIRouter, Depends, HTTPException
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

class CustomStrOutputParser(StrOutputParser):
     def parse(self, text: str) -> str:
        cleaned_text = text.strip('"')
        cleaned_text = cleaned_text.replace('\\n', '<br>')  # Convert newlines to HTML line breaks
        cleaned_text = re.sub(r'["*]', '', cleaned_text)
        cleaned_text = cleaned_text.strip()
        return cleaned_text

embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = Chroma(persist_directory="./Smart-Library/app/llama/chromadb", embedding_function=embeddings)
llm = Ollama(model="llama3.1", temperature=0)
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

custom_parser = CustomStrOutputParser()

rag_chain = RetrievalQA.from_chain_type(
    llm=llm, 
    chain_type="stuff", 
    retriever=retriever, 
    chain_type_kwargs={"prompt": prompt})

def get_response(question):
    result = rag_chain({"query": question})
    response_text = result["result"]
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
    response_text = get_response(user_query)
    return response_text

