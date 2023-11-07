from langchain.prompts import MessagesPlaceholder, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory, FileChatMessageHistory, ConversationSummaryMemory

from dotenv import load_dotenv

# pip install langchain openai python-dotenv

load_dotenv()

# chat = ChatOpenAI()
chat = ChatOpenAI(verbose=True) # for debug

# # setup the memory for the chat history to be store
# # NOTE pb here is that the chat history is saved and the request to chatGPT become longer so more expensive....
# # the solution is 
# memory = ConversationBufferMemory(
#         chat_memory=FileChatMessageHistory("messages.json"), # save history into a file in case of restart, there is other classes allow database storing :)(look at it)
#         memory_key="messages", 
#         return_messages=True
#         )

# note that ConversationSummaryMemory do not work well with chat_memory=FileChatMessageHistory() 
# and it's slower than ConversationBufferMemory as it have to run an addition call to llm
# NOTE good to save money as in case of long conversation only 1 sum is sent instead of all msg
# TODO see how to save previous conversation to a db ?? (in case of restart...)
memory = ConversationSummaryMemory(
        memory_key="messages", 
        return_messages=True,
        llm=chat # that the language model we like the ConversationSummaryMemory use
        )



prompt = ChatPromptTemplate(
        input_variables=["content", "messages"],
        messages=[
            MessagesPlaceholder(variable_name="messages"), # tells chatGPT to look at msg memory 
            HumanMessagePromptTemplate.from_template("{content}")
            ]
        )

chain = LLMChain(
        llm=chat,
        prompt=prompt,
        memory=memory, # inject the memory into the chain
        verbose=True # for debug, see the what is sent off to the model language 
        )



while True:
    content = input(">> ")

    result = chain({"content": content})

    print(result["text"])
