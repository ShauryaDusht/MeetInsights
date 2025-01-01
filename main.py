from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from session_manager import get_meet_controller

load_dotenv()

curr_time = datetime.now()
join_time_ist = curr_time + timedelta(seconds=60) # 60 seconds from now
exit_time_ist = curr_time + timedelta(seconds=300) # 300 seconds from now
print(f"Joining the meeting at {join_time_ist.time()} and exiting at {exit_time_ist.time()}.")

# Get environment variables
mail_address = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
meeting_link = os.getenv("MEETING_LINK")

def main():
    # Get controller instance
    meet_controller = get_meet_controller()
    # Initialize driver
    meet_controller.initialize_driver()

    # Login and join meeting
    meet_controller.google_login(mail_address, password)
    meet_controller.join_meet(meeting_link, join_time_ist, exit_time_ist)

if __name__ == "__main__":
    main()