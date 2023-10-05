'''Utilities for accessing and using the Amazon Rekognition API'''

# For Amazon Rekognition API
import boto3

def initialise_rekognition():
    '''Initialize the Amazon Rekognition client'''
    return boto3.client('rekognition')


def detect_labels(rekognition, image):
    '''
    Prints out information about detected labels in an image using Amazon Rekognition
    image: image to be used
    '''

    response = rekognition.detect_labels(
        Image={'Bytes': image},
        MaxLabels=10  # Maximum number of labels to return
    )

    labels = response['Labels']
    for label in labels:
        print(f"Label: {label['Name']}, Confidence: {label['Confidence']}")


def detect_books(rekognition, image, object_threshold=10, text_threshold=90):
    '''
    Function for extracting bounding boxes of the books in a given image
    image_bytes: image to be inspected (loaded as bytes)
    confidence_threshold: Required confidence for including an object detection
    '''

    # Get bounding box information of book objects
    book_information = get_book_bounding_boxes(rekognition, image, object_threshold)

    # Perform text detection for each book
    for detection in book_information:
        bounding_box = detection['BoundingBox']
        # Extract text within bounding box
        extracted_text = extract_text_from_bounding_box(rekognition, image, bounding_box, text_threshold)
        detection['ExtractedText'] = extracted_text

    return book_information

def get_book_bounding_boxes(rekognition, image_bytes, confidence_threshold):
    '''Returns list of bounding boxes detected for book-relevant labels'''

    # Detect labels (objects) in the image
    response = rekognition.detect_labels(
        Image={'Bytes': image_bytes},
        MaxLabels=20,  # Maximum number of labels to return
        MinConfidence=confidence_threshold  # Confidence threshold for detected labels
    )

    book_information = []

    for label in response['Labels']:
        # Check if the label is book or book-related
        if 'Book' in label['Name'] or 'Page' in label['Name'] or 'Publication' in label['Name']:
            for instance in label['Instances']:
                bounding_box = instance['BoundingBox']
                # Save relevant information
                book_information.append({
                    'Label': label['Name'],
                    'Confidence': instance['Confidence'],
                    'BoundingBox': bounding_box
                })

    return book_information


def extract_text_from_bounding_box(rekognition, image_bytes, bounding_box, confidence_threshold):
    '''Extract text from a bounding box using Amazon Rekognition'''
    # Create filter for image based on bounding box
    bounding_box_filter = {
      "RegionsOfInterest": [ 
         {"BoundingBox": bounding_box}
      ],
      "WordFilter": { 
         "MinBoundingBoxHeight": 0,
         "MinBoundingBoxWidth": 0,
         "MinConfidence": confidence_threshold
      }
   }

    # Use Amazon Rekognition to detect text in the region
    response = rekognition.detect_text(Image={'Bytes': image_bytes}, Filters=bounding_box_filter)

    # Extract text detected in the region
    extracted_text = ''
    for text_detection in response['TextDetections']:
        if text_detection['Type'] == 'LINE':
            extracted_text += text_detection['DetectedText'] + ' '

    return extracted_text.strip()
