# Smart Mirror with Emotion Detection & Music Recommendation

A sophisticated IoT-based smart mirror application that detects user emotions through facial recognition and recommends personalized music based on the detected mood. Built with Flask backend and an interactive 3D frontend using Three.js.

## 👨‍💻 Developer

**MARPU SAI MAHESH**
- 📧 Email: chintusaimaheshmarpu@gmail.com
- 📱 Phone: +91 9502342564
- 📍 Location: Andhra Pradesh, India
- 💼 LinkedIn: [linkedin.com/in/marpumahesh](https://www.linkedin.com/in/marpumahesh/)
- 🐙 GitHub: [github.com/saimahesh19](https://github.com/saimahesh19)

## 🌟 Features

- **Real-time Face Recognition**: Identifies known users from a pre-loaded database of faces
- **Emotion Detection**: Uses DeepFace AI to analyze facial expressions and detect 7 emotions:
  - Happy
  - Sad
  - Angry
  - Fear
  - Surprise
  - Disgust
  - Neutral
- **Personalized Music Recommendations**: Integrates with Spotify API to suggest mood-appropriate music
- **Multi-language Support**: Music recommendations in 5 languages:
  - Telugu
  - Hindi
  - Tamil
  - Malayalam
  - English
- **Interactive 3D Interface**: Built with Three.js for an immersive user experience
- **Live Video Feed**: Real-time camera feed with emotion overlay

## 🛠️ Technology Stack

### Backend
- **Python 3.x**
- **Flask**: Web framework for API endpoints
- **OpenCV**: Computer vision and video processing
- **face_recognition**: Face detection and recognition
- **DeepFace**: Deep learning-based emotion analysis
- **Spotipy**: Spotify Web API wrapper

### Frontend
- **HTML5**: Structure and markup
- **CSS3**: Styling and animations
- **JavaScript (ES6+)**: Interactive functionality
- **Three.js**: 3D graphics and visualization

## 📋 Prerequisites

- Python 3.7 or higher
- Webcam/Camera device
- Spotify Developer Account (for API credentials)
- Known face images for recognition

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/saimahesh19/smart-mirror.git
cd smart-mirror
```

### 2. Install Python Dependencies

```bash
pip install flask opencv-python face-recognition deepface spotipy
```

### 3. Set Up Known Faces

Create a folder for known faces and add images:

```bash
mkdir pics
# Add .jpg or .png images of known people to the pics folder
# Name files as: /images/FaceRecognition.jpg
```

### 4. Configure Spotify API

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new application
3. Copy your Client ID and Client Secret
4. Update the credentials in the Flask app:

```python
SPOTIFY_CLIENT_ID = 'your_client_id_here'
SPOTIFY_CLIENT_SECRET = 'your_client_secret_here'
```

### 5. Update File Paths

Modify the `KNOWN_FACES_FOLDER` path in the Flask app to point to your pics folder:

```python
KNOWN_FACES_FOLDER = r"path/to/your/pics/folder"
```

## 🎮 Usage

### 1. Start the Flask Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

### 2. Access the Application

Open your web browser and navigate to:
```
http://localhost:5000
```

### 3. Using the Smart Mirror

1. **Face Detection**: Position yourself in front of the camera
2. **Emotion Analysis**: The system analyzes your emotion every 10 seconds
3. **View Results**: Your name (if recognized) and detected emotion appear on screen
4. **Music Recommendation**: Select your preferred language and click to play mood-appropriate music
5. **Spotify Integration**: Music opens automatically in your Spotify app

## 📁 Project Structure

```
smart-mirror/
│
├── app.py                 # Flask backend application
├── templates/
│   └── index.html        # Frontend HTML with Three.js
├── static/
│   ├── css/
│   │   └── style.css     # Styling
│   └── js/
│       └── main.js       # JavaScript logic
├── pics/                 # Known faces database
│   ├── /images/Person.jpg
│   └── /images/Person.jpg
└── README.md            # Project documentation
```

## 🎵 Mood-Music Mapping

The application maps emotions to music genres across different languages:

| Emotion | Telugu | Hindi | Tamil | Malayalam | English |
|---------|--------|-------|-------|-----------|---------|
| Happy | Joyful Folk | Festive Bollywood | Celebratory Gaana | Cheerful Mappila | Energetic Dance |
| Sad | Melancholic Melodies | Heartfelt Sufi | Emotional Classical | Reflective Film Songs | Melancholic Ballads |
| Angry | Mass Beats | Aggressive Bhangra | Powerful Kuthu | Intense Folk | Intense Rock |
| Fear | Uplifting Devotional | Motivational Qawwali | Inspirational Bhajan | Courageous Classical | Empowering Pop |
| Surprise | Dynamic Fusion | Eclectic Filmi | Unexpected Carnatic | Vibrant Fusion | Dynamic Jazz |
| Disgust | Peaceful Carnatic | Serene Ghazals | Melancholic Film Songs | Soulful Sufi | Calming Classical |
| Neutral | Tranquil Instrumental | Soothing Raag | Relaxing Raga | Peaceful Instrumental | Ambient Chill |

## 🔧 API Endpoints

### GET `/`
Returns the main application interface

### GET `/video_feed`
Streams live video feed with emotion detection overlay

### GET `/get_emotion`
Returns the currently detected emotion as JSON
```json
{
  "emotion": "happy"
}
```

### POST `/play_music`
Plays music based on detected emotion and selected language

**Request Body:**
```json
{
  "language": "english"
}
```

## 🐛 Troubleshooting

### Camera Not Working
- Ensure your webcam is properly connected
- Check camera permissions in your OS settings
- Try changing the camera index in `cv2.VideoCapture(0)` to `1` or `2`

### Face Recognition Issues
- Ensure images in the pics folder are clear and well-lit
- Use frontal face photos for best results
- Check that image filenames don't contain special characters

### Spotify Not Opening
- Ensure Spotify desktop app is installed
- Check that your API credentials are correct
- Verify your internet connection

### DeepFace Installation Issues
```bash
pip install --upgrade deepface
pip install tf-keras
```

## 🔐 Security Notes

- **Never commit API credentials** to version control
- Use environment variables for sensitive data:
  ```python
  import os
  SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
  SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
  ```
- Implement user authentication for production deployment
- Use HTTPS in production environments

## 🚀 Future Enhancements

- [ ] Add user profile management
- [ ] Implement emotion history tracking
- [ ] Add more music streaming service integrations
- [ ] Create mobile application version
- [ ] Add voice control features
- [ ] Implement weather and news widgets
- [ ] Add calendar and reminder features
- [ ] Support for multiple simultaneous users

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/saimahesh19/smart-mirror/issues).

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Contact

**MARPU SAI MAHESH**

- Email: chintusaimaheshmarpu@gmail.com
- LinkedIn: [linkedin.com/in/marpumahesh](https://www.linkedin.com/in/marpumahesh/)
- GitHub: [github.com/saimahesh19](https://github.com/saimahesh19)
- Phone: +91 9502342564

---

⭐ If you found this project helpful, please consider giving it a star!

**Made with ❤️ by Marpu Sai Mahesh**
