import json
import pandas as pd
import requests

book_metadata=dict()
indexing_url = "https://search-books-main-5xruavjoyo7mq2fem4jwni4ace.ap-south-1.es.amazonaws.com/books_main/_doc"
headers = {
        'Authorization': 'Basic b3BlbnNlYXJjaC1ib29rczpCb29rc0AyMDIz',
        'Content-Type': 'application/json'
    }
def read_one_csv():
    og_path='/Users/vagishasharma/Documents/suggest-books/file_name_to_replace.csv'
    for i in range (1,2):
        path=og_path.replace("file_name_to_replace",str(i))
        df = pd.read_csv(path, encoding='latin-1')
        cols=df.columns.values
        json_data = df.to_json(orient='records')
        json_obj = json.loads(json_data)
        for obj in json_obj:
            temp_dict=dict()
            for col in cols:
                temp_dict[str(col).replace("-","_").replace(" ","_")]=obj[col]
            book_metadata[temp_dict['book_title_wrapper']]=temp_dict
        print("Finished extracting : "+ path)

def index_to_opensearch():
    for item in book_metadata:
        payload = json.dumps(book_metadata[item])
        response = requests.request("POST", indexing_url, headers=headers, data=payload)

def read_all_csv():
    og_path='/Users/vagishasharma/Documents/suggest-books/file_name_to_replace.csv'
    for i in range (1,9):
        path=og_path.replace("file_name_to_replace",str(i))
        df = pd.read_csv(path, encoding='latin-1')
        cols=df.columns.values
        json_data = df.to_json(orient='records')
        json_obj = json.loads(json_data)
        for obj in json_obj:
            temp_dict=dict()
            for col in cols:
                temp_dict[str(col).replace("-","_").replace(" ","_")]=obj[col]
            book_metadata[temp_dict['book_title_wrapper']]=temp_dict
        print("Finished extracting : "+ path)
