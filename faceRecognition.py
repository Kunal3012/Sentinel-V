import os
import face_recognition
import cv2
import pickle

# Function to encode faces in a folder and create a record of names and encodings
def encode_faces(folder_path):
    # Initialize empty lists for names and encodings
    known_names = []
    known_encodings = []

    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)

        # Check if file is an image
        if not os.path.isfile(filepath) or not filename.endswith((".jpg", ".jpeg", ".png")):
            continue

        # Load image
        img = face_recognition.load_image_file(filepath)

        # Extract name from filename
        name = os.path.splitext(filename)[0]

        # Get face encoding
        encoding = face_recognition.face_encodings(img)[0]

        # Append name and encoding to lists
        known_names.append(name)
        known_encodings.append(encoding)

    # Save names and encodings to file
    with open("encodings.pickle", "wb") as f:
        pickle.dump({"names": known_names, "encodings": known_encodings}, f)
    return known_names, known_encodings

# Function to detect face from webcam and compare to known encodings
def detect_face():
    # Load encodings from file
    with open("encodings.pickle", "rb") as f:
        data = pickle.load(f)
    known_names = data["names"]
    known_encodings = data["encodings"]

    # Initialize webcam
    cap = cv2.VideoCapture(0)

    while True:
        # Capture frame from webcam
        ret, frame = cap.read()

        # Convert frame to RGB format
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect faces in frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Loop through detected faces
        for face_encoding, face_location in zip(face_encodings, face_locations):
            # Compare face encoding to known encodings
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            name = "Unknown"

            # Check if there is a match
            if True in matches:
                match_index = matches.index(True)
                name = known_names[match_index]

            # Draw rectangle around face and label with name
            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

        # Display the resulting image
        cv2.imshow("Face Detection", frame)

        # Break loop if 'q' key is pressed
        if cv2.waitKey(1) == ord("q"):
            break

    # Release webcam and close windows
    cap.release()
    cv2.destroyAllWindows()

# Ask user for folder path and encode faces
folder_path = r"C:\Users\KUNALYADAV\OneDrive - Amity University\Desktop\Sentinel I\Faces"
known_names, known_encodings = encode_faces(folder_path)


# Detect faces from webcam and compare to known encodings
detect_face()