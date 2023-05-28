from flask import Flask, jsonify, request, render_template

import main

app = Flask(__name__)

# Example function to process user input and retrieve the list of image URLs
def process_user_input(query,field):
    # Replace this with your own logic to process the user input and fetch the image URLs
    titles = main.get_results(query, "title")
    links = main.get_results(query, "link")
    authors = main.get_results(query, "author")
    book_types = main.get_results(query, "type")
    genres = main.get_results(query, "genre")

    if (str(field).__eq__("title")):
        return titles
    elif (str(field).__eq__("link")):
        return links
    elif (str(field).__eq__("genre")):
        return genres
    elif (str(field).__eq__("type")):
        return book_types
    else:
        return authors

@app.route('/')
def home():
    return render_template('src.html')

# API endpoint to process user input and get the list of images
@app.route('/api/images', methods=['POST'])
def get_images():
    input_data = request.get_json()
    input_string = input_data.get('inputString')
    image_urls = process_user_input(input_string,"link")
    titles=process_user_input(input_string,"title")
    authors= process_user_input(input_string,"author")
    types=process_user_input(input_string,"book_types")
    genres = process_user_input(input_string,"genre")
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
