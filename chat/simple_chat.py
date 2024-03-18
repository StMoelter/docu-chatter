import os

# from langchain.chat_models import AzureChatOpenAI
from langchain.chat_models import ChatOpenAI
# from langchain_community.chat_models import OpenAIChat
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationSummaryBufferMemory



from dotenv import load_dotenv
load_dotenv(f"{os.path.dirname(__file__)}/../.env")



def run_llm(question, history):
    history = history or []
    llm = ChatOpenAI(
        verbose=True,
        temperature=0,
        model_name='gpt-3.5-turbo-0125'
    )
    memory=ConversationSummaryBufferMemory(
        llm=llm,
        max_token_limit=50,
        )
    conversation = ConversationChain(
        llm=llm,
        memory=memory
    )

    answer = conversation.predict(input=question)
    import pdb; pdb.set_trace()

    history.append(question) 
    return answer, history
  