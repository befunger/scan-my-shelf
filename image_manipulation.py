'''Utilities for image manipulation, mostly in regards to bounding boxes and cropping'''
import cv2 # For image manipulation

# For plotting/debugging visualisation
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def display_bounding_boxes(image_path, bounding_boxes):
    '''Display bounding boxes overlaid on the original image'''
    # Load the original image
    original_image = cv2.imread(image_path)
    original_image_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

    # Create a figure and axis
    _, ax = plt.subplots()

    # Display the original image
    ax.imshow(original_image_rgb)

    # Iterate through each bounding box and plot the cropped region
    for _, box in enumerate(bounding_boxes, start=1):
        # Extract the bounding box coordinates
        image_height, image_width, _ = original_image.shape
        left = int(box['BoundingBox']['Left'] * image_width)
        top = int(box['BoundingBox']['Top'] * image_height)
        width = int(box['BoundingBox']['Width'] * image_width)
        height = int(box['BoundingBox']['Height'] * image_height)

        # Create a rectangle patch for the bounding box
        rect = patches.Rectangle((left, top), width, height, linewidth=1, edgecolor='r', facecolor='none')
        ax.add_patch(rect)

    plt.axis('off')
    plt.show()

def display_cropped_images_separately(image_path, bounding_boxes):
    '''Displays a list of subimages cropped based on bounding boxes'''
    # Load the original image
    original_image = cv2.imread(image_path)
    original_image_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

    # Create a grid for displaying cropped images
    num_images = len(bounding_boxes)
    fig, axes = plt.subplots(1, num_images, figsize=(15, 5))

    # Iterate through each bounding box and display the cropped region
    for idx, box in enumerate(bounding_boxes):
        # Extract the bounding box coordinates
        image_height, image_width, _ = original_image.shape
        left = int(box['BoundingBox']['Left'] * image_width)
        top = int(box['BoundingBox']['Top'] * image_height)
        width = int(box['BoundingBox']['Width'] * image_width)
        height = int(box['BoundingBox']['Height'] * image_height)

        # Crop the book region from the original image
        cropped_book_image = original_image_rgb[top:top+height, left:left+width]

        # Display the cropped image
        axes[idx].imshow(cropped_book_image)
        axes[idx].axis('off')
        axes[idx].set_title(f"Book {idx+1}\nLabel: {box['Label']}\nConfidence: {box['Confidence']:.2f}")

    plt.tight_layout()
    plt.show()


def get_sub_image(image_path, box):
    '''Crop down a subimage from an image using a bounding box'''
    # Load original image
    original_image = cv2.imread(image_path)
    original_image_rgb = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

    # Extract the bounding box coordinates
    image_height, image_width, _ = original_image.shape
    left = int(box['BoundingBox']['Left'] * image_width)
    top = int(box['BoundingBox']['Top'] * image_height)
    width = int(box['BoundingBox']['Width'] * image_width)
    height = int(box['BoundingBox']['Height'] * image_height)

    # Crop the book region from the original image
    cropped_book_image = original_image_rgb[top:top+height, left:left+width]

    return cropped_book_image
