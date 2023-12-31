'''Illustrates the full pipeline usage of the application (Similar to server.py, but without launching a server)'''
import time

import googlebooks as books
import rekognition as rek
import image_manipulation as im
import chatgpt as gpt


# Constants used during execution (More testing needed for optimal/dynamic choice)
OBJECT_DETECTION_THRESHOLD = 10
TEXT_DETECTION_THRESHOLD = 90
IMAGE_PATH = "C:\\Projects\\scan-my-shelf\\images\\shelf1.jpg"
MULTI_DETECT = False
VERIFY_BOOK_TITLES = False

# Open image
with open(IMAGE_PATH, 'rb') as image_file:
    image_bytes = image_file.read()

start_time = time.time()

# Initialise Rekognition
rekognition = rek.initialise_rekognition()

# Gets the bounding boxes of all detected books (including )
bounding_boxes = rek.detect_books(rekognition, image_bytes, OBJECT_DETECTION_THRESHOLD, TEXT_DETECTION_THRESHOLD)

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
results = set()
print("----")
for search_term in search_queries:
    result = books.search_books(search_term)
    print("Search term:", search_term)
    if not result is None and result['totalItems'] > 0:
        item = result['items'][0] # Gets the first result. Note that this seems to often turn up very irrelevant
        volume_info = item['volumeInfo']
        # entry = f"Title: {volume_info.get('title')}\nAuthors: {', '.join(volume_info.get('authors', ['N/A']))}\nRating: {volume_info.get('averageRating')}\nSummary: {volume_info.get('description')}"
        entry = f"Title: {volume_info.get('title')}\nAuthors: {', '.join(volume_info.get('authors', ['N/A']))}"
        results.add(entry)
        print(f'{entry}\n----')
    else:
        print("No book found for the extracted text.\n----")


print(f"Time elapsed for API call: {time.time() - start_time} seconds.")
