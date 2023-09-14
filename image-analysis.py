from dotenv import load_dotenv
import os
import sys
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

# Load configuration settings from environment variables
load_dotenv()
cog_endpoint = os.getenv('COG_SERVICE_ENDPOINT')
cog_key = os.getenv('COG_SERVICE_KEY')

def main():
    try:
        # Get image file path
        image_file = r'C:\Users\KUNALYADAV\OneDrive - Amity University\Desktop\AI-102-AIEngineer\15-computer-vision\Python\image-analysis\images\street.jpg'
        if len(sys.argv) > 1:
            image_file = sys.argv[1]

        # Authenticate Computer Vision client
        credential = CognitiveServicesCredentials(cog_key)
        cv_client = ComputerVisionClient(cog_endpoint, credential)

        # Analyze image and print results as JSON
        analysis_result = AnalyzeImage(cv_client, image_file)
        print(analysis_result)

    except Exception as ex:
        print(ex)

def AnalyzeImage(cv_client, image_file):
    print('Analyzing', image_file)

    # Specify features to be retrieved
    features = [
        VisualFeatureTypes.description,
        VisualFeatureTypes.tags,
        VisualFeatureTypes.categories,
        VisualFeatureTypes.brands,
        VisualFeatureTypes.objects,
        VisualFeatureTypes.adult
    ]

    # Get image analysis
    with open(image_file, mode="rb") as image_data:
        analysis = cv_client.analyze_image_in_stream(image_data, features)

    # Prepare the analysis results in a structured dictionary
    result = {
        "description": [{"text": caption.text, "confidence": caption.confidence} for caption in analysis.description.captions],
        "tags": [{"name": tag.name, "confidence": tag.confidence} for tag in analysis.tags],
        "categories": [{"name": category.name, "score": category.score} for category in analysis.categories],
        "brands": [{"name": brand.name, "confidence": brand.confidence} for brand in analysis.brands],
        "objects": [{"name": detected_object.object_property, "confidence": detected_object.confidence} for detected_object in analysis.objects],
        "adult": {
            "is_adult_content": analysis.adult.is_adult_content,
            "is_racy_content": analysis.adult.is_racy_content,
            "is_gory_content": analysis.adult.is_gory_content
        }
    }

    return result

if __name__ == "__main__":
    main()