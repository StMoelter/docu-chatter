from langchain.document_loaders.sitemap import SitemapLoader
import nest_asyncio
import pdb
import re

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

sitemap_uri = "https://stability.ai/sitemap.xml"
cache_file = "~/workspace/vendor/docu-chatter/tmp/stability.ai"


def fetch_data():
    if os.path.isfile(cache_file):
        filehandler = open(cache_file, "rb")
        raw_documents = pickle.load(filehandler)
    else:
        sitemap_loader = SitemapLoader(
            web_path=sitemap_uri, header_template=header_template
        )
        sitemap_loader.requests_per_second = 4
        raw_documents = sitemap_loader.load()
        file = open(pickle_file, "wb")
        pickle.dump(raw_documents, file)
        sitemap_loader = SitemapLoader(
            web_path=sitemap_uri, header_template=header_template
        )

    print(f"loaded {len(raw_documents)} documents")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=50, separators=["\n\n", "\n", " ", ""]
    )
    pdb.set_trace()


if __name__ == "__main__":
    fetch_data()
