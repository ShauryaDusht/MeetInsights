import os
import requests

'''
$$$$$$$$\ $$$$$$$\   $$$$$$\  $$\   $$\  $$$$$$\   $$$$$$\  $$$$$$$\  $$$$$$\ $$$$$$$\ $$$$$$$$\ 
\__$$  __|$$  __$$\ $$  __$$\ $$$\  $$ |$$  __$$\ $$  __$$\ $$  __$$\ \_$$  _|$$  __$$\\__$$  __|
   $$ |   $$ |  $$ |$$ /  $$ |$$$$\ $$ |$$ /  \__|$$ /  \__|$$ |  $$ |  $$ |  $$ |  $$ |  $$ |   
   $$ |   $$$$$$$  |$$$$$$$$ |$$ $$\$$ |\$$$$$$\  $$ |      $$$$$$$  |  $$ |  $$$$$$$  |  $$ |   
   $$ |   $$  __$$< $$  __$$ |$$ \$$$$ | \____$$\ $$ |      $$  __$$<   $$ |  $$  ____/   $$ |   
   $$ |   $$ |  $$ |$$ |  $$ |$$ |\$$$ |$$\   $$ |$$ |  $$\ $$ |  $$ |  $$ |  $$ |        $$ |   
   $$ |   $$ |  $$ |$$ |  $$ |$$ | \$$ |\$$$$$$  |\$$$$$$  |$$ |  $$ |$$$$$$\ $$ |        $$ |   
   \__|   \__|  \__|\__|  \__|\__|  \__| \______/  \______/ \__|  \__|\______|\__|        \__|   
            $$$$$$\  $$\       $$$$$$$$\  $$$$$$\  $$\   $$\ $$$$$$$$\ $$$$$$$\  
            $$  __$$\ $$ |      $$  _____|$$  __$$\ $$$\  $$ |$$  _____|$$  __$$\ 
            $$ /  \__|$$ |      $$ |      $$ /  $$ |$$$$\ $$ |$$ |      $$ |  $$ |
            $$ |      $$ |      $$$$$\    $$$$$$$$ |$$ $$\$$ |$$$$$\    $$$$$$$  |
            $$ |      $$ |      $$  __|   $$  __$$ |$$ \$$$$ |$$  __|   $$  __$$< 
            $$ |  $$\ $$ |      $$ |      $$ |  $$ |$$ |\$$$ |$$ |      $$ |  $$ |
            \$$$$$$  |$$$$$$$$\ $$$$$$$$\ $$ |  $$ |$$ | \$$ |$$$$$$$$\ $$ |  $$ |
            \______/ \________|\________|\__|  \__|\__|  \__|\________|\__|  \__|
'''

class TranscriptCleaner:
    def __init__(self):
        self.api_key = os.getenv("FOREFRONT_API_KEY")
        
        if not self.api_key:
            raise ValueError("Forefront API key not found in environment variables")
        
        self.url = "https://api.forefront.ai/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        self.system_prompt = '''
            You are a transcript cleaning assistant. Clean the following transcript by:
            1 Removing repetitive phrases and stutters
            2 Preserving key information and timestamps
            3 Formatting the output for clarity
            4 Retaining technical terms and instructions         
            Format the output with timestamps at the start of each paragraph
        '''

    def clean_and_save_transcript(self, transcript_path):
        """Clean the transcript using Forefront AI and save it to a new file"""
        try:
            # Read the transcript
            with open(transcript_path, 'r', encoding='utf-8') as file:
                transcript_text = file.read()

            # Prepare the API payload
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
                "max_tokens": 1000,
                "temperature": 0.2
            }

            # Make API request
            response = requests.post(
                self.url, 
                json=payload, 
                headers=self.headers, 
                timeout=120
            )
            
            print(f"[STATUS]: {response.status_code}")
            
            if response.status_code != 200:
                raise Exception(f"API request failed: {response.text}")

            # Extract cleaned text from response
            cleaned_text = response.json()['choices'][0]['message']['content']

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

        except requests.exceptions.Timeout:
            print("[ERROR]: Request timed out. Try reducing the transcript length.")
            raise
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