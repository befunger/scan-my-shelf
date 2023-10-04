'''Utilities for accessing the Open Library API'''
import requests

def search_books(params):
    '''Searches for books in the Open Library database using the supplied parameters'''
    base_url = "https://openlibrary.org/search.json?"

    response = requests.get(f"{base_url}", params=params)

    if response.status_code == 200:
        data = response.json()
        return data['docs']
    else:
        print("Error:", response.status_code)
        return None


def search_title(title):
    '''Search book using only title'''
    params = {"title": title}
    return search_books(params)

def search_title_and_author(title, author):
    '''Search book with both author and title'''
    params = {"title": title, "author": author}
    return search_books(params)

def search_query(query):
    '''Search book with query'''
    params = {"q": query}
    return search_books(params)
