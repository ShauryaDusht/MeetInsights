# 🎯 MeetInsights

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-green.svg)](https://openai.com/)
[![Google AI](https://img.shields.io/badge/Google-Gemini-red.svg)](https://deepmind.google/technologies/gemini/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Chrome](https://img.shields.io/badge/Chrome-Required-blue.svg)](https://www.google.com/chrome/)

> 🚀 Transform your virtual meetings with MeetInsights - an intelligent assistant that automatically joins Google Meet sessions, captures conversations, and generates polished, professional transcripts using advanced AI. Never miss a critical meeting detail again! ✨

## 💡 Motivation

Ever missed an important meeting because of a scheduling conflict? Or spent hours transcribing meeting recordings? MeetInsights was born from these common frustrations! 

As remote work became the norm, I found myself juggling multiple meetings while trying to keep track of important discussions. The existing solutions were either expensive, unreliable, or required manual intervention. That's when I decided to create MeetInsights - a tool that could not only attend meetings on my behalf but also provide clean, accurate transcripts powered by AI.

## 🌟 Core Features

### 🤖 Works Like a Real Assistant
- Shows up on time to your meetings
- Takes detailed notes
- Leaves when the meeting ends
- Sends you polished meeting transcripts

### 🧠 Powered by AI
- Uses OpenAI/Google Gemini to clean up transcripts
- Removes filler words and repetitions
- Keeps important technical details intact
- Makes notes easy to read and understand

## 🚀 Getting Started

### 📋 System Requirements
- 🐍 Python 3.9 or higher
- 🌐 Google Chrome (latest version)
- 📧 Active Google Account
- 🔑 One of the following API keys:
  - Google Gemini API key
  - OpenAI API key
  - Forefront API key

### ⚡ Quick Installation

1. **Clone Repository** 📦:
   ```bash
   git clone https://github.com/ShauryaDusht/MeetInsights.git
   cd MeetInsights
   ```

2. **Set Up Environment** 🛠️:
   Run the following commands in terminal:
   ```
   python -m venv venv
   ```
   ```
   .venv\Scripts\activate # On Windows
   ```
   ```
   source venv/bin/activate  # On Mac/Linux 
   ```
   ```
   pip install -r requirements.txt
   ```

3. **Configure Settings** ⚙️:

   Create `.env` file in project root:
   ```env
   # Required Settings ✨
   EMAIL=your.email@gmail.com
   PASSWORD=your-google-password
   MEETING_LINK=https://meet.google.com/xxx-xxxx-xxx

   # Choose ONE of the following API keys 🔑
   OPENAI_API_KEY='your-openai-key'
   GEMINI_API_KEY='your-gemini-key'
   FOREFRONT_API_KEY='your-forefront-key'
   ```
4. **Other Requirements** 📦:
- Download [ChromeDriver](https://chromedriver.chromium.org/downloads) and add to PATH
- Ensure Google Meet is set to English language
- Keep the system awake during the meeting

## 💻 Usage Guide

### 🎮 Basic Operation
1. **Launch Application** 🚀:
   ```
   python main.py
   ```

2. **Schedule Meeting** 📅:
   ```bash
   Enter meeting join time (HH:MM): 09:55  # Join 5 minutes early
   Enter meeting exit time (HH:MM): 11:00
   ```

3. **Monitor Progress** 📊:
   - 👀 View real-time transcription status
   - ⏳ Check processing progress
   - 📂 Access cleaned transcripts in `cleaned_transcripts/`

## 📂 Project Architecture

```
MeetInsights/
├── session_manager.py          # Meeting session control
├── transcription_scraper.py    # Caption extraction
├── gemini_cleaner.py           # Gemini AI processing
├── openai_cleaner.py           # OpenAI processing
├── forefront_cleaner.py        # Forefront AI processing
├── main.py                     # Application entry point
├── requirements.txt            # Dependencies
├── .env                        # Configuration settings (make sure to add this)
└── README.md                   # Documentation
```

## 🤝 Contributing

We welcome contributions! Here's how to get involved:

1. 🍴 **Fork the Repository**
2. 🌟 **Create Feature Branch**
3. 💾 **Commit Changes**
4. 🚀 **Push Branch**
5. ✨ **Open Pull Request**

## 📫 Support & Contact

Need help? Reach out through:
- 📧 Email: [shauryadusht@gmail.com](mailto:shauryadusht@gmail.com)
- 🎫 Issues: [GitHub Issues](https://github.com/ShauryaDusht/MeetInsights/issues)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. ⚖️