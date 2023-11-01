#import libraries
import os
import pickle
import time
import streamlit as st
from langchain.llms import OpenAI
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
col1, col2= st.columns([1, 3])
col1.title("Articles Research Tool")
col2.image("serach_img.jpeg",width=200)
st.write("**Welcome to your News Article Assistant**")

st.markdown("_Just drop the article URLs, and I'm here to assist you with summaries, insights, and answers to your questions. Share the URL, and let's dive into the world of news together_")
st.sidebar.title("News Articles URLS")
st.sidebar.markdown("**_Note: You can only process up to three urls at once._**")


urls = []
for i in range(3):
    url = st.sidebar.text_input(f"URL {i + 1}")
    urls.append(url)

processed_url_clicked = st.sidebar.button("Process URLS")

main_placeholder = st.empty()

#creat llm object
llm = OpenAI(
    temperature=0.9,
    max_tokens=500
)
def generate_text_data_urls(urls):
    urls_loaders = []
    combined_text = ""
    bool = []
    for url in urls:
        text_data = get_text_data(url=url, root=root, data=data)

        if text_data == False:
            pass
        else:
            combined_text += text_data[0].page_content + "\n"
            urls_loaders.append(text_data[0])

        print(f"The url - {url} done .....")

    # merged_docs = MergedDataLoader(loaders=urls_loaders)
    # all_docs = merged_docs.load()
    return urls_loaders, combined_text
urls_positions = {
    v:k + 1 for k,v in enumerate(urls)
}



if processed_url_clicked:
    #chcek if url is valid
    main_placeholder.write("**VALIDATING PROVIDED URLS**")
    valid,invalid = categorize_urls_with_statement(urls)
    if len(valid) == 0:
        st.error("Unfortunately, the provided URLs are not valid. Please provide valid URLs to continue.")
    if len(invalid) != 0 or len(valid) == 3:
        if len(valid) > 0:
            for i in invalid:
               st.error(f"URL : {i} is not valid")
            #selected_option = st.selectbox("Choose an option", ("Option 1", "Option 2"))
            cont = st.radio(
                "**Continuing with the valid ones...click No if you would'nt**",
                ["Yes", "No"])

            if cont == "Yes":
                #load data generate text
                main_placeholder = st.empty()
                main_placeholder.write("**LOADING DATA ......**")

                url_docs, combined_text = generate_text_data_urls(valid)
                # split data

                if combined_text:
                    main_placeholder.write("**DATA SPLITTING STARTED.....**")
                    text_splitter = RecursiveCharacterTextSplitter(
                        chunk_size=1000,
                        chunk_overlap=200
                    )
                    text_split = text_splitter.split_text(combined_text)

                    # embedding text
                    main_placeholder.write("**EMBEDDINGS AND VECTOR STORES GENERATED**")
                    embeddings = OpenAIEmbeddings()
                    vectors_openai = FAISS.from_texts(text_split, embeddings)
                    file_path = "vector_index.pkl"
                    with open(file_path, "wb") as f:
                        pickle.dump(vectors_openai,f)

                    #query = main_placeholder.text_input("Ask me your question",key="question")



                else:
                    st.write("**There seems to be an issue with text processing. Please check the URL and provide a valid one, or try again later.**")

            else:
                 pass








query = main_placeholder.text_input("Ask me your question",key="question")
file_path = "vector_index.pkl"

if query:
    if os.path.exists(file_path):
        with open(file_path,"rb") as f:
            vector_stores = pickle.load(f)
            chain = RetrievalQA.from_llm(llm=llm,
                                         retriever=vector_stores
                                         .as_retriever())
            result = chain({"query":query},return_only_outputs=True)

            st.header("Answer")
            st.subheader(result["result"])










