from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from session_manager import get_meet_controller

'''USE EITHER OF TRASNSCRIPT CLEANER MODULES'''
from openai_transcript_cleaner import TranscriptCleaner
# from forefront_transcript_cleaner import TranscriptCleaner

# Function to get time input from user
def get_time_input(prompt):
    while True:
        try:
            time_str = input(prompt + " (format HH:MM): ")
            hour, minute = map(int, time_str.split(':'))
            if 0 <= hour <= 23 and 0 <= minute <= 59:
                curr_time = datetime.now()
                return curr_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
            else:
                print("Invalid time. Hours should be 0-23 and minutes should be 0-59.")
        except ValueError:
            print("Invalid format. Please use HH:MM format (e.g., 14:30)")

def main():
    # Load environment variables
    load_dotenv()
    
    # Get environment variables
    mail_address = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
    meeting_link = os.getenv("MEETING_LINK")
    
    if not all([mail_address, password, meeting_link]):
        raise ValueError("Missing required environment variables")

    # Set up meeting times
    print("The entering time should be atleast 2 minutes before the meeting starts...")
    join_time_ist = get_time_input("Enter meeting join time")
    exit_time_ist = get_time_input("Enter meeting exit time")
    
    # Validate that exit time is after join time
    if exit_time_ist <= join_time_ist:
        raise ValueError("Exit time must be after join time")
    
    print(f"Joining the meeting at {join_time_ist.time()} and exiting at {exit_time_ist.time()}.")

    try:
        meet_controller = get_meet_controller()
        meet_controller.initialize_driver()

        meet_controller.google_login(mail_address, password)
        meet_controller.join_meet(meeting_link, join_time_ist, exit_time_ist)

        print("Meeting ended. Processing transcript...")

        try:
            transcript_cleaner = TranscriptCleaner()
            
            latest_transcript = transcript_cleaner.get_latest_transcript()
            
            cleaned_transcript_path = transcript_cleaner.clean_and_save_transcript(latest_transcript)
            print("Transcript processing completed successfully")
            
        except Exception as e:
            print(f"Failed to process transcript: {str(e)}")
            raise

    except Exception as e:
        print(f"Error during meeting or transcript processing: {str(e)}")
        raise
    finally:
        print("Script execution completed")

if __name__ == "__main__":
    main()