import cv2
import mysql.connector
import numpy as np

# Connect to MySQL database
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='qwerty_123',
    database='mirrorverse'
)
cursor = db.cursor()

# Load pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Capture video from webcam
cap = cv2.VideoCapture(0)

# Function to prompt user to input their name
def get_user_name():
    name = input("Enter your name: ")
    return name

# Function to store face data and name in database
def store_face_in_database(name, face_data):
    query = "INSERT INTO faces (name, face_data) VALUES (%s, %s)"
    cursor.execute(query, (name, face_data))
    db.commit()

# Function to compare detected face with stored faces
def recognize_face(face_roi):
    query = "SELECT name, face_data FROM faces"
    cursor.execute(query)
    results = cursor.fetchall()
    
    for name, stored_face_data in results:
        # Convert stored face data to numpy array
        nparr = np.frombuffer(stored_face_data, np.uint8)
        # Decode numpy array to image
        stored_face = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
        
        # Compare detected face with stored faces
        # Use any suitable method for face comparison
        # Here, we're using simple pixel-wise comparison
        if np.array_equal(face_roi, stored_face):
            return name
    
    return None

# Main loop
while True:
    # Read frame from camera
    ret, frame = cap.read()
    
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # Iterate over detected faces
    for (x, y, w, h) in faces:
        # Draw rectangle around detected face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # Extract face region
        face_roi = gray[y:y+h, x:x+w]
        
        # Check if user is new or existing
        new_user = input("Are you a new user? (yes/no): ").lower() == 'yes'
        
        if new_user:
            # New user: prompt to input name and store face data in database
            user_name = get_user_name()
            store_face_in_database(user_name, cv2.imencode('.jpg', face_roi)[1].tostring())
        else:
            # Existing user: try to recognize the detected face
            name = recognize_face(face_roi)
            if name is not None:
                # Display user's name if recognized
                cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
    
    # Display frame
    cv2.imshow('Face Recognition', frame)
    
    # Break loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close all windows
cap.release()
cv2.destroyAllWindows()
