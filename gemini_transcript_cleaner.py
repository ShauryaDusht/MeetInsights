import os
import time
import google.generativeai as genai
import google.generativeai.types.generation_types
from pathlib import Path
from dotenv import load_dotenv

class TranscriptCleaner:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=self.api_key)
        
        # Configure the model
        generation_config = {
            "temperature": 0.1,
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 2048,
        }
        
        # Initialize the model
        self.model = genai.GenerativeModel(
            model_name="gemini-pro",
            generation_config=generation_config
        )
        
        self.system_prompt = f'''You are a transcript cleaning assistant. Your task is to:
            1. Remove repetitive phrases and stutters
            2. Combine related segments into coherent paragraphs
            3. Maintain the original meaning and key information
            4. Keep important timestamps at the start of each major segment
            5. Format the output in clear, readable paragraphs
            6. Maintain technical terms and specific instructions mentioned
            7. Change certain things like file dot thing to file.thing
            Process the following transcript according to these guidelines.
        '''
        
        self.max_retries = 3
        
    def make_api_request(self, transcript_text):
        """Make API request with retry logic"""
        prompt = f"{self.system_prompt}\n\n{transcript_text}"
        
        for attempt in range(self.max_retries):
            try:
                response = self.model.generate_content(prompt)
                
                if response.text:
                    return response.text.strip()
                else:
                    print(f"[ERROR]: Empty response received")
                    if attempt < self.max_retries - 1:
                        time.sleep(2 ** attempt)
                        continue
                    raise Exception("Empty response from API")
                    
            except Exception as e:
                print(f"[ERROR]: {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise

    def clean_and_save_transcript(self, transcript_path):
        """Clean the transcript using Gemini API and save it to a new file"""
        try:
            # Read the transcript
            transcript_path = Path(transcript_path)
            with open(transcript_path, 'r', encoding='utf-8') as file:
                transcript_text = file.read()

            # Get cleaned text from API
            cleaned_text = self.make_api_request(transcript_text)

            # Create cleaned transcripts directory
            cleaned_dir = transcript_path.parent / "cleaned_transcripts"
            cleaned_dir.mkdir(exist_ok=True)

            # Save cleaned transcript
            new_filename = f"cleaned_{transcript_path.name}"
            new_path = cleaned_dir / new_filename

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
        transcript_dir = Path.cwd() / "transcripts"
        transcript_files = list(transcript_dir.glob("meet_transcript_*"))
        
        if not transcript_files:
            raise Exception("No transcript files found")
        
        latest_file = max(transcript_files, key=lambda x: x.stat())
        return latest_file
