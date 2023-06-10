import streamlit as st
import requests
import json
import openai

auto_suggest_url = "https://search-books-main-5xruavjoyo7mq2fem4jwni4ace.ap-south-1.es.amazonaws.com/books_main/_search"
add_data_url = "https://search-books-main-5xruavjoyo7mq2fem4jwni4ace.ap-south-1.es.amazonaws.com/books_main/_doc"
headers = {
        'Authorization': 'Basic b3BlbnNlYXJjaC1ib29rczpCb29rc0AyMDIz',
        'Content-Type': 'application/json'
    }
def submit_book_details(title,author,book_link,price,book_type,genre):

    payload = json.dumps({
        "book_title_wrapper": title,
        "book_link": book_link,
        "book_author": author,
        "strikethrough": price,
        "book_type": book_type,
        "Book_by_Genre": genre
    })

    response = requests.request("POST", add_data_url, headers=headers, data=payload)
    if(response.status_code.__eq__(201)):
        return "SUCCESS"
    else:
        return "FAILED"

def generate_story(input_string):

    # Set up your OpenAI API key
    openai.api_key = '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'

    prompt = f"Once upon a time, there was {input_string}. The story unfolds as follows:"
    response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=prompt,
            max_tokens=200,
            n=1,
            stop=None,
            temperature=0.7
        )

    generated_text = response.choices[0].text.strip()

    return generated_text


def get_metadata_for_rating(imageUrl):
    payload = json.dumps({
    "query": {
    "match": {
      "book_link": imageUrl
    }
    }
    })
    response = requests.request("POST", auto_suggest_url, headers=headers, data=payload).json()['hits']['hits'][0]['_source']
    print(response)
    try:
        author=str(response['book_author']).replace("by","")
    except (Exception):
        author = ""
    try:
        title=response['book_title_wrapper']
    except (Exception):
        title = ""
    try:
        type=response['book_type']
    except (Exception):
        type = ""
    try:
        genre=response['Book_by_Genre']
    except (Exception):
        genre = ""
    try:
        price=response['strikethrough']
    except (Exception):
        price = ""

    return author,title,type,genre,price
def fetch_response(query,auth_filter,genre_filter,type_filter):
    if (str(auth_filter).__contains__("-")):

        payload = json.dumps({
            "query": {
                "bool": {
                    "must": [{

                        "match": {
                            str(auth_filter.split("-")[0]): str(auth_filter.split("-")[1]).replace("by","")

                        }},
                        {

                            "match": {
                                str(genre_filter.split("-")[0]): str(genre_filter.split("-")[1])

                        }},
                        {

                            "match": {
                                str(type_filter.split("-")[0]): str(type_filter.split("-")[1])

                        }},
                        {
                            "match": {
                                "book_title_wrapper": query
                            }
                        }
                    ]

                }
            }
        })
    else:
        payload = json.dumps({
            "_source": ["book_title_wrapper", "book_image_src", "Book_by_Genre", "book_type", "book_author"],
            "query": {
                "multi_match": {
                    "query": query,
                    "type": "bool_prefix",
                    "fields": [
                        "book_title_wrapper",
                        "book_title_wrapper._2gram",
                        "book_title_wrapper._3gram"
                    ]
                }
            }
        })

    response = requests.request("POST", auto_suggest_url, headers=headers, data=payload).json()['hits']['hits']
    return response
def get_results(field,response):
    titles=[]
    links=[]
    genres=[]
    book_types=[]
    authors=[]
    for resp in response:
        title=resp['_source']['book_title_wrapper']
        link = resp['_source']['book_image_src']
        genre = resp['_source']["Book_by_Genre"]
        book_type= resp['_source']['book_type']
        author=resp['_source']['book_author']
        if title not in titles:
            titles.append(title)
        if link not in links:
            links.append(link)
        if genre not in genres:
            genres.append(genre)
        if book_type not in book_types:
            book_types.append(book_type)
        if author not in authors:
            authors.append(author)

    if (str(field).__eq__("title")):
        print(titles)
        return titles
    elif (str(field).__eq__("link")):
        return links
    elif(str(field).__eq__("genre")):
        return genres
    elif (str(field).__eq__("type")):
        return book_types
    elif (str(field).__eq__("author")):
        return authors


def get_details(link):
        payload = json.dumps({
            "query": {
                "match": {
                    "book_link": link
                }
            }
        })
        response = requests.request("POST", auto_suggest_url, headers=headers, data=payload).json()['hits']['hits'][0]['_source']
        return response

def show_results(links, titles):
    for i in range(0, len(links), 3):
        container_id = f"container_{i}"
        container = st.empty()

        col1, col2, col3 = st.columns(3)
        with col1:
            st.image(links[i], use_column_width="always")
            with st.expander(titles[i]):
                get_details(links[i])

        with col2:
            if (1 + i < len(links)):
                st.image(links[i + 1], use_column_width="always")
                with st.expander(titles[i + 1]):
                    get_details(links[i + 1])

        with col3:
            if (2 + i < len(links)):
                st.image(links[i + 2], use_column_width="always")
                with st.expander(titles[i + 2]):
                    get_details(links[i + 2])

        if st.button("Clear Container"):
            # Clear the container's contents
            container.empty()
            titles=titles.clear()
            links=links.clear()
            # Remove the container from Streamlit
            session_state = st.session_state
            if container_id in session_state:
                del session_state[container_id]



if __name__=="__main__":
    # generate_story("thriller story based on crypto")
    submit_book_details("v","v","v","v","v","v")
#     # index_to_opensearch()
#     get_suggestions("stat")

# show_results(links,titles)






# main_category = st.radio("options", ["Click here if you are looking for the details of a book",
#                                      "Click here if you are looking for a book recommendation",
#                                      "Click here if you are are a first time reader"], index=0)

# Search for a book
# if str(main_category).__eq__("Click here if you are looking for the details of a book"):
#     query=st.text_input("Enter name")
#     for sugg in get_suggestions_link(query):
#         html = f"<img src='link_to_replace'>".replace("link_to_replace",sugg)
#         st.markdown(html, unsafe_allow_html=True)
#     st.write("Here are the book details:")
#
# if str(main_category).__eq__("Click here if you are looking for a book recommendation"):
#     st.write("Choose a genre:")
#     st.write("Here are our reccomendations:")
#
# if str(main_category).__eq__("Click here if you are are a first time reader"):
#     st.write("Please help us get to know about your interests:")
