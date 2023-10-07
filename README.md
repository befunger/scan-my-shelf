# scan-my-shelf
An ongoing project to develop an application for book enthusiasts. This repo is still very much a work in progress!

This repo contains the backend API for the [scan-my-shelf mobile app](https://github.com/befunger/scan-my-shelf-mobile/) developed in Python using Flask.

# Installation
* To run this project locally, clone the repository.
    ```
    git clone https://github.com/befunger/scan-my-shelf.git
    ```
* Create a [Conda](https://docs.conda.io/en/latest/) environment using the [environment.yml](https://github.com/befunger/scan-my-shelf/blob/main/environment.yml) file:
    ```
    conda env create -f environment.yml
    conda activate scan-my-shelf
    ```

* Run the application:
    ```
    python server.py
    ```

* Once the server is running, the API_URL should be displayed in the terminal:
    ```
    * Running on <API_URL>
    ```

# Usage
Once the server is running, API calls can be made to the **/recognize_books** endpoint. The POST should contain an image file used for detecting books.

* Example using the requests package for Python:
    ```
    response = requests.post(<API_URL>/recognize_books, files={'image': image_bytes})
    ```

* The API returns a json containing detected book objects, each containing multiple fields of information:
    ```
    response: {'books': ['book_1', 'book_2', 'book_3']}
    book_1: {'title': 'Ella Minnow Pea', 'author': 'Mark Dunn', 'rating': '5.0', [...]}
    ```
