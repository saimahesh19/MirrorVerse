import cv2
import numpy as np
# Path to the image
image_path = r"C:\Users\SAI MAHESH\Desktop\files\semisters\sem6\prj\iot\smart_mirror\pics\Mahesh.jpg"

# Load the face image
face_image = cv2.imread(image_path)

# Define the animation parameters
num_frames = 50
frame_height, frame_width = face_image.shape[:2]

# Create a VideoWriter object to save the animation as a video file
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('face_animation.avi', fourcc, 20.0, (frame_width, frame_height))

# Create an animation by moving the face around
for i in range(num_frames):
    # Create a blank frame
    frame = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)

    # Calculate the position of the face for this frame
    x_offset = int((i / num_frames) * (frame_width - face_image.shape[1]))
    y_offset = int((i / num_frames) * (frame_height - face_image.shape[0]))

    # Add the face to the frame at the calculated position
    frame[y_offset:y_offset+face_image.shape[0], x_offset:x_offset+face_image.shape[1]] = face_image

    # Write the frame to the output video
    out.write(frame)

    # Display the frame
    cv2.imshow('Face Animation', frame)
    cv2.waitKey(50)  # Adjust the delay between frames (in milliseconds)

# Release the VideoWriter object
out.release()
cv2.destroyAllWindows()
