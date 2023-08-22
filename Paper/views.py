from django.shortcuts import render
from langchain import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
import os
from dotenv import load_dotenv
from .utils import get_text, summarize_and_create_vectordb, get_llm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

# Load the env
load_dotenv()
openai_api_key = os.getenv("OPENAI_KEY")


messages = [
    (
        "Bot",
        "👋 Hello there! As your personal document assistant, I'm here to assist you with any document-related needs you may have. How can I help you today?",
    ),
]


# Create your views here.
@csrf_exempt
def chatpaper(request, url):
    url = "https://arxiv.org/pdf/" + url

    # query = request.data["query"]

    data = json.loads(request.body)

    # query = data.get("query", "")
    query = data["query"]

    if query == "":
        text = get_text(url)
        summary = summarize_and_create_vectordb(text, openai_api_key)
        print(summary)
        return JsonResponse({"summary": summary})

    # text = get_text(url)

    # summary = summarize_and_create_vectordb(text, openai_api_key)

    # Get the embeddings for similarity search
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

    # Load the vector store for similarity search
    new_db = FAISS.load_local("faiss_index", embeddings)

    # Perform similarity search on the query
    docs = new_db.similarity_search(query, k=2)

    # Get the language model for question answering
    llm = get_llm(openai_api_key=openai_api_key)

    # Load the question answering chain
    chain = load_qa_chain(llm, chain_type="stuff")

    # Perform question answering on the input documents
    answer = chain.run(input_documents=docs, question=query)

    # # Add the user query and bot response to the messages list
    # messages.append(("You", f"{query}"))
    # messages.append(("Bot", f"{response}"))

    return JsonResponse({"answer": answer})
