from flask import Flask, jsonify, request, render_template, send_file
import sqlite3
import main
import os
from dotenv import load_dotenv
import openai
load_dotenv()
app = Flask(__name__)

#setting up variables
openai_secret_key = os.environ.get("OPENAI_SECRET_KEY")
username=""

# Example function to process user input and retrieve the list of image URLs
def process_user_input(field,response):
    options = []
    # Replace this with your own logic to process the user input and fetch the image URLs
    if str(field) == "title":
        titles = main.get_results("title", response)
        options = titles
    elif str(field) == "link":
        links = main.get_results("link", response)
        options = links
    elif str(field) == "genre":
        genres = main.get_results("genre", response)
        options = genres
    elif str(field) == "type":
        book_types = main.get_results("type", response)
        options = book_types
    else:
        authors = main.get_results("author", response)
        options = authors

    return options


@app.route('/')
def home():
    return render_template('src.html')

@app.route('/templates/menu.html')
def return_menu():
    return render_template('menu.html')

@app.route('/templates/writer.html')
def return_writer_page():
    return render_template('writer.html')

@app.route('/templates/about.html')
def return_about_page():
    return render_template('about.html')

@app.route('/api/submit-book-details',methods=['POST'])
def submit_book_details():
    title = request.json['title']
    author = request.json["author"]
    book_link = request.json["bookLink"]
    price = request.json["price"]
    book_type = request.json["bookType"]
    genre = request.json["genre"]
    return {"response_message":"SUCCESS"}

@app.route('/api/book-details',methods=['POST'])
def get_book_rating():
    image_url = request.json['imageUrl']
    author,title,type,genre,price = main.get_metadata_for_rating(image_url)
    return render_template('rating.html',book_title= title,author_name=author,genre=genre,
                           type=type,price=price,book_link=image_url)

# API endpoint to process user input and get the list of images
@app.route('/api/images', methods=['POST'])
def get_images():
    input_data = request.get_json()
    if 'filterValue' in input_data:
        input_string = input_data.get('inputString')
        fqs= str(input_data.get('filterValue')).split('|')
        auth_filter= fqs[0]
        genre_filter=fqs[1]
        type_filter=fqs[2]
        response=main.fetch_response(input_string,auth_filter,genre_filter,type_filter)
        image_urls = process_user_input("link",response)
        titles = process_user_input("title",response)
        authors = process_user_input("author",response)
        types = process_user_input("type",response)
        genres = process_user_input("genre",response)
    else:
        input_string = input_data.get('inputString')
        response = main.fetch_response(input_string, "","","")
        image_urls = process_user_input("link",response)
        titles=process_user_input("title",response)
        authors= process_user_input("author",response)
        types=process_user_input("type",response)
        genres = process_user_input("genre",response)
    return jsonify({'imageUrls': image_urls,'titles':titles,'authors':authors,'types':types,'genres':genres})

@app.route('/api/metadata',methods=['POST'])
def get_metadata():
    img_url= request.get_json()
    link = img_url.get('imageUrl')
    metadata= main.get_details(link)
    return {"bookLink": metadata["book_link"],"author": metadata["book_author"],
            "genre": metadata["Book_by_Genre"]}

if __name__ == '__main__':
    app.run()
