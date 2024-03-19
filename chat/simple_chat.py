import os
import yaml

from langchain.chat_models import AzureChatOpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationSummaryBufferMemory
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
from langchain.schema.messages import AIMessage, HumanMessage


from dotenv import load_dotenv

load_dotenv(f"{os.path.dirname(__file__)}/../.env")


def hash_to_msg(hash):
    klass = list(hash.keys())[0]
    if klass == "HumanMessage":
        return HumanMessage(hash[klass])
    elif klass == "AIMessage":
        return AIMessage(hash[klass])
    else:
        raise Exception(f"Unknown class {klass}")


def load_status(status, memory):
    status = status or {}
    chat_memory = list(map(hash_to_msg, status["chat_memory"])) if "chat_memory" in status else []
    memory.moving_summary_buffer = status["moving_summary_buffer"] if "moving_summary_buffer" in status else ''
    memory.chat_memory = ChatMessageHistory(messages=chat_memory)
    return memory


def save_status(memory):
    messages = list(map(
        lambda m: {m.__class__.__name__: m.content},
        memory.chat_memory.messages,
    ))
    return {
        "chat_memory": list(messages),
        "moving_summary_buffer": memory.moving_summary_buffer,
    }


def get_llm_open_ai():
    return ChatOpenAI(verbose=True, temperature=0, model_name="gpt-3.5-turbo-0125")


def get_llm_azure():
    return AzureChatOpenAI(
        azure_endpoint=os.environ["AZURE_ENDPOINT"],
        openai_api_key=os.environ["AZURE_KEY"],
        azure_deployment=os.environ["AZURE_LLM_DEPLOYMENT"],
        openai_api_version=os.environ["AZURE_VERSION"],
    )


def run_llm(question, status):
    # status = yaml.safe_load(status) or {'chat_memory': ChatMessageHistory(), 'moving_summary_buffer': ""}
    llm = get_llm_azure()
    memory = ConversationSummaryBufferMemory(
        llm=llm,
        max_token_limit=4000,
    )
    load_status(status, memory)
    conversation = ConversationChain(llm=llm, memory=memory)

    answer = conversation.predict(input=question)
    # import pdb;pdb.set_trace()
    status = save_status(memory)
   
    return answer, status
