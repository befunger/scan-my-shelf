'''Utilities for accessing the Open Library API'''
import requests

def search_books(params):
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


# Book title and author
query = "Dragon Thunder Kalla"
title = "Dragon Thunder"
author = "Kalla"

# Search for the book
# books = search_title_and_author(title, author)
# books = search_title(title)
# books = search_query(query)

# Display book information
print(len(books), "books found.")
if books:
    book = books[0]
    print("Title:", book.get('title', 'N/A'))
    print("Author:", book.get('author_name', ['N/A'])[0])
    print("Publish Year:", book.get('first_publish_year', 'N/A'))
    print("Number of Pages:", book.get('number_of_pages', 'N/A'))
    # print("Publishers:", book.get('publisher', ['N/A'])[0])
    # print("Subjects:", book.get('subject', []))
else:
    print("Book not found.")
