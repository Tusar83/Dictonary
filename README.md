# 📚 Dictionary App

A modern, beautiful dictionary web app powered by NLTK WordNet with voice search, responsive design, and online API fallback.

![Streamlit](https://img.shields.io/badge/Streamlit-1.28.1-red?style=flat&logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat&logo=python)
![NLTK](https://img.shields.io/badge/NLTK-3.8.1-green?style=flat)

## ✨ Features

- **🎤 Voice Search**: Click the microphone button and speak! Uses the browser's native Speech Recognition API
  - Supported browsers: Chrome, Edge, Safari (Firefox with flag)
  - Automatically fills search and triggers lookup
  
- **📱 Fully Responsive**: Perfect on mobile, tablet, and desktop
  - Adaptive layouts using CSS media queries
  - Touch-friendly buttons and inputs
  - No horizontal scrolling
  
- **📚 Offline Dictionary**: NLTK WordNet with 200,000+ English words
  - Definitions, synonyms, antonyms
  - Part-of-speech tags
  - Example sentences
  
- **🌐 Online Fallback**: WordsAPI integration for words not in WordNet
  - Seamless fallback when needed
  - Optional (requires API key)
  
- **🎨 Theme Toggle**: Light and dark mode
  - Beautiful gradient UI
  - Smooth transitions
  
- **📜 Search History**: Quick access to last 5 searches
  - Click sidebar buttons to revisit words
  
- **📥 Download Results**: Export word data as text files
  
- **⚡ Production Ready**: 
  - Error handling
  - Loading spinners
  - Fun error messages

## 🚀 Quick Start

### Local Installation

```bash
# 1. Clone or setup the project
cd Dictionary

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download NLTK data
python -c "import nltk; nltk.download('wordnet'); nltk.download('omw')"

# 4. Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

### Voice Search Setup

1. **Chrome/Edge/Safari**: Voice search works out of the box!
2. Click the **🎤 Voice Search** button
3. Speak the word you want to look up
4. The word will be automatically filled and searched

### Optional: WordsAPI Fallback

For words not in WordNet, enable online lookups:

```bash
# 1. Sign up (free tier available)
# https://www.wordsapi.com/

# 2. Get your API key

# 3. Set environment variable
# Windows (PowerShell):
$env:WORDS_API_KEY="your_api_key_here"

# Mac/Linux:
export WORDS_API_KEY="your_api_key_here"

# Or create .env file:
cp .env.example .env
# Edit .env and add your key
```

## 🌐 Deployment

### Streamlit Cloud (Free)

```bash
# 1. Push to GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/dictionary-app.git
git push -u origin main

# 2. Go to https://share.streamlit.io
# 3. Click "Deploy an app"
# 4. Select your repo and main file: app.py
# 5. Click Deploy!
```

Your app will be live at a unique URL!

### Docker

```bash
docker build -t dictionary-app .
docker run -p 8501:8501 dictionary-app
```

## 📋 Requirements

- Python 3.8+
- Streamlit 1.28.1+
- NLTK 3.8.1+
- Requests 2.31.0+ (for WordsAPI)
- python-dotenv 1.0.0+ (for .env support)

See `requirements.txt` for exact versions.

## 🎯 Usage Tips

1. **Voice Search Works Best With:**
   - Clear, slow pronunciation
   - Single words (not phrases)
   - English pronunciation
   - Quiet environments (for accuracy)

2. **For Complex Words:**
   - Use the text input for better accuracy
   - Or spell it out while using voice

3. **Mobile Users:**
   - All features work on mobile browsers
   - Voice search especially useful on mobile!
   - Sidebar collapses automatically

4. **API Key Optional:**
   - Works perfectly offline with WordNet
   - API key only needed for extended word coverage

## 🛠️ Tech Stack

- **Frontend**: Streamlit (Python web framework)
- **Backend**: NLTK, WordsAPI, Web Speech API
- **Responsive Design**: CSS media queries
- **Voice Input**: Browser's native Speech Recognition API

## 📝 Project Structure

```
Dictionary/
├── app.py              # Main Streamlit app
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
├── .gitignore         # Git ignore rules
└── venv/              # Virtual environment
```

## 🐛 Troubleshooting

### Voice search not working?
- Check browser support: Chrome, Edge, Safari
- Allow microphone permissions
- Try a different browser
- Check browser console for errors (F12)

### WordsAPI not working?
- Verify API key is set correctly
- Check internet connection
- Free tier has rate limits

### App won't start?
- Ensure all dependencies installed: `pip install -r requirements.txt`
- NLTK data downloaded: `python -c "import nltk; nltk.download('wordnet')"`
- Python 3.8+ version

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📞 Support

For issues, questions, or feature requests, please open a GitHub issue.

---

**Made with ❤️ using Streamlit & NLTK**

Enjoy exploring the English language! 📚✨
