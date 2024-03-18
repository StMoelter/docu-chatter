from langchain.document_loaders.sitemap import SitemapLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OllamaEmbeddings
from langchain.vectorstores import Weaviate
import re, os, pickle, nest_asyncio

from langchain.embeddings import OpenAIEmbeddings

import pdb

from dotenv import load_dotenv
load_dotenv(f"{os.path.dirname(__file__)}/../.env")

nest_asyncio.apply()

header_template = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "en-US,en;q=0.9,de-DE;q=0.8,de;q=0.7,en-DE;q=0.6",
    "Accept-Encoding": "gzip, deflate",
    "Referer": "https://www.google.com/",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

# https://rubyonrails.org/sitemap.xml
"""
sitemap_uri = "https://documentation.scip.sumcumo.net/sitemap.xml"
cache_file = "/Users/steffenmoelter/workspace/vendor/docu-chatter/tmp/scip-docu.pickle"

"""


sitemap_uri = "https://rubyonrails.org/sitemap.xml"
cache_file = "/Users/steffen/workspace/vendor/docu-chatter/tmp/ror.pickle"


def fetch_data():
    if os.path.isfile(cache_file):
        filehandler = open(cache_file, "rb")
        raw_documents = pickle.load(filehandler)
    else:
        sitemap_loader = SitemapLoader(
            web_path=sitemap_uri, 
            header_template=header_template,
            continue_on_failure=True,
        )
        sitemap_loader.requests_per_second = 2
        raw_documents = sitemap_loader.load()
        file = open(cache_file, "wb")
        pickle.dump(raw_documents, file)

    print(f"loaded {len(raw_documents)} documents")
    for doc in raw_documents:
        doc.page_content = re.sub(r"\s+", ' ', doc.page_content)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=100
    )

    documents = text_splitter.split_documents(raw_documents)
    pdb.set_trace()

    # embeddings = OllamaEmbeddings(model='wizard-vicuna-uncensored')
    embeddings = OpenAIEmbeddings(allowed_special='all', disallowed_special=())

    print(f"Going to add {len(documents)} to Weaviate")
    # Weaviate.from_documents(documents, embeddings, weaviate_url="http://127.0.0.1:8081")
    print("****Loading to vectorestore done ***")



if __name__ == "__main__":
    fetch_data()
