from langchain_community.retrievers import PubMedRetriever

if __name__=="__main__":
    retriever = PubMedRetriever()
    doc = retriever.get_relevant_documents("how about the AIDS in Asia")
    print(doc)