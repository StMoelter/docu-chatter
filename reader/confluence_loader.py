from langchain.document_loaders import ConfluenceLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import AzureOpenAIEmbeddings
from langchain.vectorstores import Weaviate
from datetime import datetime, timezone, timedelta

import re, os, pickle, nest_asyncio
import pdb

nest_asyncio.apply()

cache_file = "../tmp/confluence.pickle"
confluence_key = "GIGD"


def fetch_data():
    if os.path.isfile(cache_file):
        filehandler = open(cache_file, "rb")
        raw_documents = pickle.load(filehandler)
    else:
        loader = ConfluenceLoader(url="https://confluence.sumcumo.net", cloud=False)
        loader.confluence._session.cookies.set(
            "JSESSIONID",
            os.environ["CONFLUENCE_JSESSION_ID"],
            domain="confluence.sumcumo.net",
        )
        raw_documents = loader.load(space_key=confluence_key, include_attachments=False)
        file = open(cache_file, "wb")
        pickle.dump(raw_documents, file)

    print(f"loaded {len(raw_documents)} documents")
    for doc in raw_documents:
        doc.page_content = re.sub(r"\s+", " ", doc.page_content)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    documents = text_splitter.split_documents(raw_documents)
    # pdb.set_trace()
    for doc in documents:
        doc.metadata['confluence_id']= doc.metadata.pop('id')

    embeddings = AzureOpenAIEmbeddings(
        azure_endpoint=os.environ["AZURE_ENDPOINT"],
        openai_api_key=os.environ["AZURE_KEY"],
        azure_deployment=os.environ["AZURE_EMBEDDING_DEPLOYMENT"],
        openai_api_version=os.environ["AZURE_VERSION"],
    )

    print(f"Going to add {len(documents)} to Weaviate")
    Weaviate.from_documents(documents, embeddings, weaviate_url="http://127.0.0.1:8081")
    print("****Loading to vectorestore done ***")


if __name__ == "__main__":
    fetch_data()
