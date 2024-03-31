# import mysql.connector
# import cv2
# import numpy as np
# r"C:\Users\SAI MAHESH\Desktop\files\personal\PASSPORT PHOTO.jpg"
# # Connect to MySQL database
# mydb = mysql.connector.connect(
#     host='localhost',
#     user='root',
#     password='qwerty_123',
#     database='mirrorverse'
# )import mysql.connector


import os
import face_recognition
import cv2

def load_known_faces(folder_path):
    known_face_encodings = []
    known_face_names = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            # Load the image
            image_path = os.path.join(folder_path, filename)
            known_image = face_recognition.load_image_file(image_path)

            # Encode the face
            face_encoding = face_recognition.face_encodings(known_image)[0]

            # Extract the name from the filename (remove extension)
            name = os.path.splitext(filename)[0]

            # Append encoding and name to lists
            known_face_encodings.append(face_encoding)
            known_face_names.append(name)

    return known_face_encodings, known_face_names

def recognize_faces(known_face_encodings, known_face_names):
    # Open the default camera
    video_capture = cv2.VideoCapture(0)

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        # Resize frame for faster face recognition
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (OpenCV) to RGB color (face_recognition)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Find all face locations in the frame
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        # Compare faces in the camera feed with the known faces
        for face_encoding in face_encodings:
            # Compare the face with the known faces
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # Check if any known face matches
            if True in matches:
                # Find the index of the first match
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            # Display the name of the person
            cv2.putText(frame, name, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

        # Display the resulting frame
        cv2.imshow('Video', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close windows
    video_capture.release()
    cv2.destroyAllWindows()

# Path to the folder containing images
folder_path = r"C:\Users\SAI MAHESH\Desktop\files\semisters\sem6\prj\iot\smart_mirror\pics"

# Load the known face encodings and names
known_face_encodings, known_face_names = load_known_faces(folder_path)

# Call the function to recognize faces from the camera feed
recognize_faces(known_face_encodings, known_face_names)
