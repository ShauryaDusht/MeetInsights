from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import pytz
import time
# from audio_recorder import AudioRecorder
from transcription_scraper import TranscriptionScraper
class MeetController:
    def __init__(self):
        self.opt = self._setup_chrome_options()
        self.driver = None
        # self.audio_recorder = AudioRecorder()
        self.transcription_scraper = None
     
    def _setup_chrome_options(self):
        """Set up Chrome options for the webdriver"""
        opt = Options()
        # disable automation warning
        opt.add_argument("--disable-blink-features=AutomationControlled")
        # open Browser in maximized mode
        opt.add_argument("--start-maximized")
        opt.add_experimental_option(
            "prefs",
            {
                # turn off microphone by default
                "profile.default_content_setting_values.media_stream_mic": 1,
                # turn off camera by default
                "profile.default_content_setting_values.media_stream_camera": 1,
                "profile.default_content_setting_values.geolocation": 0,
                "profile.default_content_setting_values.notifications": 1,
                # enable captions
                "accessibility.captions.enabled": True,
                "accessibility.captions.on": 1
            },
        )
        return opt

    def initialize_driver(self):
        """Initialize the Chrome webdriver"""
        self.driver = webdriver.Chrome(options=self.opt)
        return self.driver

    def google_login(self, mail_address, password):
        """
        Login to Google account
        
        Args:
            mail_address (str): Google account email
            password (str): Google account password
        """
        self.driver.get(
            "https://accounts.google.com/ServiceLogin?hl=en&passive=true&continue=https://www.google.com/&ec=GAZAAQ"
        )
        self.driver.find_element(By.ID, "identifierId").send_keys(mail_address)
        self.driver.find_element(By.ID, "identifierNext").click()
        self.driver.implicitly_wait(10)
        self.driver.find_element(
            By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input'
        ).send_keys(password)
        self.driver.implicitly_wait(10)
        time.sleep(2)
        self.driver.find_element(By.ID, "passwordNext").click()
        self.driver.implicitly_wait(10)
        self.driver.get("https://accounts.google.com/")
        self.driver.implicitly_wait(10)

    def _handle_name_dialog(self, custom_name=None):
        """
        Handle the name input dialog in Google Meet
        
        Args:
            custom_name (str, optional): Custom name to use in the meeting. Defaults to "Automated Attendee"
        """
        try:
            name_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "name"))
            )
            name_input.send_keys(custom_name or "Automated Attendee")
            
            submit_buttons = self.driver.find_elements(
                By.XPATH, "//button[contains(span, 'Continue') or contains(span, 'Join')]"
            )
            if submit_buttons:
                submit_buttons[0].click()
                print("Name submitted successfully")
                time.sleep(2)
            else:
                print("Submit button not found after entering name")
        except Exception as e:
            print(f"No name dialog found or error handling it: {str(e)}")

    def _handle_mic_and_camera(self):
        """Turn off microphone and camera before joining the meeting"""
        time.sleep(2)
        try:
            mic_button = self.driver.find_element(
                By.XPATH, "//div[@aria-label='Turn off microphone']"
            )
            if mic_button:
                mic_button.click()
                print("Microphone turned off.")
        except Exception:
            print("Microphone button not found or already muted.")
        
        time.sleep(1)
        try:
            camera_button = self.driver.find_element(
                By.XPATH, "//div[@aria-label='Turn off camera']"
            )
            if camera_button:
                camera_button.click()
                print("Camera turned off.")
        except Exception:
            print("Camera button not found or already off.")

    def _join_meeting_room(self):
        """Attempt to join the meeting"""
        try:
            join_button = self.driver.find_element(By.XPATH, "//span[text()='Join now']")
            join_button.click()
            print("Joined the meeting.")
        except Exception:
            print("Join button not found.")
            try:
                ask_to_join_button = self.driver.find_element(
                    By.XPATH, "//span[text()='Ask to join']"
                )
                ask_to_join_button.click()
                print("Requested to join the meeting.")
            except Exception:
                print("Neither 'Join now' nor 'Ask to join' button was found.")

    def join_meet(self, meeting_link, join_time_ist, exit_time_ist, timezone="Asia/Kolkata"):
        """
        Join a Google Meet session at specified time and record audio
        """
        tz = pytz.timezone(timezone)
        join_time_utc = tz.localize(join_time_ist).astimezone(pytz.utc)
        exit_time_utc = tz.localize(exit_time_ist).astimezone(pytz.utc)
        
        wait_time = (join_time_utc - datetime.now(pytz.utc)).total_seconds()
        if wait_time > 0:
            print(f"Waiting for {wait_time:.2f} seconds before joining...")
            time.sleep(wait_time)
        
        self.driver.get(meeting_link)
        time.sleep(5)
        
        self._handle_mic_and_camera()
        self._handle_name_dialog()
        self._join_meeting_room()
        print("Meeting started.")
        
        try:
            time.sleep(10)  # Wait for meeting to fully load
            
            # Initialize and start transcription scraping
            self.transcription_scraper = TranscriptionScraper(self.driver)
            self.transcription_scraper.start_transcription()
            
            # Continuous monitoring loop
            while True:
                current_time = datetime.now(pytz.utc)
                wait_time = (exit_time_utc - current_time).total_seconds()
                
                if wait_time <= 0:
                    print("Meeting time is up. Preparing to exit...")
                    break
                
                # Print remaining time every minute
                if int(wait_time) % 60 == 0:
                    print(f"Time remaining in meeting: {int(wait_time/60)} minutes")
                
                # Brief sleep to prevent CPU overuse
                time.sleep(1)
                
                # Check if transcription is still running
                if not self.transcription_scraper.is_running:
                    print("Transcription stopped unexpectedly. Attempting to restart...")
                    self.transcription_scraper.start_transcription()

        except Exception as e:
            print(f"Error during meeting: {str(e)}")
        finally:
            if self.transcription_scraper:
                print("Stopping transcription...")
                self.transcription_scraper.stop_transcription()
            print("Closing browser...")
            self.driver.quit()
            print("Meeting ended. Chrome tab closed.")
        return

def get_meet_controller():
    '''
    Returns an instance of MeetController : All the functions of MeetController can be accessed using this instance
    '''
    return MeetController()