import os
import cv2
from flask import Flask, render_template, Response, request, jsonify, redirect, url_for
from threading import Thread
import face_recognition
from deepface import DeepFace
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import webbrowser
import time
import mysql.connector
import numpy as np
import requests

app = Flask(__name__)

# Load known faces
KNOWN_FACES_FOLDER = r"C:\Users\SAI MAHESH\Desktop\files\semisters\sem6\prj\iot\smart_mirror\pics"
known_face_encodings = []
known_face_names = []

for filename in os.listdir(KNOWN_FACES_FOLDER):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image_path = os.path.join(KNOWN_FACES_FOLDER, filename)
        known_image = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(known_image)[0]
        known_face_encodings.append(face_encoding)
        known_face_names.append(os.path.splitext(filename)[0])

# Connect to MySQL database
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='qwerty_123',
    database='mirrorverse'
)

# Set up Spotify credentials
SPOTIFY_CLIENT_ID = 'a5828eeb0885407b9b98d4d2319ac661'
SPOTIFY_CLIENT_SECRET = 'cfc6e731ebb148da9c44b3df6ea0fcc9'

# Authenticate with Spotify
client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID,
                                                      client_secret=SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Define mood and language mappings
mood_map = {
    'angry': {'telugu': 'Mass Beats', 'hindi': 'Aggressive Bhangra', 'tamil': 'Powerful Kuthu', 'malayalam': 'Intense Folk', 'english': 'Intense Rock'},
    'disgust': {'telugu': 'Peaceful Carnatic', 'hindi': 'Serene Ghazals', 'tamil': 'Melancholic Film Songs', 'malayalam': 'Soulful Sufi', 'english': 'Calming Classical'},
    'fear': {'telugu': 'Uplifting Devotional', 'hindi': 'Motivational Qawwali', 'tamil': 'Inspirational Bhajan', 'malayalam': 'Courageous Classical', 'english': 'Empowering Pop'},
    'happy': {'telugu': 'Joyful Folk', 'hindi': 'Festive Bollywood', 'tamil': 'Celebratory Gaana', 'malayalam': 'Cheerful Mappila', 'english': 'Energetic Dance'},
    'sad': {'telugu': 'Melancholic Melodies', 'hindi': 'Heartfelt Sufi', 'tamil': 'Emotional Classical', 'malayalam': 'Reflective Film Songs', 'english': 'Melancholic Ballads'},
    'surprise': {'telugu': 'Dynamic Fusion', 'hindi': 'Eclectic Filmi', 'tamil': 'Unexpected Carnatic', 'malayalam': 'Vibrant Fusion', 'english': 'Dynamic Jazz'},
    'neutral': {'telugu': 'Tranquil Instrumental', 'hindi': 'Soothing Raag', 'tamil': 'Relaxing Raga', 'malayalam': 'Peaceful Instrumental', 'english': 'Ambient Chill'}
}

# Global variable to store dominant emotion
dominant_emotion = None

# Function to authenticate user
def authenticate(username, password):
    cursor = db.cursor()
    query = "SELECT * FROM authenticate WHERE username = %s AND password = %s"
    cursor.execute(query, (username, password))
    result = cursor.fetchone()
    cursor.close()
    return result is not None

# Function to get weather data
def get_weather_data(latitude, longitude, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch weather data.")
        return None

# Function to detect emotion
def detect_emotion(frame):
    global dominant_emotion
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_small_frame)

    for top, right, bottom, left in face_locations:
        face_frame = frame[top*4:bottom*4, left*4:right*4]
        face_frame_rgb = cv2.cvtColor(face_frame, cv2.COLOR_BGR2RGB)

        emotion_result_list = DeepFace.analyze(face_frame_rgb, actions=['emotion'], enforce_detection=False)

        if emotion_result_list:
            emotion_result = emotion_result_list[0]
            dominant_emotion = max(emotion_result['emotion'].items(), key=lambda x: x[1])[0]

            face_encoding = face_recognition.face_encodings(face_frame_rgb)
            if face_encoding:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding[0])
                name = "Unknown"
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                return name, dominant_emotion

    return None, None

@app.route('/')
def login():
    return render_template('authentication.html')

@app.route('/authenticate', methods=['POST'])
def authentication():
    username = request.form['username']
    password = request.form['password']
    if authenticate(username, password):
        return redirect(url_for('choose_option'))
    else:
        return "Authentication failed. Invalid username or password."

@app.route('/choose_option')
def choose_option():
    return render_template('index1.html')

@app.route('/option_selected', methods=['POST'])
def option_selected():
    option = request.form['option']
    if option == 'smart_mirror':
        return redirect(url_for('smart_mirror'))
    elif option == 'cartoon_mirror':
        return redirect(url_for('cartoon_mirror'))
    else:
        return "Invalid option selected."

@app.route('/smart_mirror')
def smart_mirror():
    # Weather details
    latitude = 13.0836
    longitude = 80.275
    api_key = 'c9a572a88fa13f639d8819851d9ca37f'
    weather_data = get_weather_data(latitude, longitude, api_key)
    return render_template('index.html', weather_data=weather_data)

@app.route('/video_feed')
def video_feed():
    def generate_frames():
        video_capture = cv2.VideoCapture(0)
        video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Adjusting
        video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 920)  # Adjusting frame height
        
        start_time = time.time()
        emotion_detected = False
        detected_name = None
        
        global dominant_emotion  # Ensure we're using the global variable
        
        while True:
            ret, frame = video_capture.read()
            if not ret:
                break

            if time.time() - start_time >= 10 and not emotion_detected:
                detected_name, dominant_emotion = detect_emotion(frame)
                start_time = time.time()
                emotion_detected = True

            if emotion_detected and dominant_emotion:
                if detected_name:
                    cv2.putText(frame, f"{detected_name} seems {dominant_emotion}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                else:
                    cv2.putText(frame, f"You seem {dominant_emotion}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            ret, jpeg = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')


        video_capture.release()
        cv2.destroyAllWindows()

    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/play_music', methods=['POST'])
def play_music():
    request_data = request.get_json()  # Get JSON data from request body
    selected_language = request_data.get('language', '').lower()

    # Use the dominant emotion as the selected mood
    selected_mood = dominant_emotion

    # Search for tracks based on mood and language
    query = f"mood:{mood_map[selected_mood][selected_language]} language:{selected_language}"
    results = sp.search(q=query, type='track', limit=10)

    # Let the user choose a track to play
    selected_idx = 0  # For simplicity, let's always play the first track from search results
    selected_track_id = results['tracks']['items'][selected_idx]['id']

    # Open the selected track in the Spotify app
    webbrowser.open(f"spotify:track:{selected_track_id}")

    return "Playing music..."



@app.route('/cartoon_mirror')
def cartoon_mirror():
    # Weather details
    latitude = 13.0836
    longitude = 80.275
    api_key = 'c9a572a88fa13f639d8819851d9ca37f'
    weather_data = get_weather_data(latitude, longitude, api_key)
    return render_template('cartoon.html', weather_data=weather_data)

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

def generate_cartoon_frames():
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

    cap.release()
    cv2.destroyAllWindows()

@app.route('/cartoon_feed')
def cartoon_feed():
    return Response(generate_cartoon_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
