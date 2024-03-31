# import cv2
# import numpy as np
# from flask import request, jsonify
# from deepface import DeepFace

# import cv2
# import numpy as np
# from deepface import DeepFace

# def analyze_emotion(image_path):
#     # Load the image using OpenCV
#     img = cv2.imread(image_path)

#     # Analyze emotion using DeepFace
#     result = DeepFace.analyze(img, actions=['emotion'])

#     return result

# # Path to the image
# image_path = r"C:\Users\SAI MAHESH\Desktop\files\semisters\sem6\prj\iot\smart_mirror\pics\Mahesh.jpg"

# # Analyze emotion of the image
# emotion_result = analyze_emotion(image_path)

# # Print the result
# print(emotion_result)



# import cv2
# import numpy as np
# from deepface import DeepFace

# def analyze_emotion(image_path):
#     # Load the image using OpenCV
#     img = cv2.imread(image_path)

#     # Analyze emotion using DeepFace
#     result = DeepFace.analyze(img, actions=['emotion'])

#     # Extract the emotion information from the result
#     emotion_result = result[0]  # Get the dictionary from the list
#     dominant_emotion = max(emotion_result['emotion'].items(), key=lambda x: x[1])

#     return emotion_result, dominant_emotion

# # Path to the image
# image_path = r"C:\Users\SAI MAHESH\Desktop\files\semisters\sem6\prj\iot\smart_mirror\pics\Mahesh.jpg"

# # Analyze emotion of the image
# emotion_result, dominant_emotion = analyze_emotion(image_path)

# # Print the dominant emotion
# print("Dominant emotion:", dominant_emotion)


import cv2
import numpy as np
from deepface import DeepFace
import matplotlib.pyplot as plt

def analyze_emotion(image_path):
    # Load the image using OpenCV
    img = cv2.imread(image_path)

    # Analyze emotion using DeepFace
    result = DeepFace.analyze(img, actions=['emotion'])

    # Extract the emotion information from the result
    emotion_result = result[0]  # Get the dictionary from the list
    dominant_emotion = max(emotion_result['emotion'].items(), key=lambda x: x[1])

    return emotion_result, dominant_emotion

# Path to the image
image_path = r"C:\Users\SAI MAHESH\Desktop\files\semisters\sem6\prj\iot\smart_mirror\pics\Mahesh.jpg"

# Analyze emotion of the image
emotion_result, dominant_emotion = analyze_emotion(image_path)

# Display the image with emotion
img = cv2.imread(image_path)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Overlay the dominant emotion on the image
cv2.putText(img_rgb, f"Dominant Emotion: {dominant_emotion[0]}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

# Display the image using Matplotlib
plt.figure(figsize=(8, 6))
plt.imshow(img_rgb)
plt.axis('off')
plt.show()
