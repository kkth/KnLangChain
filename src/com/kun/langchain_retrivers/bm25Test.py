from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document


if __name__=="__main__":
    retriever = BM25Retriever.from_texts(["foo", "bar", "world", "hello", "foo bar"])
    result = retriever.get_relevant_documents("foo")
    print(result)
