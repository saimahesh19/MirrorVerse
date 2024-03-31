from flask import Flask, render_template, Response
import cv2
import numpy as np

app = Flask(__name__)

# Function to apply edge mask
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

# Function to cartoonify the image
def cartoonify(img):
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

    # Cartoonify the image
    cartoon = cv2.bitwise_and(blurred, blurred, mask=edges)

    return cartoon

def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Cartoonify the frame
        cartoon_frame = cartoonify(frame)

        # Encode frame as JPEG image
        ret, buffer = cv2.imencode('.jpg', cv2.cvtColor(cartoon_frame, cv2.COLOR_BGR2RGB))
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('cartoon.html')

@app.route('/cartoon_feed')
def cartoon_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
