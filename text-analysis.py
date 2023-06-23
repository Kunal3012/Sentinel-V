from dotenv import load_dotenv
import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

def main():
    try:
        # Get Configuration Settings
        load_dotenv()
        cog_endpoint = os.getenv('COG_SERVICE_ENDPOINT')
        cog_key = os.getenv('COG_SERVICE_KEY')

        # Create client using endpoint and key
        credential = AzureKeyCredential(cog_key)
        cog_client = TextAnalyticsClient(endpoint=cog_endpoint, credential=credential)

        # Analyze each text file in the reviews folder
        reviews_folder = r'C:\Users\KUNALYADAV\Desktop\Sentinel I\review_statements'
        for file_name in os.listdir(reviews_folder):
            # Read the file contents
            print('\n-------------\n' + file_name)
            text = open(os.path.join(reviews_folder, file_name), encoding='utf8').read()
            print('\n' + text)

            # Get language
            detectedLanguage = cog_client.detect_language(documents=[text])[0]
            print('\nLanguage: {}'.format(detectedLanguage.primary_language.name))

            # Get sentiment
            sentimentAnalysis = cog_client.analyze_sentiment(documents=[text])[0]
            print("\nSentiment: {}".format(sentimentAnalysis.sentiment))

            # Get key phrases
            phrases = cog_client.extract_key_phrases(documents=[text])[0].key_phrases
            if len(phrases) > 0:
                print("\nKey Phrases:")
                for phrase in phrases:
                    print('\t{}'.format(phrase))


            # Get entities
            entities = cog_client.recognize_entities(documents=[text])[0].entities
            if len(entities) > 0:
             print("\nEntities")
             for entity in entities:
               print('\t{} ({})'.format(entity.text, entity.category))

            # Get entities
            entities = cog_client.recognize_entities(documents=[text])[0].entities
            if len(entities) > 0:
               print("\nEntities")
               for entity in entities:
                print('\t{} ({})'.format(entity.text, entity.category))

    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()