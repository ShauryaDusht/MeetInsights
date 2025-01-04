import os
import openai
from dotenv import load_dotenv

class TranscriptCleaner:
    def __init__(self):
        load_dotenv()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        openai.api_key = self.openai_api_key
        
        self.prompt = f'''
            You are a transcript cleaning assistant. Your task is to:
            1. Remove repetitive phrases and stutters
            2. Combine related segments into coherent paragraphs
            3. Maintain the original meaning and key information
            4. Keep important timestamps at the start of each major segment
            5. Format the output in clear, readable paragraphs
            6. Maintain technical terms and specific instructions mentioned
            7. Change certain things like file dot thing to file.thing
        '''

    def clean_and_save_transcript(self, transcript_path):
        """Clean the transcript and save it to a new file"""
        try:
            # Read the transcript
            with open(transcript_path, 'r', encoding='utf-8') as file:
                transcript_text = file.read()

            # Process with OpenAI
            response = openai.Completion.create(
                engine="davinci-002",
                prompt=self.prompt + "\n\n" + transcript_text,
                max_tokens=200,
                temperature=0.1,
            )
            cleaned_text = response.choices[0].text.strip()

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