from fastapi import APIRouter, Depends, HTTPException
from langchain_ollama import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from langgraph.graph import END, StateGraph, START
from typing_extensions import TypedDict
from typing import List
import re
from langchain_ollama import OllamaLLM
from pydantic import BaseModel, Field

class IntentResponseModel(BaseModel):
    intent_number: int = Field(description="The intent number ranging from 1 to 7")
    metadata: str = Field(description="The extracted entity related to the intent")


class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: question
        generation: LLM generation
        documents: list of documents
    """

    question: str
    generation: str
    documents: List[str]

embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = Chroma(persist_directory="./Smart-Library/app/llama/chromadb", embedding_function=embeddings)
llm = ChatOllama(model="llama3.1", temperature=0)
retriever = vectorstore.as_retriever(top_k=3)


class IntentExtractor:
    def __init__(self, model_name="llama3.1"):
        self.llm = OllamaLLM(model=model_name)

    def classify_intent_and_extract_entities(self, document: str) -> IntentResponseModel:
        prompt_message = (f"""
            You are an AI assistant that classifies user intents based on their queries related to books.

            Please read the user's query below and identify the correct intent. Your response must include the intent number and relevant metadata (like a book title, author name, or category).

            User Query: "{document}"

            Classify the user's intent into one of the following categories and provide the corresponding intent number and metadata:
            
            0. General inquiry: The user asks a general question not specific to a category, author, or year.
            1. Author Retrieval: The user asks for books by a specific author.
            2. Category Retrieval: The user asks for books in a specific category.
            3. Year Retrieval: The user asks for books published in a specific year.
            4. Ratings Retrieval: The user asks for books by their average ratings.
            5. Recommendation: The user will ask for a recommendation, or ask to recommend a book/series similar to another seperate book/series.
            6. Book Retrieval: The user will ask you to just give/return them a specific book.
            7. Summarizer: The user will ask you to talk about or give them a summary of a book or book series, summarize or describe it to the best of your abilities.

            Respond in the following format:
            Intent Number: [0-7]
            Metadata: [Relevant Metadata]
            """
        )

        response = self.llm.invoke(prompt_message).strip()
        print(f"LLM Response:\n{response}")

        intent_match = re.search(r"Intent Number: (\d+)", response)
        metadata_match = re.search(r"Metadata: ([^\n]+)", response)

        if intent_match:
            intent_number = int(intent_match.group(1))
            print(f"Extracted Intent Number: {intent_number}") #debugging
        else:
            intent_number = 0
            print("Failed to extract intent number. Defaulting to 0.")  #debugging

        metadata = metadata_match.group(1).strip() if metadata_match else ""
        print(f"Extracted Metadata: {metadata}")  #debugging

        return IntentResponseModel(
            intent_number=intent_number,
            metadata=metadata
        )


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

answer_grader = prompt | llm | StrOutputParser()

rag_chain = RetrievalQA.from_chain_type(
    llm=llm, 
    chain_type="stuff", 
    retriever=retriever, 
    chain_type_kwargs={"prompt": prompt})

##### NODES #####

def retrieve(state):
    """
    Retrieve documents

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, documents, that contains retrieved documents
    """
    print("---RETRIEVE---")
    question = state["question"]

    documents = retriever.get_relevant_documents(question)
    return {"documents": documents, "question": question}


def generate(state):
    """
    Generate answer

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, generation, that contains LLM generation
    """
    print("---GENERATE---")
    question = state["question"]
    documents = state["documents"]

    response = rag_chain.invoke({"query": question, "context": documents})
    # return {"documents": documents, "question": question, "generation": generation}
    generation = response["result"] if isinstance(response, dict) else response

    return {"documents": documents, "question": question, "generation": generation}


def search_by_category(state):
    """
    Search for books by category.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updates documents key with relevant books in the specified category
    """
    print("---SEARCH BY CATEGORY---")
    question = state["question"]
    intent_extractor = IntentExtractor()
    intent_response = intent_extractor.classify_intent_and_extract_entities(question)
    state["metadata"] = intent_response.metadata

    category = state["metadata"]
    documents = retriever.get_relevant_documents(category)
    
    return {"documents": documents, "question": state["question"]}


def search_by_author(state):
    """
    Search for books by a specific author.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updates documents key with relevant books by the specified author
    """
    print("---SEARCH BY AUTHOR---")
    question = state["question"]
    intent_extractor = IntentExtractor()
    intent_response = intent_extractor.classify_intent_and_extract_entities(question)
    state["metadata"] = intent_response.metadata

    author = state["metadata"]
    documents = retriever.get_relevant_documents(author)
    
    return {"documents": documents, "question": state["question"]}


def search_by_published_year(state):
    """
    Search for books by a specific publish year.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updates documents key with relevant books by the specified publish year
    """
    print("---SEARCH BY PUBLISHED YEAR---")
    question = state["question"]
    intent_extractor = IntentExtractor()
    intent_response = intent_extractor.classify_intent_and_extract_entities(question)
    state["metadata"] = intent_response.metadata

    year = state["metadata"]
    documents = retriever.get_relevant_documents(year)
    
    return {"documents": documents, "question": state["question"]}


def search_by_average_rating(state):
    """
    Search for books by their average rating.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updates documents key with relevant books by the average rating
    """
    print("---SEARCH BY AVERAGE RATING---")
    question = state["question"]
    intent_extractor = IntentExtractor()
    intent_response = intent_extractor.classify_intent_and_extract_entities(question)
    state["metadata"] = intent_response.metadata

    rating = state["metadata"]
    documents = retriever.get_relevant_documents(rating)
    
    return {"documents": documents, "question": state["question"]}


def recommendation(state):
    """
    Recommend a book to the user.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updates documents key with relevant book recommendations
    """
    print("---RECOMMENDATION---")
    recommendation = state["question"]
    documents = retriever.get_relevant_documents(recommendation)
    
    return {"documents": documents, "question": state["question"]}


# def book_retrieval(state):
#     """
#     Retrieve a book to the user in tabular format.

