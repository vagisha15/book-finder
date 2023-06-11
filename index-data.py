import json
import pandas as pd
import requests
from constants import INDEXING_URL, HEADERS , MASTER_FILES_PATH, FILE_NAME_TO_REPLACE, EMPTY_STRING ,UNDERSCORE, BOOK_TITLE_WRAPPER

book_metadata = {}


def read_csv_files(file_path_template, start_index, end_index):
    for i in range(start_index, end_index + 1):
        path = file_path_template.replace(FILE_NAME_TO_REPLACE, str(i))
        df = pd.read_csv(path, encoding='latin-1')
        cols = df.columns.values
        json_data = df.to_json(orient='records')
        json_obj = json.loads(json_data)
        for obj in json_obj:
            temp_dict = {}
            for col in cols:
                temp_dict[str(col).replace("-", UNDERSCORE).replace(EMPTY_STRING, UNDERSCORE)] = obj[col]
            book_metadata[temp_dict[BOOK_TITLE_WRAPPER]] = temp_dict
        print("Finished extracting: " + path)


def index_to_opensearch():
    for item in book_metadata:
        payload = json.dumps(book_metadata[item])
        response = requests.request("POST", INDEXING_URL, headers=HEADERS, data=payload)


if __name__ == "__main__":
    file_path_template = MASTER_FILES_PATH
    start_index = 1
    end_index = 8

    read_csv_files(file_path_template, start_index, end_index)
    index_to_opensearch()
