'''Simulates the client-side making API calls to the server.py endpoint'''
import time

import requests

# Endpoint URL
API_URL = 'http://192.168.56.1:8001/recognize_books'  # Change this to your actual API URL

def test_api_with_image(image):
    '''Tests the API with a given image'''
    # Load the image file
    with open(image, 'rb') as image_file:
        image_bytes = image_file.read()

    # Make a POST request to the API endpoint with the image
    response = requests.post(API_URL, files={'image': image_bytes})

    # Print the response from the API
    print("Response code:", response.status_code)
    for index, book in enumerate(response.json()['books'], start=1):
        print(f"Book {index}.\n    Title: {book['title']}\n    Author: {book['author']}")

def test_api_without_image():
    '''Tests the API without providing an image'''
    # Make a POST request to the API endpoint with the image
    response = requests.post(API_URL)

    # Print the response from the API
    print("Response code:", response.status_code)

if __name__ == '__main__':
    # Image path for test image
    IMAGE_PATH = "C:\\Projects\\scan-my-shelf\\images\\shelf1.jpg"

    # Call the test function
    start_time = time.time()
    test_api_with_image(IMAGE_PATH)
    print(f"Time elapsed for API call: {time.time() - start_time} seconds.")

    start_time = time.time()
    test_api_without_image() # Send empty request to verify behaviour
    print(f"Time elapsed for empty API call: {time.time() - start_time} seconds.")
