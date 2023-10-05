import requests
import time

# Endpoint URL
API_URL = 'http://127.0.0.1:8000/recognize_books'  # Change this to your actual API URL

def test_api_with_image(image_path):
    '''Tests the API with a given image'''
    # Load the image file
    with open(image_path, 'rb') as image_file:
        image_bytes = image_file.read()

    # Make a POST request to the API endpoint with the image
    response = requests.post(API_URL, files={'image': image_bytes})

    # Print the response from the API
    print("Response code:", response.status_code)
    print("Books detected:")
    for book in response.json()['books']:
        print(f"Title: {book['title']}, Author: {book['authors']}")

if __name__ == '__main__':
    # Image path for test image
    image_path = "C:\\Projects\\scan-my-shelf\\images\\shelf2.jpg"

    # Call the test function
    start_time = time.time()
    test_api_with_image(image_path)
    print(f"Time elapsed for API call: {time.time() - start_time} seconds.")