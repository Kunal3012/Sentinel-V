import os
import cv2
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials

# Replace with your endpoint and subscription key
load_dotenv()
ENDPOINT =  os.getenv('COG_SERVICE_ENDPOINT')
SUBSCRIPTION_KEY = os.getenv('COG_SERVICE_KEY')

# Initialize the FaceClient
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(SUBSCRIPTION_KEY))

# Function to detect and recognize faces from a folder
def detect_and_recognize_faces_from_folder(folder_path):
    image_paths = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if filename.endswith((".jpg", ".jpeg", ".png"))]

    for image_path in image_paths:
        image = open(image_path, "r+b")

        # Detect faces in the image
        detected_faces = face_client.face.detect_with_stream(image, detection_model="detection_03")

        if not detected_faces:
            print(f"No faces detected in {image_path}")
            continue

        for face in detected_faces:
            # Recognize face if it's detected
            recognized_faces = face_client.face.identify(
                [face.face_id],
                large_person_group_id="your_large_person_group_id"  # Replace with your group ID
            )

            if recognized_faces:
                candidate = recognized_faces[0].candidates[0]
                person_id = candidate.person_id

                # Get person information using person_id
                person = face_client.large_person_group_person.get("your_large_person_group_id", person_id)

                # Print the recognized person's name
                print(f"Recognized {person.name} in {image_path}")

# Call the function with the path to the folder containing images
folder_path = r"C:\Users\KUNALYADAV\OneDrive - Amity University\Desktop\Sentinel I\Faces"
detect_and_recognize_faces_from_folder(folder_path)