#     Args:
#         state (dict): The current graph state

#     Returns:
#         state (dict): Updates documents key with relevant book retrieval
#     """
#     print("---BOOK RETRIVAL---")
#     recommendation = state["question"]
#     documents = retriever.get_relevant_documents(recommendation)
    
#     return {"documents": documents, "question": state["question"]}

import pandas as pd

def book_retrieval(state):
    """
    Retrieve a book to the user in tabular format.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updates documents key with relevant book retrieval in tabular format
    """
    print("---BOOK RETRIEVAL---")

    query = state.get("metadata", state["question"])
    documents = retriever.get_relevant_documents(query)
    
    if documents:
        output = ""
        for doc in documents:
            metadata = doc.metadata
            output += f"**Title**: {metadata.get('title', 'N/A')}\n"
            output += f"**Authors**: {metadata.get('authors', 'N/A')}\n"
            output += f"**Published Year**: {metadata.get('published_year', 'N/A')}\n"
            output += f"**Average Rating**: {metadata.get('average_rating', 'N/A')}\n"
            output += f"**Number of Pages**: {metadata.get('num_pages', 'N/A')}\n"
            output += f"**Categories**: {metadata.get('categories', 'N/A')}\n"
            output += f"**Description**: {metadata.get('description', 'N/A')}\n"
            output += "\n"  #add a new line between for when there aer different books

        return {"documents": documents, "question": state["question"], "generation": output.strip()}
    else:
        return {"documents": documents, "question": state["question"], "generation": "Sorry, no relevant books found."}


def summarizer(state):
    """
    Summarize a book on the provided metadata.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updates documents key with relevant book summary
    """
    print("---SUMMARY---")
    question = state["question"]
    intent_extractor = IntentExtractor()
    intent_response = intent_extractor.classify_intent_and_extract_entities(question)
    state["metadata"] = intent_response.metadata

    summary = state["metadata"]
    documents = retriever.get_relevant_documents(summary)

    primary_document = documents[0]
    summary_context = primary_document.page_content
    

    summary_prompt = f"""
    Based on the user's query, provide a detailed and coherent summary of the book or series. Summarize or describe it to the best of your abilities:

    {summary_context}

    Summary:
    """

    response = llm.invoke(summary_prompt)
    summary = response.content.strip()
    
    return {"documents": documents, "question": state["question"], "generation": summary}
    # state["generation"] = summary
    # return state


