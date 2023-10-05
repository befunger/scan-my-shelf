import requests

# Endpoint URL
API_URL = 'http://127.0.0.1:8000/recognize_books'  # Change this to your actual API URL

def test_api_with_image(image_path):
    '''Tests the API with a given image'''
    # # Load the image file
    # image_file = open(image_path, 'rb')

    # # Make a POST request to the API endpoint with the image
    # response = requests.post(API_URL, files={'image': image_file})

    print("Sending request. This may take a while.")
    # For now, no variable image parameter
    response = requests.post(API_URL, files={})

    # Print the response from the API
    print("Response code:", response.status_code)
    print("Books detected:")
    for book in response.json()['books']:
        print(f"Title: {book['title']}, Author: {book['authors']}")

if __name__ == '__main__':
    # Image path for test image
    image_path = "C:\\Projects\\scan-my-shelf\\images\\shelf3.jpg"

    # Call the test function
    test_api_with_image(image_path)
