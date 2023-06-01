import os
import platform

import openai
import chromadb
import langchain

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.document_loaders import PyPDFLoader


openai.api_key = os.getenv("OPENAI_API_KEY")

class NewSession:
    def __init__(self, pdf_url):
        self.chat_history = []

        # LLMのセットアップ
        llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
    
        # PDFをページごとに分割してベクターストアに格納する
        loader = PyPDFLoader(pdf_url)
        pages = loader.load_and_split()
        embeddings = OpenAIEmbeddings()
        vectorstore = Chroma.from_documents(pages, embedding=embeddings, persist_directory=".")
        vectorstore.persist()

        # LLMに自然言語で質問するためのオブジェクトを作成
        self.pdf_qa = ConversationalRetrievalChain.from_llm(
            llm, 
            vectorstore.as_retriever(search_kwargs={"k": 1}), 
            return_source_documents=True
            ) 


    def add_chat_history(self, query, result):
        old_query = (query, result)
        self.chat_history.append(old_query)


    def question_to_llm(self, query):
        result = self.pdf_qa({"question": query, "chat_history": self.chat_history})
        result_content = result["answer"]
        source_contents = [doc.page_content for doc in result['source_documents']]

        self.add_chat_history(query, result_content)

        return {
            "result_content": result["answer"],
            "source": source_contents
            }


    def show_chat_history(self):
        print("----- debug -----")
        print(self.chat_history)


if __name__ == '__main__':

    session = NewSession("miyagi_test.pdf")

    input_query = ""
    while(input_query != "exit"):
        input_query = input("You: ")
        if input_query != "exit":
            response = session.question_to_llm(input_query)
            print(f"ChatBot: {response['result_content']}")
            #print(f"### source: {response['source']} ###")
        else:
            session.show_chat_history()