import streamlit as st
import requests
import json

auto_suggest_url = "https://search-books-main-5xruavjoyo7mq2fem4jwni4ace.ap-south-1.es.amazonaws.com/books_main/_search"
headers = {
        'Authorization': 'Basic b3BlbnNlYXJjaC1ib29rczpCb29rc0AyMDIz',
        'Content-Type': 'application/json'
    }
def get_results(query,field):
    titles=[]
    links=[]
    genres=[]
    book_types=[]
    authors=[]
    payload = json.dumps({
        "_source": ["book_title_wrapper","book_image_src","Book_by_Genre","book_type","book_author"],
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
        return titles
    elif (str(field).__eq__("link")):
        return links
    elif(str(field).__eq__("genre")):
        return genres
    elif (str(field).__eq__("type")):
        return book_types
    else:
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
        st.write("Link to Buy: "+response["book_link"] )
        st.write("Author: "+response["book_author"] )
        st.write("Genre: "+response["Book_by_Genre"] )

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



# if __name__=="__main__":
#     # read_one_csv()
#     # index_to_opensearch()
#     get_suggestions("stat")
st.title("Looking for a book?")
st.header("We are here to help.")
query=st.text_input("Enter name")
titles=get_results(query,"title")
links=get_results(query,"link")
authors_list=get_results(query,"author")
type_list=get_results(query,"type")
genre_list=get_results(query,"genre")

if(len(links)>0):
    author_filter = st.sidebar.selectbox("Author", authors_list)
    book_type_filter = st.sidebar.selectbox("Book Type", type_list)
    book_type_filter = st.sidebar.selectbox("Genre", genre_list)
    show_results(links,titles)

if ((not(query.__eq__(""))) and len(links)<0):
    st.write("No results matching your criteria")





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
