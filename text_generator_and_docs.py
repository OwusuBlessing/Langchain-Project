
from url_data_loader_utils import is_valid_url,get_text_loader,get_html_content,save_json

root = r"C:\Users\User\Desktop\Main-NLP-PROJECTS\Langchain-Project\HTML_FILE_PATHS"
def get_text_data(url, root, data):
    valid = is_valid_url(url)
    if valid:
        print("URL is valid......")
        if url in data.keys():
            print("URL exists in our database....retrieving html content")
            if data[url]:
                html_content_path = data[url]
                print("html content retrieved.....")
                text_data = get_text_loader(html_content_path
                                            )

                save_json(json_data=data)

                return text_data
                # return retrieved_text
            # use html loader here to generate text
            else:
                path_html = get_html_content(root=root, data=data, url=url)  # get html content and save
                save_json(json_data=data)  # save new data as json

                # load the html content here
                retrieved_html_path = get_html_content(root=root, url=url, data=data)
                # return retrieved_text

                text_data = get_text_loader(retrieved_html_path

                                            )
                return text_data
        else:
            path_html = get_html_content(root=root, data=data, url=url)
            # save data to url data
            save_json(json_data=data)

            # use html text loader now
            retrieved_html_path = get_html_content(root=root, data=data, url=url)

            text_data = get_text_loader(retrieved_html_path

                                        )
            return text_data
    else:
        return False


def generate_text_data_urls(urls):
    urls_loaders = []
    combined_text = ""
    for url in urls:
        text_data = get_text_data(url=url, root=root, data=data)
        combined_text += text_data[0].page_content + "\n"
        urls_loaders.append(text_data[0])

        print(f"The url - {url} done .....")

    # merged_docs = MergedDataLoader(loaders=urls_loaders)
    # all_docs = merged_docs.load()
    return urls_loaders, combined_text
