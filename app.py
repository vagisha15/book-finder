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

@app.route('/templates/login.html')
def return_login_page():
    return render_template('login.html')

@app.route('/templates/signup.html')
def return_signup_page():
    return render_template('signup.html')

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

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('data/users.db')
        return conn
    except sqlite3.Error as e:
        print(e)

# Function to create the users table if it doesn't exist
def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           username TEXT NOT NULL,
                           password TEXT NOT NULL,
                           email TEXT NOT NULL,
                           fname TEXT NOT NULL,
                           lname TEXT);''')
        conn.commit()
    except sqlite3.Error as e:
        print(e)

# Function to insert a new user into the database
def insert_user(conn, username, password):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                       (username, password))
        conn.commit()
        print("User inserted successfully.")
    except sqlite3.Error as e:
        print(e)

# Function to retrieve a user by username from the database
def get_user(conn, username):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        return user
    except sqlite3.Error as e:
        print(e)

# Function to check if a given username exists in the database
def is_username_taken(conn, username):
    user = get_user(conn, username)
    if user:
        return True
    else:
        return False

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get("username")
    password = request.form.get("password")

    conn = create_connection()

    if conn is not None:
        if is_username_taken(conn, username):
            response = {"success": False, "message": "Username already taken."}
        else:
            insert_user(conn, username, password)
            response = {"success": True, "message": "User registered successfully."}
    else:
        response = {"success": False, "message": "Error: Could not establish a database connection."}

    return jsonify(response)

@app.route('/login', methods=['POST'])
def login():
    # Retrieve user data from the request
    username = request.form.get("username")
    password = request.form.get("password")

    # Create a connection to the database
    conn = create_connection()

    if conn is not None:
        # Get the user from the database
        user = get_user(conn, username, password)
        if user:
            response = {"success": True, "message": "Login successful."}
        else:
            response = {"success": False, "message": "Invalid username or password."}
    else:
        response = {"success": False, "message": "Error: Could not establish a database connection."}

    # Return the response as JSON
    return jsonify(response)

@app.route('/generateIdeas', methods=['POST'])
def generateIdeas(prompt: str):
    prompt = request.json.get('prompt')

    
    openai.api_key = openai_secret_key
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=1000
    )

    # Extract the generated ideas from the response
    ideas = response.choices[0].text.strip()

    return jsonify({'ideas': ideas})




if __name__ == '__main__':
    with create_connection() as conn:
        create_table(conn)
    app.run()
