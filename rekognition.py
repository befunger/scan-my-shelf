'''Utilities for accessing and using the Amazon Rekognition API'''

# For image manipulation (Cropping a sub-image for text detection)
import io
from PIL import Image

# For Amazon Rekognition
import boto3

def initialise_rekognition():
    '''Initialize the Amazon Rekognition client'''
    return boto3.client('rekognition')


def detect_labels(rekognition, image_path):
    '''
    Prints out information about detected labels in an image using Amazon Rekognition
    image_path: file path to the image to be used
    '''
    with open(image_path, 'rb') as image_file:
        image_bytes = image_file.read()

    response = rekognition.detect_labels(
        Image={'Bytes': image_bytes},
        MaxLabels=10  # Maximum number of labels to return
    )

    labels = response['Labels']
    for label in labels:
        print(f"Label: {label['Name']}, Confidence: {label['Confidence']}")


def detect_books(rekognition, image_path, confidence_threshold=50):
    '''
    Function for extracting bounding boxes of the books in a given image
    image_path: File path to image to be inspected
    confidence_threshold: Required confidence for including a label
    '''
    # Load the image as bytes
    with open(image_path, 'rb') as image_file:
        image_bytes = image_file.read()

    # Detect labels (objects) in the image
    response = rekognition.detect_labels(
        Image={'Bytes': image_bytes},
        MaxLabels=20,  # Maximum number of labels to return
        MinConfidence=confidence_threshold  # Confidence threshold for detected labels
    )

    # Initialize a list to store bounding boxes of books
    book_bounding_boxes = []

    # Iterate through the detected labels
    for label in response['Labels']:
        # Check if the label is book or book-related
        if 'Book' in label['Name'] or 'Page' in label['Name'] or 'Publication' in label['Name']:
            for instance in label['Instances']:
                bounding_box = instance['BoundingBox']
                # Get text from within the bounding box
                extracted_text = extract_text_from_bounding_box(rekognition, image_bytes, bounding_box)
                # Save relevant information
                book_bounding_boxes.append({
                    'Label': label['Name'],
                    'Confidence': instance['Confidence'],
                    'BoundingBox': bounding_box,
                    'ExtractedText' : extracted_text
                })

    return book_bounding_boxes


def extract_text_from_bounding_box(rekognition, image_bytes, bounding_box):
    '''Extract text from a bounding box using Amazon Rekognition'''
    # Get image dimensions
    image_width, image_height = Image.open(io.BytesIO(image_bytes)).size

    # Extract bounding box coordinates
    left = int(bounding_box['Left'] * image_width)
    top = int(bounding_box['Top'] * image_height)
    width = int(bounding_box['Width'] * image_width)
    height = int(bounding_box['Height'] * image_height)

    # Crop the region from the image
    region_image = Image.open(io.BytesIO(image_bytes)).crop((left, top, left + width, top + height))

    # Convert cropped image to bytes
    region_image_bytes = io.BytesIO()
    region_image.save(region_image_bytes, format='JPEG')
    region_image_bytes = region_image_bytes.getvalue()

    # Use Amazon Rekognition to detect text in the region
    response = rekognition.detect_text(Image={'Bytes': region_image_bytes})

    # Extract text detected in the region
    extracted_text = ''
    for text_detection in response['TextDetections']:
        if text_detection['Type'] == 'LINE':
            extracted_text += text_detection['DetectedText'] + ' '

    return extracted_text.strip()
