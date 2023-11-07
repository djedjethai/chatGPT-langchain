from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
# from langchain.prompts import MessagesPlaceholder, HumanMessagePromptTemplate, ChatPromptTemplate
# from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
# from langchain.memory import ConversationBufferMemory, FileChatMessageHistory, ConversationSummaryMemory

# pip install langchain openai python-dotenv
# pip install tiktoken
# pip install chromadb


from dotenv import load_dotenv

load_dotenv()

# NOTE that cost money as openAI is doing the job
embeddings = OpenAIEmbeddings()
# emb = embeddings.embed_query("Hi there")

text_splitter = CharacterTextSplitter(
        separator="\n", # split on new line character
        chunk_size=200, # chunk size
        chunk_overlap=0 # copy some  text over each chunk(means some text gonna be repeated)
        )

# load a text file using langChain(note that we can load any kind of file or even from buckets)
loader = TextLoader("facts.txt")
# docs = loader.load() # load the full text
# docs = loader.load_and_split() # load the text and split it automatically 
docs = loader.load_and_split(
        text_splitter=text_splitter
        )

# use Chroma which is a specific version done to work with langchain
# this func will automatically reachout to openAI and calculate the embeddings,
# which are automatically store into the sqlite db(linked to chroma)
# so it cost money.. a little but still
# NOTE each time we run the program it recalculate the embeddings and re-store them
# so it duplicate datas......
db = Chroma.from_documents(
        docs, 
        embedding=embeddings,
        persist_directory="emb"
        )

# search in the db the match embeddings
# results = db.similarity_search() if does not casr the score(result[1])
results = db.similarity_search_with_score(
        "what is an interresting fact with the english language ?",
        k=2 # return only the most match element, if 3 it will return the 3 one
        )

for result in results:
    print("\n")
    print(result[1])
    print(result[0].page_content)




# chat = ChatOpenAI()
# chat = ChatOpenAI(verbose=True) # for debug






