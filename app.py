from flask import Flask, jsonify, request, render_template

import main

app = Flask(__name__)

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
