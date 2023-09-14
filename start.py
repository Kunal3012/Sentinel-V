from dotenv import load_dotenv
from datetime import datetime
import os
import cv2
import azure.cognitiveservices.speech as speech_sdk
import logging
import asyncio
import telegram
from knowledge_base import sentinel_responses

TOKEN = '5782912448:AAELn1wznXUtPmXOgQTEON8_niAuLDJrgm8'
CHAT_ID = -913473170

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

logger = logging.getLogger(__name__)

def main():
    
    try:
        global speech_config

        # Get Configuration Settings
        load_dotenv()
        cog_key = os.getenv('COG_SERVICE_KEY')
        cog_region = os.getenv('COG_SERVICE_REGION')
        # Configure speech service
        speech_config = speech_sdk.SpeechConfig(cog_key, cog_region)
        send_message_to_telegram("Face Detected")
        while True:
             print('Ready to use speech service in:', speech_config.region)
            # Get spoken input 
             InteractOut("Hello! Dear Visitor")
             send_message_to_telegram("Interaction Initiated")

             InteractOut(Sentinel_bot(TranscribeCommand()))        
    
      
    except Exception as ex:
        print(ex)
        

def detect_face_and_draw_box():
    
    send_message_to_telegram("sir! Sentinel is online!")
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()

        # Convert the frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Draw a rectangle around each detected face
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Call the InteractOut() function when a face is detected
            main()

        # Display the frame with the detected faces
        cv2.imshow('Face Detection', frame)

        # Exit the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close the window
    video_capture.release()
    cv2.destroyAllWindows()


def TranscribeCommand():
    command = ''

    # Configure speech recognition
    audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
    speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)
    print('Speak now...')

    # Process speech input
    speech = speech_recognizer.recognize_once_async().get()
    if speech.reason == speech_sdk.ResultReason.RecognizedSpeech:
         command = speech.text
         print(command)
    else:
        print(speech.reason)
        if speech.reason == speech_sdk.ResultReason.Canceled:
            cancellation = speech.cancellation_details
            print(cancellation.reason)
            print(cancellation.error_details)

    # Return the command
    return command
async def send_telegram_message(message):
    bot = telegram.Bot(token=TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=message)

def send_message_to_telegram(message):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_telegram_message(message))

def InteractOut(response_text):

    speech_config.speech_synthesis_voice_name = "en-GB-RyanNeural"
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)
    

    # Synthesize spoken output

    speak = speech_synthesizer.speak_text_async(response_text).get()
    if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
     print(speak.reason)

    # Print the response
    print(response_text)

def handle_visitor_registration(intent, entities):
    if intent == 'VisitorRegistration':
        if not entities:
            # No specific entity provided, general inquiry about the registration process
            return "To register as a visitor, please proceed to the main reception desk and provide your name, contact details, and the purpose of your visit. You may also be asked to present a valid identification document."
        else:
            for entity in entities:
                if entity['entity'] == 'Name':
                    name = TranscribeCommand("Please")
                elif entity['entity'] == 'ContactDetails':
                    contact_details = TranscribeCommand()
                elif entity['entity'] == 'Purpose':
                    purpose = TranscribeCommand()
            return "Thank you for providing your details. Your registration as a visitor is being processed."

    # Handle other intents or unrecognized inputs
    return "I'm sorry, I couldn't understand your request. Please provide more information."

def Sentinel_bot(input_text):
    # Convert input to lowercase for case-insensitive matching
    input_text = input_text.lower()
    
    # Check if the input exists as a key in the dictionary
    if input_text in sentinel_responses:
        return sentinel_responses[input_text]
    else:
        return sentinel_responses["default"]

if __name__ == "__main__":
    detect_face_and_draw_box()