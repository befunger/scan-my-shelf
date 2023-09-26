'''Utilities for accessing the Google Books API'''

# For making HTTP requests to the Google Books API
import requests

def get_credentials():
    '''Retrieves credentials for Google Books API'''
    with open("../API/GoogleBooks.txt", 'r') as f:
        GOOGLE_BOOKS_API_KEY = f.read().strip('key=')
    GOOGLE_BOOKS_API_BASE_URL = "https://www.googleapis.com/books/v1/volumes"

    return {'key': GOOGLE_BOOKS_API_KEY, 'URL' : GOOGLE_BOOKS_API_BASE_URL}

def search_books(query):
    '''Search for a book query using the Google Books API'''
    # Get credentials for API usage
    credentials = get_credentials()
    params = {
        'q': query,
        'key': credentials['key']
    }

    response = requests.get(credentials['URL'], params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code}")
        return None
