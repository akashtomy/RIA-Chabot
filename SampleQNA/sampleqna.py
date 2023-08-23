import os
import tempfile

import streamlit as st
from langchain.agents import create_csv_agent
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from PyPDF2 import PdfReader

from secret_key import openapi_key

os.environ["OPENAI_API_KEY"] = openapi_key

def main():
    st.set_page_config(page_title="Q&A")
    st.header("Q&A")

    file_type = st.radio("What type of file would you like to upload?", ('CSV','PDF'))

    if file_type == "CSV":
        csv = st.file_uploader("Upload your CSV", type="csv")
        if csv is not None:
            question = st.text_input("Write your question:")
            llm = OpenAI(temperature=0)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temporary_file:
                temporary_file.write(csv.getvalue())

            agent = create_csv_agent(llm, temporary_file.name, verbose=False)

            os.unlink(temporary_file.name)

            if question is not None and question != "":
                answer = agent.run(question)
                st.write(answer)
    elif file_type =="PDF":
        pdf = st.file_uploader("Upload your PDF", type="pdf")
        
        if pdf is not None:
            question = st.text_input("Write your question:")
            llm = OpenAI(temperature=0)

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temporary_file:
                temporary_file.write(pdf.getvalue())
            
            pdfreader = PdfReader(temporary_file.name)

            raw_text = ''

            for i, page in enumerate(pdfreader.pages):
                content = page.extract_text()
                if content:
                    raw_text += content

            text_splitter = CharacterTextSplitter(
                separator = "\n",
                chunk_size = 800,
                chunk_overlap  = 200,
                length_function = len,
            )
            texts = text_splitter.split_text(raw_text)
            os.unlink(temporary_file.name)

            if question is not None and question != "":
                embeddings = OpenAIEmbeddings()
                document_search = FAISS.from_texts(texts, embeddings)
                chain = load_qa_chain(OpenAI(), chain_type='stuff')

                docs = document_search.similarity_search(question)
                response = chain.run(input_documents=docs, question=question)
                st.write(response)

if __name__ == "__main__":
    main()