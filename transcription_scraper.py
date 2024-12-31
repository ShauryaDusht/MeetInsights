from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

class TranscriptionScraper:
    def __init__(self, driver):
        self.driver = driver
        self.transcript_texts = []
        self.last_text = None

    def _extract_transcript_text(self):
        """Extract text from the transcript elements"""
        try:
            # Using the class names from the screenshot
            transcript_elements = self.driver.find_elements(
                By.CSS_SELECTOR, 
                "div.bh4Abd.VbkSUe span"
            )
            
            for element in transcript_elements:
                text = element.text.strip()
                if text and text != self.last_text:
                    self.transcript_texts.append(text)
                    self.last_text = text
                    # Print the text as it's captured (optional)
                    print(f"Captured: {text}")
                    
        except Exception as e:
            print(f"Error extracting transcript: {str(e)}")

    def save_transcript(self, filename=None):
        """Save the collected transcript to a file"""
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"transcript_{timestamp}.txt" if filename is None else filename
        
        # Create a transcripts directory if it doesn't exist
        os.makedirs('transcripts', exist_ok=True)
        filepath = os.path.join('transcripts', filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            for text in self.transcript_texts:
                f.write(text + '\n')
        
        print(f"Transcript saved to {filepath}")

    def start_scraping(self, interval=2):
        """
        Start scraping the transcript continuously
        
        Args:
            interval (int): Time interval between scraping attempts in seconds
        """
        print("Starting transcript scraping...")
        last_save_time = time.time()
        save_interval = 60  # Save every 60 seconds
        
        try:
            while True:
                self._extract_transcript_text()
                
                # Auto-save periodically
                current_time = time.time()
                if current_time - last_save_time >= save_interval:
                    self.save_transcript()
                    last_save_time = current_time
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\nStopping transcript scraping...")
            self.save_transcript()  # Final save on exit
        except Exception as e:
            print(f"Error during scraping: {str(e)}")
            self.save_transcript()  # Save on error

def get_transcription_scraper(driver):
    """Factory function to create a TranscriptionScraper instance"""
    return TranscriptionScraper(driver)

# Example usage in a standalone script
if __name__ == "__main__":
    # This is just example code showing how to use the scraper directly
    from selenium.webdriver.chrome.options import Options
    
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option(
        "prefs",
        {
            "profile.default_content_setting_values.media_stream_mic": 1,
            "profile.default_content_setting_values.media_stream_camera": 1,
            # make captions visible by default to scrape them
            "profile.default_content_setting_values.notifications": 2,
        },
    )
    
    # Initialize driver
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Navigate to Google Meet (you would need to handle login and joining meeting)
        meet_link = "https://meet.google.com/zfd-uocg-egd"
        driver.get(meet_link)
        
        # Create and start the scraper
        scraper = get_transcription_scraper(driver)
        scraper.start_scraping()
        
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        driver.quit()