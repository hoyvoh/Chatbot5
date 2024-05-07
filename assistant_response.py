import requests
from bs4 import BeautifulSoup
import pandas as pd
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_core.documents.base import Document
from langchain.vectorstores.faiss import FAISS
import os
import time
import json

os.environ["HUGGINGFACEHUB_API_TOKEN"] = "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"
os.environ["LANGCHAIN_API_KEY"] = "ls__f23a410c23034fd4a322211dec10f26f"
os.environ['CURL_CA_BUNDLE'] = ''
AWANLM_API_KEY = "0e2205fc-c3cb-4499-9298-63379d721d1b"

main_url = "https://huggingface.co/docs/transformers/index"
parse_url = "https://huggingface.co/docs/transformers/{}"

import torch
from torch import cuda, bfloat16
from typing import Any

# get list of models and links
def get_links_and_names(url):
    response = requests.get(url)
    d = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.find_all('tr')
        for r in rows:
            a_tag = r.find('a')
            if a_tag:
                link = a_tag.attrs['href']
                title = a_tag.text.lower()
                if link and title:
                    #print("{} | {}".format(title, link))
                    loader = WebBaseLoader(parse_url.format(link))
                    document = loader.load()

                    line = {"title":title, "link":link, "document": document}
                    d.append(line)
    return d

def keyword_store():
    context = pd.read_csv("page_index_2.csv")
    context = context['title'].tolist()
    embeddings = HuggingFaceEmbeddings()
    vector_store = FAISS.from_texts(context, embeddings)
    return vector_store

def keyword_search(query, vector_store):
    retriever = vector_store.as_retriever()
    results = retriever.invoke(query)
    return results

links_and_names = pd.read_csv("page_index_2.csv")
list_of_linksandnames = []
for i, row in links_and_names.iterrows():
    list_of_linksandnames.append(row)
# print(list_of_linksandnames[0]['title'])

def context_fetching(doc, query):
    start = time.time()
    document = [Document(doc)]

    text_splitter = RecursiveCharacterTextSplitter(
    separators=[
        "\n\n",
        "\n",
        " ",
        ".",
        ",",
        "\u200B",  # Zero-width space
        "\uff0c",  # Fullwidth comma
        "\u3001",  # Ideographic comma
        "\uff0e",  # Fullwidth full stop
        "\u3002",  # Ideographic full stop
        "",
    ],
    chunk_size=1000,
    chunk_overlap=200
    # Existing args
    )
    splitted_doc = text_splitter.split_documents(document)
    
    embeddings = HuggingFaceEmbeddings()
    vector_store = FAISS.from_documents(splitted_doc, embeddings)
    retriever = vector_store.as_retriever()
    results = retriever.invoke(query) # config top contexts here
    end = time.time()
    print("Context fetched from context_fetching in: {}s".format(end-start))
    return results, vector_store

url = "https://api.awanllm.com/v1/chat/completions"

def get_ans_from_api(user_query, context):
    start = time.time()
    model_name = "Meta-Llama-3-8B-Instruct-Dolfin-v0.1"
    payload = json.dumps({
    "model": "{}".format(model_name),
    "messages": [
        {"role":"system",
        "content": "You are iRobin, a friendly assistant to a student. Use the following information to answer the user's question. In case you don't know the answer, just say that you don't know, don't try to make up an answer. Related information for you: {}".format(context)},
        {"role": "user",
        "content": "{}".format(user_query)}
        ]
    })   
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {AWANLM_API_KEY}"
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    response_json = response.json()
    result = response_json['choices'][0]['message']['content']
    end = time.time()
    print("Answer is returned at get_ans_from_api after {}s".format(end-start))
    print(result)
    return result

def get_response(query, need_context):
    start = time.time()
    query = query.lower()
    keywords = keyword_store()
    top_results = keyword_search(query, keywords)
    query_key = str(top_results[0].page_content)
    # Find query link

    doc = [res['document'] for res in list_of_linksandnames if res['title'] == query_key]
    # get context
    context = context_fetching(doc[0], query)
    response = get_ans_from_api(query, context)

    end = time.time()
    print("Response is returned at get_response after: {}s".format(str(end-start)))

    return response

if __name__ == "__main__":
    start = time.time()
    
    query = "Can you tell me about albert?"
    query = query.lower()

    response = get_response(query)

    end = time.time()
    print("Enlapsed time: {}s".format(end-start))