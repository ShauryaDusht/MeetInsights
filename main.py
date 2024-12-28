from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pytz
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

def googleLogin(driver, mail_address, password):
    driver.get(
        "https://accounts.google.com/ServiceLogin?hl=en&passive=true&continue=https://www.google.com/&ec=GAZAAQ"
    )
    driver.find_element(By.ID, "identifierId").send_keys(mail_address)
    driver.find_element(By.ID, "identifierNext").click()
    driver.implicitly_wait(10)
    driver.find_element(
        By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input'
    ).send_keys(password)
    driver.implicitly_wait(10)
    time.sleep(2)
    driver.find_element(By.ID, "passwordNext").click()
    driver.implicitly_wait(10)
    driver.get("https://accounts.google.com/")
    driver.implicitly_wait(10)

def handle_name_dialog(driver):
    try:
        # Wait for the name input field
        name_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "name"))
        )
        # Enter your name (you can modify this)
        name_input.send_keys("Automated Attendee")
        
        # Look for and click the submit/continue button
        submit_buttons = driver.find_elements(By.XPATH, "//button[contains(span, 'Continue') or contains(span, 'Join')]")
        if submit_buttons:
            submit_buttons[0].click()
            print("Name submitted successfully")
            time.sleep(2)
        else:
            print("Submit button not found after entering name")
    except Exception as e:
        print(f"No name dialog found or error handling it: {str(e)}")

def offMicAndCam(driver):
    time.sleep(2)
    try:
        mic_button = driver.find_element(
            By.XPATH, "//div[@aria-label='Turn off microphone']"
        )
        if mic_button:
            mic_button.click()
            print("Microphone turned off.")
    except Exception:
        print("Microphone button not found or already muted.")
    
    time.sleep(1)
    try:
        camera_button = driver.find_element(
            By.XPATH, "//div[@aria-label='Turn off camera']"
        )
        if camera_button:
            camera_button.click()
            print("Camera turned off.")
    except Exception:
        print("Camera button not found or already off.")
    
    time.sleep(1)
    
    # Handle name dialog before joining
    handle_name_dialog(driver)
    
    try:
        join_button = driver.find_element(By.XPATH, "//span[text()='Join now']")
        join_button.click()
        print("Joined the meeting.")
    except Exception:
        print("Join button not found.")
        try:
            ask_to_join_button = driver.find_element(
                By.XPATH, "//span[text()='Ask to join']"
            )
            ask_to_join_button.click()
            print("Requested to join the meeting.")
        except Exception:
            print("Neither 'Join now' nor 'Ask to join' button was found.")

def joinMeet(driver, meeting_link, join_time_ist, exit_time_ist):
    ist = pytz.timezone("Asia/Kolkata")
    join_time_utc = ist.localize(join_time_ist).astimezone(pytz.utc)
    exit_time_utc = ist.localize(exit_time_ist).astimezone(pytz.utc)
    
    wait_time = (join_time_utc - datetime.now(pytz.utc)).total_seconds()
    if wait_time:
        time.sleep(wait_time)
    
    driver.get(meeting_link)
    time.sleep(5)
    
    offMicAndCam(driver)
    print("Meeting started.")
    
    wait_time = (exit_time_utc - datetime.now(pytz.utc)).total_seconds()
    if wait_time > 0:
        time.sleep(wait_time)
    
    driver.quit()
    print("Meeting ended. Chrome tab closed.")



curr_time = time.time()
join_time_ist = datetime.fromtimestamp(curr_time + 150)   # 2.5 minutes from now
exit_time_ist = datetime.fromtimestamp(curr_time + 360)   # 6 minutes from now
print(f"Joining the meeting at {join_time_ist.time()} and exiting at {exit_time_ist.time()}.")

mail_address = os.getenv("EMAIL")
password =  os.getenv("PASSWORD")
meeting_link = os.getenv("MEETING_LINK")

'''
FOR THE FINAL VERSION, UNCOMMENT THE FOLLOWING CODE AND COMMENT THE ABOVE CODE

today = datetime.now().date()

join_time_ist = datetime.combine(
    today,
    datetime.strptime(
        input("Enter the start time in the format HH:MM:SS: "), "%H:%M:%S"
    ).time(),
)
exit_time_ist = datetime.combine(
    today,
    datetime.strptime(
        input("Enter the end time in the format HH:MM:SS: "), "%H:%M:%S"
    ).time(),
)

mail_address = input("Enter your email: ")
password = getpass.getpass("Enter your password: ")
meeting_link = input("Enter the meeting link: ")
'''

opt = Options()
# disable automation warning
opt.add_argument("--disable-blink-features=AutomationControlled")
# open Browser in maximized mode
opt.add_argument("--start-maximized") 
opt.add_experimental_option(
    "prefs",
    {
        "profile.default_content_setting_values.media_stream_mic": 1,
        "profile.default_content_setting_values.media_stream_camera": 1,
        "profile.default_content_setting_values.geolocation": 0,
        "profile.default_content_setting_values.notifications": 1,
    },
)

def main():
    driver = webdriver.Chrome(options=opt)
    googleLogin(driver, mail_address, password)
    joinMeet(driver, meeting_link, join_time_ist, exit_time_ist)

if __name__ == "__main__":
    main()