
import numpy as np
import cv2

# Function to read the image file
def read_file(filename):
    img = cv2.imread(filename)
    return img

# Edge mask function to transform the image into grayscale and reduce noise
def edge_mask(img, line_size, blur_value):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.medianBlur(gray, 7)
    edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, line_size, blur_value)
    return edges

# Function to reduce the number of colors in the photo
def color_quantization(img, k):
    data = np.float32(img).reshape((-1, 3))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
    ret, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    result = center[label.flatten()]
    result = result.reshape(img.shape)
    return result

# Read the image
filename = r"C:\Users\SAI MAHESH\Desktop\files\personal\bdaypic\IMG-20240219-WA0015.jpg"
img = read_file(filename)

# Store the original dimensions of the image
original_height, original_width = img.shape[:2]

# Generate edge mask
line_size = 9
blur_value = 9
edges = edge_mask(img, line_size, blur_value)

# Color quantization
total_color = 9
img = color_quantization(img, total_color)

# Bilateral filter to reduce noise
d = 9  # Diameter of each pixel neighborhood
sigmaColor = 75  # A larger value means larger areas of semi-equal color
sigmaSpace = 75  # A larger value means farther pixels will influence each other
blurred = cv2.bilateralFilter(img, d, sigmaColor, sigmaSpace)

# Resize the edges mask to match the original image dimensions
edges = cv2.resize(edges, (original_width, original_height))

# Cartoonify the image
cartoon = cv2.bitwise_and(blurred, blurred, mask=edges)

# Enhance the nighttime effect by adjusting color and contrast
# You can experiment with different values here
cartoon = cv2.convertScaleAbs(cartoon, alpha=0.8, beta=50)

# Create a resizable window and display the cartoonified image
cv2.namedWindow("Cartoonified Image", cv2.WINDOW_NORMAL)
cv2.imshow("Cartoonified Image", cartoon)
cv2.waitKey(0)
cv2.destroyAllWindows()
