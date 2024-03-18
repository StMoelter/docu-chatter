import os
import weaviate
from typing import Any, Dict, List

from langchain.embeddings import AzureOpenAIEmbeddings
from langchain.chat_models import AzureChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import Weaviate
from langchain.callbacks.stdout import StdOutCallbackHandler

from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
load_dotenv(f"{os.path.dirname(__file__)}/../.env")

def get_chat_history(chat_history):
    buffer = ""
    for dialogue_turn in chat_history:
      human = "Human: " + dialogue_turn[0]
      ai = "Assistant: " + dialogue_turn[1]
      buffer += "\n" + "\n".join([human, ai])
    return buffer


def run_llm_azure(query: str, chat_history: List[Dict[str, Any]] = []):
    embeddings = OpenAIEmbeddings()
    client = weaviate.Client(url="http://127.0.0.1:8081")
    vectorstore = Weaviate(
        client=client, 
        index_name=os.environ["WEAVIATE_INDEX"], 
        text_key='text', 
        embedding=embeddings,
        by_text=False
        )
   
    chat = AzureChatOpenAI(
        azure_endpoint=os.environ["AZURE_ENDPOINT"],
        openai_api_key=os.environ["AZURE_KEY"],
        azure_deployment=os.environ["AZURE_LLM_DEPLOYMENT"],
        openai_api_version=os.environ["AZURE_VERSION"],
    )

    qa = ConversationalRetrievalChain.from_llm(
        llm=chat, retriever=vectorstore.as_retriever(),
        return_source_documents=True,
        callbacks=[StdOutCallbackHandler()],
        get_chat_history=get_chat_history
    )
    # import pdb; pdb.set_trace()
    return qa({"question": query, "chat_history": chat_history})

def run_llm(query: str, chat_history: List[Dict[str, Any]] = []):
    embeddings = OpenAIEmbeddings()

    client = weaviate.Client(url="http://127.0.0.1:8081")
    vectorstore = Weaviate(
        client=client, 
        index_name=os.environ["WEAVIATE_INDEX"], 
        text_key='text', 
        embedding=embeddings,
        by_text=False,
        attributes=['source', 'loc']
        )
   
    chat = ChatOpenAI(
        verbose=True,
        temperature=0,
    )

    qa = ConversationalRetrievalChain.from_llm(
        llm=chat, retriever=vectorstore.as_retriever(
            search_kwargs={'k': 5, 'fetch_k': 50, 'properties': ['source', 'text']}
            ),
        return_source_documents=True,
        callbacks=[StdOutCallbackHandler()],
        get_chat_history=get_chat_history,
        return_generated_question=True,
        response_if_no_docs_found="Sorry, da habe ich keine Informationen zu gefunden."
    )
    # import pdb; pdb.set_trace()
    return qa({"question": query, "chat_history": chat_history})
