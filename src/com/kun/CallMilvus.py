from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Milvus
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

if __name__ =="__main__":

    loader = TextLoader("/Users/kunhe/myproj/KnLangChain/training.txt")
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()
    vector_db = Milvus.from_documents(
        docs,
        embeddings,
        collection_name="collection_kun",
        connection_args={"host": "127.0.0.1", "port": "19530"},
    )
    query = "关于训练集有什么描述"
    docs = vector_db.similarity_search(query)
    print(docs[0].page_content)