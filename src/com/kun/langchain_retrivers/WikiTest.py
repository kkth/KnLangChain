from langchain_community.retrievers import WikipediaRetriever
from langchain.chains import ConversationalRetrievalChain
from langchain_openai import ChatOpenAI

if __name__=="__main__":
    retriever = WikipediaRetriever()
    docs = retriever.get_relevant_documents(query="HUNTER X HUNTER")
    print(docs)

    model = ChatOpenAI(model_name="gpt-3.5-turbo")  # switch to 'gpt-4'
    qa = ConversationalRetrievalChain.from_llm(model, retriever=retriever)

    questions = [
        "What is Apify?",
        "When the Monument to the Martyrs of the 1830 Revolution was created?",
        "What is the Abhayagiri Vihāra?",
        # "How big is Wikipédia en français?",
    ]
    chat_history = []

    for question in questions:
        result = qa({"question": question, "chat_history": chat_history})
        chat_history.append((question, result["answer"]))
        print(f"-> **Question**: {question} \n")
        print(f"**Answer**: {result['answer']} \n")