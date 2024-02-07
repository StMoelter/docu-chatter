import os
import weaviate
from typing import Any, Dict, List

from langchain.embeddings import AzureOpenAIEmbeddings
from langchain.chat_models import AzureChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import Weaviate
from langchain.callbacks.stdout import StdOutCallbackHandler

def get_chat_history(chat_history):
    buffer = ""
    for dialogue_turn in chat_history:
      human = "Human: " + dialogue_turn[0]
      ai = "Assistant: " + dialogue_turn[1]
      buffer += "\n" + "\n".join([human, ai])
    return buffer


def run_llm(query: str, chat_history: List[Dict[str, Any]] = []):
    embeddings = AzureOpenAIEmbeddings(
        azure_endpoint=os.environ["AZURE_ENDPOINT"],
        openai_api_key=os.environ["AZURE_KEY"],
        azure_deployment=os.environ["AZURE_EMBEDDING_DEPLOYMENT"],
        openai_api_version=os.environ["AZURE_VERSION"],
    )
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
