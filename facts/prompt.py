from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA # allow us to to the full chain in one stop
from langchain.chat_models import ChatOpenAI 
from dotenv import load_dotenv

# to bebug, it will print all intermediate stages
# import langchain
# langchain.debug = True

load_dotenv()

chat = ChatOpenAI()
embeddings = OpenAIEmbeddings()

db = Chroma(
        persist_directory="emb",
        embedding_function=embeddings # not the same arg compare to the main, bc we use Chroma()
        )

# as the db. is the one we have saved embedded of chunks of datas, the retriever look there.
# a Retriever is an object which have a method get_relevant_documents() 
# that take a string and return a lidt of documents
# this get_relevant_documents() is reach through .as_retriever()
retriever = db.as_retriever()

chain = RetrievalQA.from_chain_type(
        llm=chat,
        retriever=retriever,
        chain_type="stuff" # "stuff" means it stuff the retrieved doc(from Chroma) into the prompt
        # chain_type="map_reduce" # send 5 req, then select the most relevant
        # chain_type="map_rerank" # send 5 req, same map_reduce but return the score as well
        # chain_type="refine" # send 5 req, same map_reduce but take the resp from previous a see if next proposale is better, in which case chatGPT can refine/update the result
        )
# NOTE what ever, the best is chain_type="stuff", bc other methods call many time the API so cost money and are slower.....

result = chain.run("What is an interresting fact about the english language?")

print(result)









