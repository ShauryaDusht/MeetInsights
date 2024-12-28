from datetime import datetime
import time
from dotenv import load_dotenv
import os
from session_manager import get_meet_controller

load_dotenv()

curr_time = time.time()
join_time_ist = datetime.fromtimestamp(curr_time + 150)   # 2min 30sec from now
# exit_time_ist = datetime.fromtimestamp(curr_time + 750)   # 12min 30sec from now
exit_time_ist = datetime.fromtimestamp(curr_time + 300)   # 5 min from now
print(f"Joining the meeting at {join_time_ist.time()} and exiting at {exit_time_ist.time()}.")

# Get environment variables
mail_address = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
meeting_link = os.getenv("MEETING_LINK")

def main():
    print("Phase 1 - Initializing the driver and joining the meeting.")
    # Get controller instance
    meet_controller = get_meet_controller()

    # Initialize driver
    meet_controller.initialize_driver()

    # Login and join meeting
    meet_controller.google_login(mail_address, password)
    meet_controller.join_meet(meeting_link, join_time_ist, exit_time_ist)
    
    print("Phase 2 - Recording the meeting in 5 minute intervals.")
    print("Phase 3 - Transcribing the recorded audio.")
    print("Phase 4 - Summarizing the transcribed text and storing it in a file.")

if __name__ == "__main__":
    main()