# def update_state(state, intent_number, metadata):
#     state["intent_number"] = intent_number
#     state["metadata"] = metadata
#     return state


def decide_intent(state):
    """
    Decide the user's intent based on their question.

    Args:
        state (dict): The current graph state

    Returns:
        str: The next node to call based on the detected intent
    """
    question = state["question"].lower()
    
    intent_extractor = IntentExtractor()
    intent_response = intent_extractor.classify_intent_and_extract_entities(question)

    print(f"Detected Intent Number: {intent_response.intent_number}")
    print(f"Detected Metadata: {intent_response.metadata}")

    state["intent_number"] = intent_response.intent_number
    state["metadata"] = intent_response.metadata
    # print("Before setting state:")
    # print(state)

    # state = update_state(state, intent_response.intent_number, intent_response.metadata)

    # print("State after setting intent and metadata in decide_intent:")
    # print(state)


    if intent_response.intent_number == 1:
        print("---DECISION: SEARCH BY AUTHOR---")
        return "search_by_author"
    elif intent_response.intent_number == 2:
         print("---DECISION: SEARCH BY CATEGORY---")
         return "search_by_category"
    elif intent_response.intent_number == 3:
        print("---DECISION: SEARCH BY PUBLISHED YEAR---")
        return "search_by_published_year"
    elif intent_response.intent_number == 4:
        print("---DECISION: SEARCH BY AVERAGE RATING---")
        return "search_by_average_rating"
    elif intent_response.intent_number == 5:
        print("---DECISION: RECOMMENDATION---")
        return "recommendation"
    elif intent_response.intent_number == 6:
        print("---DECISION: BOOK RETRIVAL---")
        return "book_retrieval"
    elif intent_response.intent_number == 7:
        print("---DECISION: SUMMARY---")
        return "summarizer"
    else:
        print("---DECISION: GENERATE ANSWER---")
        return "generate"

workflow = StateGraph(GraphState)

workflow.add_node("retrieve", retrieve) 
workflow.add_node("generate", generate)
workflow.add_node("search_by_category", search_by_category)
workflow.add_node("search_by_author", search_by_author)
workflow.add_node("search_by_published_year", search_by_published_year)
workflow.add_node("search_by_average_rating", search_by_average_rating)
workflow.add_node("recommendation", recommendation)
workflow.add_node("book_retrieval", book_retrieval)
workflow.add_node("summarizer", summarizer)



##### EDGES #####

workflow.add_edge(START, "retrieve")
# workflow.add_edge("retrieve", "generate")
workflow.add_conditional_edges(
    "retrieve", decide_intent,
    {
        "search_by_category": "search_by_category",
        "search_by_author": "search_by_author",
        "search_by_published_year": "search_by_published_year",
        "search_by_average_rating":"search_by_average_rating",
        "recommendation":"recommendation",
        "book_retrieval":"book_retrieval",
        "summarizer":"summarizer",
        "generate": "generate",
    },
)

workflow.add_edge("search_by_category", "generate")
workflow.add_edge("search_by_author", "generate")
workflow.add_edge("search_by_published_year", "generate")
workflow.add_edge("search_by_average_rating", "generate")
workflow.add_edge("recommendation", "generate")
workflow.add_edge("book_retrieval", END)
workflow.add_edge("summarizer", END)


app = workflow.compile()


# from pprint import pprint

# inputs = {"question": "talk to me about the book Harry Potter the order of the phoenix"}
# for output in app.stream(inputs):
#     for key, value in output.items():
#         pprint(f"Node '{key}':")
#     pprint("\n---\n")

# # Final generation
# pprint(value["generation"])


# async def get_response(question):
#     result = rag_chain({"query": question})
#     response_text = result["result"]
#     answer_start = response_text.find("Answer:") + len("Answer:")
#     answer = response_text[answer_start:].strip()
#     return answer