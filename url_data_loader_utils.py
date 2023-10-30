import json
import requests
import os
import re
from langchain.document_loaders import BSHTMLLoader
from pathlib import Path
from langchain.document_loaders import UnstructuredHTMLLoader

#check if url is valid or not
def is_valid_url(url):
    try:
        response = requests.get(url)
        if response.status_code >= 200 and response.status_code < 300:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False

def remove_special_characters(input_text):
    # Use a regular expression to match and remove all non-alphabet characters
    cleaned_text = re.sub(r'[^a-zA-Z]', '', input_text)
    return cleaned_text
#get html text content
def get_html_content(url,root,data):
        response = requests.get(url)
        root = Path(root)
        if response.status_code == 200:
            print("Status code 200 ......fine")
            html_content = response.text
            # Specify the file path where you want to save the HTML content

            suffix = remove_special_characters(url)

            #file_path = root / f"{suffix}.html"
            # Save the HTML content to a file
            print("Ready to save html content")
            path_to_save = root / f"{suffix}.html"
            with open(path_to_save, "w", encoding="utf-8") as file:
                print("Saving path html content for url.....")
                file.write(html_content)


            #update dictionary
            data[url] = str(path_to_save)
            print("url data updated")

            return path_to_save
        else:
            print("Bad status code")


def save_json(json_data):
    with open("urls.json","w") as file:
        print("Saving updated url json")
        json.dump(json_data,file)

def get_text_loader(html_path):
    loader = UnstructuredHTMLLoader(rf"{html_path}")
    data = loader.load()
    return data


def categorize_urls_with_statement(url_list):
    valid_urls = []
    invalid_urls = []

    for url in url_list:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                valid_urls.append(url)
            else:
                invalid_urls.append(url)
        except requests.exceptions.RequestException:
            invalid_urls.append(url)

    return valid_urls, invalid_urls









