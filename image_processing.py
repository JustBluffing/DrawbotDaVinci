import cv2
import numpy as np

def load_image(image_path):
    """
    Loads an image from the specified file path.

    Args:
        image_path (str): The file path of the image.

    Returns:
        image (numpy.ndarray): The original image in BGR format.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise IOError(f"Image {image_path} not found or cannot be read.")
    return image

def preprocess_image(image, resize_factor=1.0):
    """
    Performs preprocessing: optionally scales the image, converts it to grayscale, 
    and applies Gaussian blur.

    Args:
        image (numpy.ndarray): The original image.
        resize_factor (float, optional): Scaling factor to reduce the image resolution. Default is 1.0 (no scaling).

    Returns:
        gray (numpy.ndarray): The preprocessed grayscale image.
    """
    # Scale the image according to the desired factor
    if resize_factor != 1.0:
        width = int(image.shape[1] * resize_factor)
        height = int(image.shape[0] * resize_factor)
        image = cv2.resize(image, (width, height))

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    return gray

def detect_edges(image_gray, low_threshold=50, high_threshold=150):
    """
    Detects edges in the given grayscale image using the Canny algorithm.

    Args:
        image_gray (numpy.ndarray): The grayscale image.
        low_threshold (int, optional): Lower threshold for the Canny algorithm. Default is 50.
        high_threshold (int, optional): Upper threshold for the Canny algorithm. Default is 150.

    Returns:
        edges (numpy.ndarray): Binary image with the detected edges.
    """
    edges = cv2.Canny(image_gray, low_threshold, high_threshold)
    return edges

def find_contours(edges):
    """
    Finds contours in the edge image.

    Args:
        edges (numpy.ndarray): Binary image for edge detection.

    Returns:
        contours (list): List of detected contours.
    """
    # Note: cv2.findContours returns different values depending on the version of OpenCV.
    contours_data = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours_data[0] if len(contours_data) == 2 else contours_data[1]
    return contours

def draw_contours(image, contours):
    """
    Draws the detected contours on the provided image.

    Args:
        image (numpy.ndarray): Image data on which to draw.
        contours (list): List of contours.

    Returns:
        image_with_contours (numpy.ndarray): Image with the contours drawn.
    """
    image_with_contours = image.copy()
    cv2.drawContours(image_with_contours, contours, -1, (0, 255, 0), 2)
    return image_with_contours

"""
if __name__ == "__main__":
    # Testing section: if you run the module directly, this section will be executed.
    import sys

    if len(sys.argv) < 2:
        print("Usage: python image_processing.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    
    # Load and preprocess the image
    original_image = load_image(image_path)
    gray_image = preprocess_image(original_image, resize_factor=0.5)
    
    # Edge detection
    edges = detect_edges(gray_image)
    
    # Find contours
    contours = find_contours(edges)
    
    # Draw contours on the original image
    image_with_contours = draw_contours(original_image, contours)
    
    # Display the results
    cv2.imshow("Original Image", original_image)
    cv2.imshow("Gray & Blurred Image", gray_image)
    cv2.imshow("Edges", edges)
    cv2.imshow("Contours", image_with_contours)
    cv2.waitKey(0)
    cv2.destroyAllWindows()





if __name__ == "__main__":
    import cv2
    import sys

    if len(sys.argv) < 2:
        print("Usage: python image_processing.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]

    try:
        # Load the original image
        original_image = load_image(image_path)
        cv2.imshow("Original Image", original_image)
        
        # Preprocess the image (convert to grayscale and apply Gaussian blur)
        gray_image = preprocess_image(original_image, resize_factor=0.5)
        cv2.imshow("Gray & Blurred Image", gray_image)
        
        # Detect edges
        edges = detect_edges(gray_image)
        cv2.imshow("Edges", edges)
        
        # Find contours and draw them on the original image
        contours = find_contours(edges)
        image_with_contours = draw_contours(original_image, contours)
        cv2.imshow("Contours", image_with_contours)
        
        print("Press 'q' to quit the program.")
        # Use a loop with waitKey to check for a quit command (e.g., the 'q' key)
        while True:
            # waitKey(1) checks every millisecond for a key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Quit command received.")
                break
    except KeyboardInterrupt:
        # Allows the program to be interrupted by Ctrl+C in the CMD
        print("Program interrupted by user.")
    finally:
        cv2.destroyAllWindows()

# Example usage:
# python image_processing.py example.jpg
"""
