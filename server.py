'''Illustrates the full pipeline usage of the application'''

import googlebooks as books
import rekognition as rek
import chatgpt as gpt
from flask import Flask, request, jsonify



app = Flask(__name__)

def recognize_books(IMAGE_PATH):
    # Constants used during execution (More testing needed for optimal/dynamic choice)
    OBJECT_DETECTION_THRESHOLD = 10
    TEXT_DETECTION_THRESHOLD = 90
    MULTI_DETECT = False
    VERIFY_BOOK_TITLES = True

    '''Takes an image input and returns json with detected books and information'''
    # Initialise Rekognition
    rekognition = rek.initialise_rekognition()

    # Gets the bounding boxes of all detected books (including )
    bounding_boxes = rek.detect_books(rekognition, IMAGE_PATH, OBJECT_DETECTION_THRESHOLD, TEXT_DETECTION_THRESHOLD)

    # Get extracted text from each book detected
    extracted_texts = [box['ExtractedText'] for box in bounding_boxes]

    # Get author/title search query from extracted text
    search_queries = set()
    for text in extracted_texts:
        gpt_response = gpt.get_titles_from_text(text, MULTI_DETECT)
        for book, author in zip(gpt_response['book'], gpt_response['author']):
            search_queries.add(f'{book}, {author}')

    if VERIFY_BOOK_TITLES:
        search_queries = [query for query in search_queries if gpt.verify_book(query)]

    # Get Google Books result from search queries
    results = []
    for search_term in search_queries:
        result = books.search_books(search_term)
        if not result is None and result['totalItems'] > 0:
            item = result['items'][0] # Gets the first result. Note that this seems to often turn up very irrelevant results when the query is poor
            volume_info = item['volumeInfo']
            entry = {'title' : volume_info.get('title'), 'authors' : ', '.join(volume_info.get('authors', ['N/A'])), 'rating' : volume_info.get('averageRating'), 'summary' : volume_info.get('description')}
            results.append(entry)

    # Convert set of results into json
    return {"books": results}


@app.route('/recognize_books', methods=['POST'])
def recognize_books_endpoint():
    '''Endpoint for receiving API requests to detect books'''
    # # Check if the request contains a file
    # if 'image' not in request.files:
    #     return jsonify({"error": "No image file provided"})

    # # Get the image from the request
    # image_path = request.files['image']

    image_path = "C:\\Projects\\scan-my-shelf\\images\\shelf3.jpg"
    # Call your recognition function
    extracted_books = recognize_books(image_path)

    # Return the extracted book information as JSON response
    return jsonify(extracted_books)



if __name__ == '__main__':
    app.run(debug=True, port=8000)