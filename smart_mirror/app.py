# import os
# import cv2
# from flask import Flask, render_template, Response, request, jsonify
# from threading import Thread
# import face_recognition
# from deepface import DeepFace
# import spotipy
# from spotipy.oauth2 import SpotifyClientCredentials
# import webbrowser
# import time

# app = Flask(__name__)

# # Load known faces
# KNOWN_FACES_FOLDER = r"C:\Users\SAI MAHESH\Desktop\files\semisters\sem6\prj\iot\smart_mirror\pics"
# known_face_encodings = []
# known_face_names = []

# for filename in os.listdir(KNOWN_FACES_FOLDER):
#     if filename.endswith(".jpg") or filename.endswith(".png"):
#         image_path = os.path.join(KNOWN_FACES_FOLDER, filename)
#         known_image = face_recognition.load_image_file(image_path)
#         face_encoding = face_recognition.face_encodings(known_image)[0]
#         known_face_encodings.append(face_encoding)
#         known_face_names.append(os.path.splitext(filename)[0])

# # Set up Spotify credentials
# SPOTIFY_CLIENT_ID = 'a5828eeb0885407b9b98d4d2319ac661'
# SPOTIFY_CLIENT_SECRET = 'cfc6e731ebb148da9c44b3df6ea0fcc9'

# # Authenticate with Spotify
# client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID,
#                                                       client_secret=SPOTIFY_CLIENT_SECRET)
# sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# # Define mood and language mappings
# mood_map = {
#     'angry': {'telugu': 'Mass Beats', 'hindi': 'Aggressive Bhangra', 'tamil': 'Powerful Kuthu', 'malayalam': 'Intense Folk', 'english': 'Intense Rock'},
#     'disgust': {'telugu': 'Peaceful Carnatic', 'hindi': 'Serene Ghazals', 'tamil': 'Melancholic Film Songs', 'malayalam': 'Soulful Sufi', 'english': 'Calming Classical'},
#     'fear': {'telugu': 'Uplifting Devotional', 'hindi': 'Motivational Qawwali', 'tamil': 'Inspirational Bhajan', 'malayalam': 'Courageous Classical', 'english': 'Empowering Pop'},
#     'happy': {'telugu': 'Joyful Folk', 'hindi': 'Festive Bollywood', 'tamil': 'Celebratory Gaana', 'malayalam': 'Cheerful Mappila', 'english': 'Energetic Dance'},
#     'sad': {'telugu': 'Melancholic Melodies', 'hindi': 'Heartfelt Sufi', 'tamil': 'Emotional Classical', 'malayalam': 'Reflective Film Songs', 'english': 'Melancholic Ballads'},
#     'surprise': {'telugu': 'Dynamic Fusion', 'hindi': 'Eclectic Filmi', 'tamil': 'Unexpected Carnatic', 'malayalam': 'Vibrant Fusion', 'english': 'Dynamic Jazz'},
#     'neutral': {'telugu': 'Tranquil Instrumental', 'hindi': 'Soothing Raag', 'tamil': 'Relaxing Raga', 'malayalam': 'Peaceful Instrumental', 'english': 'Ambient Chill'}
# }

# # Global variable to store dominant emotion
# dominant_emotion = None

# def detect_emotion(frame):
#     global dominant_emotion
#     small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
#     rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
#     face_locations = face_recognition.face_locations(rgb_small_frame)

#     for top, right, bottom, left in face_locations:
#         face_frame = frame[top*4:bottom*4, left*4:right*4]
#         face_frame_rgb = cv2.cvtColor(face_frame, cv2.COLOR_BGR2RGB)

#         emotion_result_list = DeepFace.analyze(face_frame_rgb, actions=['emotion'], enforce_detection=False)

#         if emotion_result_list:
#             emotion_result = emotion_result_list[0]
#             dominant_emotion = max(emotion_result['emotion'].items(), key=lambda x: x[1])[0]

#             face_encoding = face_recognition.face_encodings(face_frame_rgb)
#             if face_encoding:
#                 matches = face_recognition.compare_faces(known_face_encodings, face_encoding[0])
#                 name = "Unknown"
#                 if True in matches:
#                     first_match_index = matches.index(True)
#                     name = known_face_names[first_match_index]

#                 return name, dominant_emotion

#     return None, None

# @app.route('/')
# def index():
#     return render_template('index.html')

# def generate_frames():
#     video_capture = cv2.VideoCapture(0)
#     video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Adjusting
#     video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 920)  # Adjusting frame height
    
#     start_time = time.time()
#     emotion_detected = False
#     detected_name = None
    
#     global dominant_emotion  # Ensure we're using the global variable
    
#     while True:
#         ret, frame = video_capture.read()
#         if not ret:
#             break

#         if time.time() - start_time >= 10 and not emotion_detected:
#             detected_name, dominant_emotion = detect_emotion(frame)
#             start_time = time.time()
#             emotion_detected = True

#         if emotion_detected and dominant_emotion:
#             if detected_name:
#                 cv2.putText(frame, f"{detected_name} seems {dominant_emotion}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
#             else:
#                 cv2.putText(frame, f"You seem {dominant_emotion}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
#         ret, jpeg = cv2.imencode('.jpg', frame)
#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

# @app.route('/video_feed')
# def video_feed():
#     return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/get_emotion')
# def get_emotion():
#     global dominant_emotion
#     return jsonify({'emotion': dominant_emotion})

# @app.route('/play_music', methods=['POST'])
# def play_music():
#     selected_language = request.form['language'].lower()
#     selected_mood = request.form['mood'].lower()

#     # Search for tracks based on mood and language
#     query = f"mood:{mood_map[selected_mood][selected_language]} language:{selected_language}"
#     results = sp.search(q=query, type='track', limit=10)

#     # Let the user choose a track to play
#     selected_idx = 0  # For simplicity, let's always play the first track from search results
#     selected_track_id = results['tracks']['items'][selected_idx]['id']

#     # Open the selected track in the Spotify app
#     webbrowser.open(f"spotify:track:{selected_track_id}")

#     return "Playing music..."

# if __name__ == '__main__':
#     app.run(debug=True)

import os
import cv2
from flask import Flask, render_template, Response, request, jsonify
from threading import Thread
import face_recognition
from deepface import DeepFace
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import webbrowser
import time

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
def index():
    return render_template('index.html')

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

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_emotion')
def get_emotion():
    global dominant_emotion
    return jsonify({'emotion': dominant_emotion})

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
if __name__ == '__main__':
    app.run(debug=True)