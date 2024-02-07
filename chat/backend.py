import os
import weaviate
from typing import Any, Dict, List

from langchain.embeddings import OllamaEmbeddings
from langchain.chat_models import ChatOllama
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import Weaviate
from langchain.callbacks.stdout import StdOutCallbackHandler


INDEX_NAME = "stable-diffusion-index"


def run_llm(query: str, chat_history: List[Dict[str, Any]] = []):
    embeddings = OllamaEmbeddings()
    client = weaviate.Client(url="http://127.0.0.1:8080")
    vectorstore = Weaviate(
        client=client, 
        index_name='LangChain_74e822ae0ec24fdc998972af272bdbdd', 
        text_key='text', 
        embedding=embeddings,
        by_text=False
        )
   
    chat = ChatOllama(
        model="wizard-vicuna-uncensored",
        verbose=True,
        temperature=0,
        language="en",
    )

    qa = ConversationalRetrievalChain.from_llm(
        llm=chat, retriever=vectorstore.as_retriever(),
        return_source_documents=True,
        callbacks=[StdOutCallbackHandler()]
    )
    return qa({"question": query, "chat_history": chat_history})
