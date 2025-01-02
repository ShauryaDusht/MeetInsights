from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from datetime import datetime
import threading
import time
import os
import traceback

class TranscriptionScraper:
    def __init__(self, driver):
        print("Initializing TranscriptionScraper")
        self.driver = driver
        self.is_running = False
        self.transcript = []
        self.scraper_thread = None
        self.lock = threading.Lock()
        self.last_save_time = time.time()
        self.save_interval = 4
        self.scrape_interval = 4
        self.last_scrape_time = 0
        
        self.filename = self._generate_filename()
        self._test_file_permissions()
    
    def _enable_captions(self):
        print("Enabling captions...")
        selectors = [
            'button[aria-label*="captions"][jsname="r8qRAd"]',
            'button[aria-label*="subtitle"][jsname="r8qRAd"]',
            'button[data-is-muted="false"][aria-label*="caption"]'
        ]
        
        for selector in selectors:
            try:
                button = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                if button.get_attribute("aria-pressed") != "true":
                    button.click()
                    time.sleep(2)
                print("Captions enabled successfully")
                return True
            except Exception as e:
                continue
                
        print("Failed to enable captions")
        return False
    
    def _test_file_permissions(self):
        try:
            with open(self.filename, 'a', encoding='utf-8') as f:
                f.write("[START OF TRANSCRIPT]\n")
        except Exception as e:
            print(f"Error: Cannot write to file - {str(e)}")
            raise Exception("Cannot write to transcript file")
    
    def _generate_filename(self):
        try:
            transcript_dir = os.path.join(os.getcwd(), "transcripts")
            os.makedirs(transcript_dir, exist_ok=True)
            filename = os.path.join(transcript_dir, 
                                  f"meet_transcript_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            return filename
        except Exception as e:
            print(f"Error generating filename: {str(e)}")
            raise
            
    def _scrape_loop(self):
        last_caption = None
        print("Starting transcription loop")
        
        while self.is_running:
            try:
                current_time = time.time()
                if current_time - self.last_scrape_time < self.scrape_interval:
                    time.sleep(0.1)
                    continue
                
                selectors = [
                    ".bh44bd.VbkSUe",
                    ".iTTPOb",
                    ".VbkSUe",
                    "[jscontroller='yQsYHe']"
                ]
                
                caption_container = None
                for selector in selectors:
                    try:
                        caption_container = self.driver.find_element(By.CSS_SELECTOR, selector)
                        if caption_container:
                            break
                    except:
                        continue
                
                if caption_container:
                    spans = caption_container.find_elements(By.TAG_NAME, "span")
                    current_caption = " ".join(span.text for span in spans if span.text.strip())
                    
                    if current_caption and current_caption != last_caption:
                        timestamp = datetime.now().strftime("%H:%M:%S")
                        caption_entry = f"[{timestamp}] {current_caption}"
                        print(f"New caption: {caption_entry}")
                        
                        with self.lock:
                            self.transcript.append(caption_entry)
                            self._force_save_transcript()
                        
                        last_caption = current_caption
                
                self.last_scrape_time = current_time
                
            except Exception as e:
                print(f"Error during scraping: {str(e)}")
            
            time.sleep(0.1)
            
    def _force_save_transcript(self):
        try:
            current_time = time.time()
            if current_time - self.last_save_time < self.save_interval:
                return False
                
            with open(self.filename, 'a', encoding='utf-8') as f:
                while self.transcript:
                    line = self.transcript[0]
                    f.write(line + "\n")
                    f.flush()
                    os.fsync(f.fileno())
                    self.transcript.pop(0)
                    
            self.last_save_time = current_time
            print("Transcript saved to file")
            return True
            
        except Exception as e:
            print(f"Error saving transcript: {str(e)}")
            return False
            
    def start_transcription(self):
        print("Starting transcription")
        self._enable_captions()
        self.is_running = True
        self.scraper_thread = threading.Thread(target=self._scrape_loop)
        self.scraper_thread.daemon = True
        self.scraper_thread.start()

    def stop_transcription(self):
        print("Stopping transcription")
        self.is_running = False
        if self.scraper_thread:
            self.scraper_thread.join(timeout=5)
        with self.lock:
            self._force_save_transcript()
        print("Transcription ended")