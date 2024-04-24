from typing import List

from langchain.docstore.document import Document
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores.pgvector import PGVector, DistanceStrategy
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

import psycopg2
from psycopg2 import sql
import json
from urllib.parse import urlparse, parse_qs

def delete_records_by_source(connection, source_value):
    # Create a cursor
    cursor = connection.cursor()

    try:
        # Construct and execute the delete query
        delete_query = sql.SQL("""
            DELETE FROM langchain_pg_embedding
            WHERE (cmetadata->>'source')::text = %s
        """)
        cursor.execute(delete_query, (source_value,))

        # Commit the transaction
        connection.commit()

        # Print number of rows affected
        print(f"{cursor.rowcount} row(s) deleted for source: {source_value}")
    except Exception as e:
        # Rollback the transaction if an error occurs
        connection.rollback()
        print("Error deleting records:", e)
    finally:
        # Close cursor
        cursor.close()


def extract_connection_info(conn_string):
    # Parse the connection string
    parsed_url = urlparse(conn_string)

    # Extract components
    dbname = parsed_url.path.lstrip('/')
    user = parsed_url.username
    password = parsed_url.password
    host = parsed_url.hostname
    port = parsed_url.port

    # Construct the connection string
    conn_info = f"dbname='{dbname}' user='{user}' password='{password}' host='{host}' port='{port}'"

    return conn_info


if __name__=="__main__":
    loader = TextLoader("/Users/kunhe/myproj/KnLangChain/training.txt")
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()

    CONNECTION_STRING = "postgresql+psycopg2://postgres:111111@localhost:5466/vector"

    COLLECTION_NAME = "kunlangchain_test"

    source_name = docs[0].metadata.get("source")
    print(source_name)
    # Connect to your PostgreSQL database
    try:
        connection_info = extract_connection_info(CONNECTION_STRING)
        connection = psycopg2.connect(connection_info)
        # Call the delete function with the source value you want to delete
        delete_records_by_source(connection, source_name)

    except psycopg2.Error as e:
        print("Error connecting to PostgreSQL:", e)
    finally:
        # Close the connection
        if connection:
            connection.close()


    db = PGVector.from_documents(
        embedding=embeddings,
        documents=docs,
        collection_name=COLLECTION_NAME,
        connection_string=CONNECTION_STRING,
        pre_delete_collection=False,
        distance_strategy=DistanceStrategy.COSINE,
    )
    query = "关于训练集有什么描述"
    docs_with_score = db.similarity_search_with_score(query)

    for doc, score in docs_with_score:
        print("-" * 80)
    print("Score: ", score)
    print(doc.page_content)
    print("-" * 80)

