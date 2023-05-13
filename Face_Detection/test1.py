import cv2
import os

# Load model
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

# Load video
video_capture = cv2.VideoCapture('face.mp4')

# Get fps
fps = int(video_capture.get(cv2.CAP_PROP_FPS))

# Define codec
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

# Get size of the video
frame_width = int(video_capture.get(3))
frame_height = int(video_capture.get(4))

# Create a output video
output_video = cv2.VideoWriter('output_video.mp4', fourcc, fps, (frame_width, frame_height))

# Define directory
output_dir = 'detected_faces'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# face count and image count
face_count = 0
img_count = 0


# Loop frame of the video
while True:
    # Read frame
    ret, frame = video_capture.read()

    if not ret:
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray,
                                          scaleFactor=1.1,
                                          minNeighbors=5,
                                          minSize=(30, 30),
                                          flags=cv2.CASCADE_SCALE_IMAGE)

    # Count faces
    num_faces = len(faces)


    # If num of faces changes, save detected face
    if num_faces != face_count:
        face_count = num_faces
        for i, (x, y, w, h) in enumerate(faces):
            roi_color = frame[y: y + h, x: x + w]

            # Save
            img_count += 1
            img_path = os.path.join(output_dir, f'detected_face_{img_count}.jpg')
            cv2.imwrite(img_path, roi_color)

    # Loop detected face
    for (x, y, w, h) in faces:
        # Draw bounding box
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 1)

        # Crop the region
        roi_gray = gray[y: y + h, x: x + w]
        roi_color = frame[y: y + h, x: x + w]

        # Detect eyes
        eyes = eye_cascade.detectMultiScale(roi_gray)

        # Draw a rectangle around each detected eye
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 1)

        # Save first detected face
        if faces.tolist().index([x, y, w, h]) == 0:
            cv2.imwrite('first_face.jpg', roi_color)

    # Add the number of faces detected to frame
    cv2.putText(frame, f'Faces: {num_faces}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Display frame
    cv2.imshow('Video', frame)

    # Write output video
    output_video.write(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# show output
video_capture.release()
output_video.release()
cv2.destroyAllWindows()
