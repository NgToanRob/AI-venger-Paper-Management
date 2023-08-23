from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import AzureChatOpenAI
from io import BytesIO
import requests
import PyPDF2
import os


def get_llm():
    llm = AzureChatOpenAI(
        openai_api_base=os.environ.get("OPENAI_API_BASE"),
        openai_api_version=os.environ.get("OPENAI_API_VERSION"),
        deployment_name=os.environ.get("OPENAI_DEPLOYMENT_NAME"),
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
        openai_api_type=os.environ.get("OPENAI_API_TYPE"),
    )
    return llm


def get_text(pdf_url: str):
    try:
        response = requests.get(pdf_url)
        pdf_bytes = BytesIO(response.content)
        pdf_reader = PyPDF2.PdfReader(pdf_bytes)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        return text
    except requests.exceptions.RequestException as e:
        print("Error fetching the PDF:", e)
        return None


def summarize_and_create_vectordb(input_text: str):
    # Split the input text into chunks for processing
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n"], chunk_size=5000, chunk_overlap=500
    )

    # Get the language model for summarization
    llm = get_llm()

    # Create document objects from the input text
    docs = text_splitter.create_documents([input_text])

    # Load the summarization chain
    summary_chain = load_summarize_chain(
        llm=llm,
        chain_type="map_reduce",
        verbose=False,  # Set verbose=True if you want to see the prompts being used
    )

    # Generate the summary
    result = summary_chain.run(docs)

    embeddings = HuggingFaceEmbeddings()

    # Create a vector store for similarity search
    db = FAISS.from_documents(docs, embeddings)

    # Save the vector store locally
    db.save_local("faiss_index")

    return result
