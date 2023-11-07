from langchain.embeddings.base import Embeddings
from langchain.vectorstores import Chroma
from langchain.schema import BaseRetriever

# override the RedundantFilterRetreiver
# this class extend BaseRetreiver myclass(BaseRetriever) is the way to extend... 
class RedundantFilterRetriever(BaseRetriever):
    # as we do not want to "HAVE TO" use OpenAIEmbeddings
    embeddings: Embeddings  # this is a property that must be of type Embeddings
    chroma: Chroma   # same for chroma
    

    def get_relevant_documents(self, query): # receive a string that we call query
        # calculate embeddings for the query string
        # we could do:
        # embeddings = OpenAIEmbeddings()
        # emb = embeddings.embed_query() # but we do not want to "HAVE TO" use OpenAIEmbeddings
        emb = self.embeddings.embed_query(query)

        # take embeddings and feed them into that 'max_marginal_relevance_by_vector'
        return self.chroma.max_marginal_relevance_search_by_vector(
                embeddings=emb, # kind of baseLine embeddings, that the thing we want to find relevant documents for
                lambda_mult=0.8 #  more it's close to 1 more the retreived documents have to match the emb score
                )

    # we do not override/use this func
    async def aget_relevant_documents(self):
        return []
