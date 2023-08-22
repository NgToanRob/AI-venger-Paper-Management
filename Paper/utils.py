from langchain import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import requests
from io import BytesIO
import PyPDF2


def get_llm(openai_api_key, temperature=0):
    """
    Get the Language Model from OpenAI.

    Args:
    - openai_api_key: The OpenAI API key.
    - temperature: The temperature parameter for text generation (default: 0).

    Returns:
    - The Language Model.
    """
    llm = OpenAI(temperature=temperature, openai_api_key=openai_api_key)
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


def summarize_and_create_vectordb(input_text: str, openai_api_key: str):
    # Split the input text into chunks for processing
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n"], chunk_size=5000, chunk_overlap=500
    )

    # Get the language model for summarization
    llm = get_llm(openai_api_key=openai_api_key)

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

    # Get the embeddings for the documents
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

    # vectors = embeddings.embed_documents([x.page_content for x in docs])

    # Create a vector store for similarity search
    db = FAISS.from_documents(docs, embeddings)

    # Save the vector store locally
    db.save_local("faiss_index")

    return result
