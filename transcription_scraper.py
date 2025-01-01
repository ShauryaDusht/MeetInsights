from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import threading
import time
import os

class TranscriptionScraper:
    def __init__(self, driver):
        print("[DEBUG] Initializing TranscriptionScraper")
        self.driver = driver
        self.is_running = False
        self.transcript = []
        self.scraper_thread = None
        self.lock = threading.Lock()
        
    def start_transcription(self):
        print("[DEBUG] Starting transcription thread")
        self.is_running = True
        self.scraper_thread = threading.Thread(target=self._scrape_loop)
        self.scraper_thread.start()
        print("[DEBUG] Thread started successfully")
        
    def stop_transcription(self):
        print("[DEBUG] Stopping transcription")
        self.is_running = False
        if self.scraper_thread:
            self.scraper_thread.join()
        self._save_transcript()
        print("[DEBUG] Transcription stopped and saved")
            
    def _scrape_loop(self):
        last_caption = None
        print("[DEBUG] Entering scrape loop")
        
        while self.is_running:
            try:
                print("[DEBUG] Looking for caption container")
                caption_container = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "bh44bd.VbkSUe"))
                )
                print("[DEBUG] Caption container found")
                
                # Refresh the span elements every loop to ensure dynamic content is captured
                spans = caption_container.find_elements(By.TAG_NAME, "span")
                print(f"[DEBUG] Found {len(spans)} span elements")
                
                current_caption = " ".join(span.text for span in spans if span.text.strip())
                print(f"[DEBUG] Current caption: {current_caption}")
                
                # Add new captions to the transcript if they differ from the last one
                if current_caption and current_caption != last_caption:
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    print(f"[DEBUG] New caption at {timestamp}")
                    with self.lock:
                        self.transcript.append(f"[{timestamp}] {current_caption}")
                        print("[DEBUG] Saving transcript")
                        self._save_transcript()
                    last_caption = current_caption
                    
            except Exception as e:
                print(f"[DEBUG] Error in scrape loop: {str(e)}")
            
            # Sleep to control scraping frequency
            time.sleep(1)  # Scrapes captions every second
        return
            
    def _save_transcript(self):
        try:
            transcript_dir = os.path.abspath("transcripts")
            os.makedirs(transcript_dir, exist_ok=True)
            filename = os.path.join(transcript_dir, f"meet_transcript_{datetime.now().strftime('%Y%m%d_%H%M')}.txt")
            print(f"[DEBUG] Preparing to write transcript to: {filename}")
            
            with self.lock:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("\n".join(self.transcript))
            print(f"[DEBUG] Successfully saved transcript to {filename}")
        except Exception as e:
            print(f"[DEBUG] Failed to save transcript: {e}")
        return