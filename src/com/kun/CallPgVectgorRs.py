from typing import List

from langchain.docstore.document import Document
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings.fake import FakeEmbeddings
from langchain_community.vectorstores.pgvecto_rs import PGVecto_rs
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

if __name__=="__main__":
    loader = TextLoader("/Users/kunhe/myproj/KnLangChain/training.txt")
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()

    ## PGVecto.rs needs the connection string to the database.
    ## We will load it from the environment variables.
    import os

    PORT = os.getenv("DB_PORT", 5466)
    HOST = os.getenv("DB_HOST", "localhost")
    USER = os.getenv("DB_USER", "postgres")
    PASS = os.getenv("DB_PASS", "111111")
    DB_NAME = os.getenv("DB_NAME", "vector")

    # Run tests with shell:
    URL = "postgresql+psycopg://{username}:{password}@{host}:{port}/{db_name}".format(
        port=PORT,
        host=HOST,
        username=USER,
        password=PASS,
        db_name=DB_NAME,
    )

    db1 = PGVecto_rs.from_documents(
        documents=docs,
        embedding=embeddings,
        db_url=URL,
        # The table name is f"collection_{collection_name}", so that it should be unique.
        collection_name="kun_pg",
    )

    query = "关于训练集有什么描"
    docs: List[Document] = db1.similarity_search(
        query, k=4
    )

    for doc in docs:
        print(doc.page_content)
        print("======================")

