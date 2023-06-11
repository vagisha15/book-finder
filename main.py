import streamlit as st
import requests
import json
import openai
from constants import AUTO_SUGGEST_URL, ADD_DATA_URL, HEADERS , BOOK_TITLE_WRAPPER, BOOK_LINK , AUTHOR ,\
                        STRIKETHROUGH , BOOK_TYPE , GENRE ,SOURCE, QUERY , MATCH , HITS , BY , MULTIMATCH


def submit_book_details(title, author, book_link, price, book_type, genre):
    # Submit book details to the database
    payload = json.dumps({
        BOOK_TITLE_WRAPPER: title,
        BOOK_LINK: book_link,
        AUTHOR: author,
        STRIKETHROUGH : price,
        BOOK_TYPE: book_type,
        GENRE: genre
    })

    response = requests.request("POST", ADD_DATA_URL, headers=HEADERS, data=payload)
    if response.status_code == 201:
        return "SUCCESS"
    else:
        return "FAILED"

def get_metadata_for_rating(image_url):
    # Retrieve metadata for a book based on its image URL
    payload = json.dumps({
        QUERY: {
            MATCH: {
                BOOK_LINK: image_url
            }
        }
    })
    response = requests.request("POST", AUTO_SUGGEST_URL, headers=HEADERS, data=payload).json()[HITS][HITS][0][SOURCE]

    # Extract metadata fields with error handling
    author = response.get(AUTHOR, "").replace(BY, "")
    title = response.get(BOOK_TITLE_WRAPPER, "")
    book_type = response.get(BOOK_TYPE, "")
    genre = response.get(GENRE, "")
    price = response.get(STRIKETHROUGH, "")

    return author, title, book_type, genre, price

def fetch_response(query, auth_filter, genre_filter, type_filter):
    # Fetch response from the search API based on query and filters
    if "-" in str(auth_filter):
        # Construct payload with filters
        payload = json.dumps({
            QUERY: {
                "bool": {
                    "must": [
                        {
                            MATCH: {
                                str(auth_filter.split("-")[0]): str(auth_filter.split("-")[1]).replace(BY, "")
                            }
                        },
                        {
                            MATCH: {
                                str(genre_filter.split("-")[0]): str(genre_filter.split("-")[1])
                            }
                        },
                        {
                            MATCH: {
                                str(type_filter.split("-")[0]): str(type_filter.split("-")[1])
                            }
                        },
                        {
                            MATCH: {
                                BOOK_TITLE_WRAPPER: query
                            }
                        }
                    ]
                }
            }
        })
    else:
        # Construct payload without filters
        payload = json.dumps({
            SOURCE: [BOOK_TITLE_WRAPPER, BOOK_LINK, GENRE, BOOK_TYPE, AUTHOR],
            QUERY: {
                MULTIMATCH: {
                    QUERY: query,
                    "type": "bool_prefix",
                    "fields": [
                        BOOK_TITLE_WRAPPER,
                        "book_title_wrapper._2gram",
                        "book_title_wrapper._3gram"
                    ]
                }
            }
        })

    response = requests.request("POST", AUTO_SUGGEST_URL, headers=HEADERS, data=payload).json()[HITS][HITS]
    return response

def get_results(field, response):
    # Extract relevant fields from the search response
    titles = []
    links = []
    genres = []
    book_types = []
    authors = []

    for resp in response:
        title = resp[SOURCE][BOOK_TITLE_WRAPPER]
        link = resp[SOURCE][BOOK_LINK]
        genre = resp[SOURCE][GENRE]
        book_type = resp[SOURCE][BOOK_TYPE]
        author = resp[SOURCE][AUTHOR]

        # Append unique values to respective lists
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

    if field == "title":
        return titles
    elif field == "link":
        return links
    elif field == "genre":
        return genres
    elif field == "type":
        return book_types
    elif field == "author":
        return authors

def get_details(link):
    # Retrieve details of a book based on its link
    payload = json.dumps({
        QUERY: {
            MATCH: {
                BOOK_LINK: link
            }
        }
    })
    response = requests.request("POST", AUTO_SUGGEST_URL, headers=HEADERS, data=payload).json()[HITS][HITS][0][SOURCE]
    return response

if __name__ == "__main__":
    pass
