import sounddevice as sd
import os
from threading import Thread
import wave
import numpy as np

class AudioRecorder:
    def __init__(self):
        self.sample_rate = int(os.getenv('SAMPLE_RATE', 44100))
        self.recording = False
        self.audio_thread = None
        
    def record_audio(self, filename):
        """Record audio in chunks and save to file"""
        print(f"Starting audio recording to {filename}")
        frames = []
        
        with sd.InputStream(samplerate=self.sample_rate, channels=2, dtype='int16') as stream:
            while self.recording:
                data, _ = stream.read(self.sample_rate)  # Read 1 second of audio
                frames.append(data)
        
        # Save the recorded audio
        if frames:
            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(2)
                wf.setsampwidth(2)  # 16-bit audio
                wf.setframerate(self.sample_rate)
                wf.writeframes(np.concatenate(frames).tobytes())
            print(f"Recording saved to {filename}")
    
    def start_recording(self, filename):
        """Start recording in a separate thread"""
        self.recording = True
        self.audio_thread = Thread(target=self.record_audio, args=(filename,))
        self.audio_thread.start()
    
    def stop_recording(self):
        """Stop the current recording"""
        if self.recording:
            self.recording = False
            if self.audio_thread:
                self.audio_thread.join()
                self.audio_thread = None