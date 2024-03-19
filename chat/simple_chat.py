import os
import yaml

# from langchain.chat_models import AzureChatOpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationSummaryBufferMemory
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory



from dotenv import load_dotenv
load_dotenv(f"{os.path.dirname(__file__)}/../.env")

def load_status(status):
    pass
def save_status(memory):
    pass

def run_llm(question, status=None):
    # status = yaml.safe_load(status) or {'chat_memory': ChatMessageHistory(), 'moving_summary_buffer': ""}
    llm = ChatOpenAI(
        verbose=True,
        temperature=0,
        model_name='gpt-3.5-turbo-0125'
    )
    memory=ConversationSummaryBufferMemory(
        llm=llm,
        max_token_limit=4000,
        # chat_memory=status['chat_memory'],
        # moving_summary_buffer=status['moving_summary_buffer'],
    )
    conversation = ConversationChain(
        llm=llm,
        memory=memory
    )

    answer = conversation.predict(input=question)
    import pdb; pdb.set_trace()
    status = save_status(memory)
       # 'chat_memory': memory.chat_memory, 
        # 'moving_summary_buffer': memory.moving_summary_buffer
    # })
    return answer, status
  