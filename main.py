#import libraries
import os
import pickle
import time
import streamlit as st
from langchain import OpenAI
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredHTMLLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import json
from text_generator_and_docs import get_text_data, generate_text_data_urls
from url_data_loader_utils import get_text_loader,get_html_content,save_json, is_valid_url,remove_special_characters,categorize_urls_with_statement
from dotenv import load_dotenv,find_dotenv
#set up openai api key
load_dotenv() #take environemtn variable from .env

#root to html contents
root = r"C:\Users\User\Desktop\Main-NLP-PROJECTS\Langchain-Project\HTML_FILE_PATHS"
url_json_paths = r"C:\Users\User\Desktop\Main-NLP-PROJECTS\Langchain-Project\urls_database\urls.json"
with open(url_json_paths, 'r') as json_file:
    data = json.load(json_file)

#ui
col1, col2 = st.columns([1, 3])
col1.title("News Research Tool")
col2.image("serach_img.jpeg",width=200)

st.sidebar.title("News Artcile URLS")
st.sidebar.markdown("**_Note: You can only process up to three urls at once._**")

urls = []
for i in range(3):
    url = st.sidebar.text_input(f"URL {i + 1}")
    urls.append(url)

processed_url_clicked = st.sidebar.button("Process URLS")

main_placeholder = st.empty()

if processed_url_clicked:
    #chcek if url is valid
    main_placeholder.write("**VALIDATING PROVIDED URLS**")
    valid,invalid = categorize_urls_with_statement(urls)
    if len(valid) == 0:
        st.error("All the provided urls are not vvalid,please valid urls")
    if len(invalid) != 0:
        if len(valid) > 0:
            for i in invalid:
               st.error(f"URL: {i} is not valid")
            st.write("Would you like to continue with the valid ones?")


            #selected_option = st.selectbox("Choose an option", ("Option 1", "Option 2"))

            yes = st.button("Yes")
            no = st.button("No")

            if yes:
                st.write("Text generated after clicking the button.")
                # load data generate text
                main_placeholder = st.empty()
                main_placeholder.write("**LOADING DATA ......**")
                url_docs, combined_text = generate_text_data_urls(valid)
                # split data
                main_placeholder.write("**DATA SPLITTING STARTED.....**")
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200
                )
                text_split = text_splitter.split_text(combined_text)
                # embedding text
                main_placeholder.write("**GENERATING EMBEDDINGS...INSTANTIATING VECTOR-STORES**")
                embeddings = OpenAIEmbeddings()
                vectors_openai = FAISS.from_texts(text_split, embeddings)
                file_path = "vector_index.pkl"
                with open(file_path, "wb") as f:
                    pickle.dump(vectors_openai,f)

                query = st.text_input("Questions")






    if len(valid) == 3:
           #split data
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            text_split = text_splitter.split_text(combined_text)

            #embedding text
            embeddings = OpenAIEmbeddings()
            vectors_openai = FAISS.from_texts(text_split, embeddings)
            file_path = "vector_index.pkl"
            with open(file_path, "wb") as f:
                pickle.dump(vectors_openai, f)









    #process url to get data






