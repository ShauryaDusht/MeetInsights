# 🎯 MeetInsights

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-green.svg)](https://openai.com/)
[![Google AI](https://img.shields.io/badge/Google-Gemini-red.svg)](https://deepmind.google/technologies/gemini/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

🤖 AI-powered assistant that automatically joins Google Meet sessions, captures conversations, and generates transcripts.

## ✨ Features

- 🎥 Automated meeting attendance
- 📝 Real-time transcription
- 🧠 AI-enhanced transcript cleaning
- 🔌 Support for OpenAI, Google Gemini, and Forefront APIs

## 🚀 Installation

1. Clone repository:
```bash
git clone https://github.com/ShauryaDusht/MeetInsights.git
cd MeetInsights
```

2. Set up environment:
```bash
python -m venv venv
source venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

3. Configure `.env`:
```env
EMAIL=your.email@gmail.com
PASSWORD=your-google-password
MEETING_LINK=https://meet.google.com/xxx-xxxx-xxx
GEMINI_API_KEY='your-key'  # Or use OPENAI_API_KEY/FOREFRONT_API_KEY
```

4. Install ChromeDriver and add to PATH

## 💻 Usage
```
python main.py
```

## 🤝 Contributing

1. 🍴 Fork repository
2. 🌱 Create feature branch
3. 🚀 Submit pull request

## 📫 Support

- 📧 Email: shauryadusht@gmail.com
- 🎫 Issues: [GitHub Issues](https://github.com/ShauryaDusht/MeetInsights/issues)
