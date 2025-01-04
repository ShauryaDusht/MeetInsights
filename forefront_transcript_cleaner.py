import os
import requests
import time
from dotenv import load_dotenv


class TranscriptCleaner:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("FOREFRONT_API_KEY")
        self.url = "https://api.forefront.ai/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        self.max_retries = 3
        
        self.system_prompt = f'''You are a transcript cleaning assistant. Your task is to:
            1. Remove repetitive phrases and stutters
            2. Combine related segments into coherent paragraphs
            3. Maintain the original meaning and key information
            4. Keep important timestamps at the start of each major segment
            5. Format the output in clear, readable paragraphs
            6. Maintain technical terms and specific instructions mentioned
            7. Change certain things like file dot thing to file.thing
        '''

    def make_api_request(self, transcript_text):
        """Make API request with retry logic"""
        payload = {
            "model": "mistralai/Mistral-7B-v0.1",
            "messages": [
                {
                    "role": "system",
                    "content": self.system_prompt
                },
                {
                    "role": "user",
                    "content": transcript_text
                }
            ],
            "max_tokens": 200,
            "temperature": 0.1,
        }

        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    self.url,
                    json=payload,
                    headers=self.headers,
                    timeout=300
                )
                print(f"[STATUS]: {response.status_code}")

                if response.status_code == 200:
                    result = response.json()
                    content = result['choices'][0]['message']['content']
                    return content.replace('<|im_end|>', '').replace('<|im_start|>', '').strip()
                else:
                    print(f"[RESPONSE]: {response.text}")
                    if attempt < self.max_retries - 1:
                        time.sleep(2 ** attempt)
                        continue
                    raise Exception(f"API request failed after {self.max_retries} attempts")

            except Exception as e:
                print(f"[ERROR]: {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise

    def clean_and_save_transcript(self, transcript_path):
        """Clean the transcript using Forefront AI and save it to a new file"""
        try:
            # Read the transcript
            with open(transcript_path, 'r', encoding='utf-8') as file:
                transcript_text = file.read()

            # Get cleaned text from API
            cleaned_text = self.make_api_request(transcript_text)

            # Create cleaned transcripts directory
            directory = os.path.dirname(transcript_path)
            cleaned_dir = os.path.join(directory, "cleaned_transcripts")
            os.makedirs(cleaned_dir, exist_ok=True)

            # Save cleaned transcript
            original_filename = os.path.basename(transcript_path)
            new_filename = "cleaned_" + original_filename
            new_path = os.path.join(cleaned_dir, new_filename)

            with open(new_path, 'w', encoding='utf-8') as file:
                file.write(cleaned_text)

            print(f"Successfully cleaned transcript and saved to: {new_path}")
            return new_path

        except Exception as e:
            print(f"Error cleaning transcript: {str(e)}")
            raise

    @staticmethod
    def get_latest_transcript():
        """Find the most recent transcript file"""
        transcript_dir = os.path.join(os.getcwd(), "transcripts")
        transcript_files = [f for f in os.listdir(transcript_dir) 
                          if f.startswith("meet_transcript_")]
        if not transcript_files:
            raise Exception("No transcript files found")
        
        latest_file = max(transcript_files, 
                         key=lambda x: os.path.getctime(os.path.join(transcript_dir, x)))
        return os.path.join(transcript_dir, latest_file)