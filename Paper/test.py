import openai
import os
from dotenv import load_dotenv
from langchain.llms import AzureOpenAI

load_dotenv()
openai_api_key = os.getenv("OPENAI_KEY")
os.environ["OPENAI_API_TYPE"] = "azure"
os.environ["OPENAI_API_BASE"] = "https://bootcamp-gpt-ae.openai.azure.com/"
os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["OPENAI_API_VERSION"] = "2023-05-15"

# # openai.api_key = openai_api_key
# # openai.api_base = "https://bootcamp-gpt-ae.openai.azure.com/"  # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
# # openai.api_type = "azure"
# # openai.api_version = "2023-05-15"  # this may change in the future
# llm = AzureOpenAI(
#     temperature=0,
#     openai_api_key=openai_api_key,
#     deployment_name="bootcamp-chatgpt",
#     model_name="gpt-4",
# )

# print(llm("hello"))


import os
import requests
import json
import openai

# openai.api_key = openai_api_key
# openai.api_base = "https://bootcamp-gpt-ae.openai.azure.com"  # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
# openai.api_type = "azure"
# openai.api_version = "2023-05-15"  # this may change in the future
deployment_name = "bootcamp-chatgpt"  # This will correspond to the custom name you chose for your deployment when you deployed a model.
# response = openai.ChatCompletion.create(
#     engine=deployment_name,  # replace this value with the deployment name you chose when you deployed the associated model.
#     messages=[],
#     temperature=0,
#     max_tokens=350,
#     top_p=0.95,
#     frequency_penalty=0,
#     presence_penalty=0,
#     stop=None,
# )
# print(response("hello asdasdasdasd"))

from langchain.embeddings import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(
    deployment=deployment_name, model="text-embedding-ada-002"
)

text = "This is a test document."
query_result = embeddings.embed_query(text)
doc_result = embeddings.embed_documents([text])

print(query_result)
