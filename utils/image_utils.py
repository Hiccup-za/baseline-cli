"""
OpenCV image processing utilities for visual testing.
"""
import os
import cv2
import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity as ssim


def load_image(image_path):
    """
    Load an image using OpenCV.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        ndarray: Loaded image in BGR format
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    # Load image in BGR format (OpenCV default)
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Failed to load image: {image_path}")
    
    return image


def compare_images(img1_path, img2_path, threshold=0.95, output_path=None):
    """
    Compare two images and highlight differences.
    
    Args:
        img1_path (str): Path to first image
        img2_path (str): Path to second image
        threshold (float): Similarity threshold (0.0 to 1.0)
        output_path (str, optional): Path to save difference image
        
    Returns:
        tuple: (similarity_score, difference_image)
    """
    # Load images
    img1 = load_image(img1_path)
    img2 = load_image(img2_path)
    
    # Ensure same dimensions
    if img1.shape != img2.shape:
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
    
    # Convert to grayscale
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    # Calculate structural similarity index
    (score, diff) = ssim(gray1, gray2, full=True)
    
    # Create visual difference image
    diff = (diff * 255).astype("uint8")
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    
    # Find contours
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    
    # Create diff image with bounding boxes
    diff_image = img2.copy()
    for c in contours:
        area = cv2.contourArea(c)
        if area > 40:  # Filter small differences
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(diff_image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    
    if output_path is not None:
        cv2.imwrite(output_path, diff_image)
    
    return score, diff_image


def find_template(screenshot_path, template_path, threshold=0.8):
    """
    Find a template image within a screenshot.
    
    Args:
        screenshot_path (str): Path to the screenshot
        template_path (str): Path to the template image to find
        threshold (float): Detection threshold (0.0 to 1.0)
        
    Returns:
        tuple: (x, y, w, h) coordinates if found, None otherwise
    """
    # Load images
    screenshot = load_image(screenshot_path)
    template = load_image(template_path)
    
    # Get dimensions
    h, w = template.shape[:2]
    
    # Perform template matching
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    
    # Find positions where match exceeds threshold
    locations = np.where(result >= threshold)
    
    if len(locations[0]) == 0:
        return None
    
    # Get the best match
    _, _, _, max_loc = cv2.minMaxLoc(result)
    top_left = max_loc
    
    return (top_left[0], top_left[1], w, h)


def highlight_region(image_path, region, output_path=None, color=(0, 255, 0), thickness=2):
    """
    Highlight a region in an image.
    
    Args:
        image_path (str): Path to the image
        region (tuple): (x, y, w, h) coordinates of region to highlight
        output_path (str, optional): Path to save highlighted image
        color (tuple): BGR color for highlighting
        thickness (int): Line thickness
        
    Returns:
        ndarray: Image with highlighted region
    """
    # Load image
    image = load_image(image_path)
    
    # Draw rectangle around region
    x, y, w, h = region
    cv2.rectangle(image, (x, y), (x + w, y + h), color, thickness)
    
    if output_path is not None:
        cv2.imwrite(output_path, image)
    
    return image


def crop_image(image_path, region, output_path=None):
    """
    Crop an image to specified region.
    
    Args:
        image_path (str): Path to the image
        region (tuple): (x, y, w, h) coordinates to crop
        output_path (str, optional): Path to save cropped image
        
    Returns:
        ndarray: Cropped image
    """
    # Load image
    image = load_image(image_path)
    
    # Crop
    x, y, w, h = region
    cropped = image[y:y+h, x:x+w]
    
    if output_path is not None:
        cv2.imwrite(output_path, cropped)
    
    return cropped 