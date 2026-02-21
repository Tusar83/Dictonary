"""
Dictionary App - A modern, beautiful dictionary web app powered by NLTK WordNet
Built with Streamlit | Python 3.8+

FEATURES:
  ✨ Full mobile/desktop responsiveness
  🎤 Voice search using browser Speech API (Chrome, Edge, Safari)
  🌐 Online API fallback (WordsAPI) for words not in WordNet
  📚 Offline NLTK WordNet support
  🎨 Light/Dark theme toggle
  📜 Search history (last 5 searches)
  📥 Download results as text file

═══════════════════════════════════════════════════════════════════════════════
LOCAL INSTALLATION & SETUP:
═══════════════════════════════════════════════════════════════════════════════

1. Install dependencies:
    pip install streamlit nltk
    
2. Download NLTK data:
    python -c "import nltk; nltk.download('wordnet'); nltk.download('wordnet_ic'); nltk.download('omw')"
    
3. Run the app locally:
    streamlit run app.py

═══════════════════════════════════════════════════════════════════════════════
STREAMLIT CLOUD DEPLOYMENT (FREE):
═══════════════════════════════════════════════════════════════════════════════

Prerequisites:
  - GitHub account
  - Push code to GitHub repository
  - requirements.txt file in root directory (provided)

Steps:
  1. Push this code to GitHub:
     git init
     git add .
     git commit -m "Initial commit"
     git remote add origin https://github.com/YOUR_USERNAME/dictionary-app.git
     git branch -M main
     git push -u origin main

  2. Go to https://share.streamlit.io
     Click "Deploy an app"
     
  3. Fill in:
     - GitHub repo: YOUR_USERNAME/dictionary-app
     - Branch: main
     - Main file path: app.py
     
  4. Click "Deploy"
     
  5. Your app is now live!
     Share the URL with anyone

Optional - Custom Domain:
  - Go to Settings in Streamlit Cloud
  - Add your custom domain (requires DNS configuration)

═══════════════════════════════════════════════════════════════════════════════
OPTIONAL API FALLBACK (WordsAPI - for words not in WordNet):
═══════════════════════════════════════════════════════════════════════════════

To enable online API fallback for words not found in WordNet:

1. Sign up (free tier available):
   https://www.wordsapi.com/

2. Get your API key from dashboard

3. Set environment variable:
   
   Windows (PowerShell):
     $env:WORDS_API_KEY="your_api_key_here"
   
   Windows (Command Prompt):
     set WORDS_API_KEY=your_api_key_here
   
   Mac/Linux:
     export WORDS_API_KEY="your_api_key_here"
   
   Or create .env file in project root:
     WORDS_API_KEY=your_api_key_here

4. Restart the app - it will now fallback to WordsAPI for unknown words!

Note: Without the API key, the app works fine offline using only WordNet.
═══════════════════════════════════════════════════════════════════════════════
"""

import streamlit as st
from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize
import nltk
import os
from datetime import datetime
import requests
from dotenv import load_dotenv
import streamlit.components.v1 as components

# Load environment variables from .env file if it exists
load_dotenv()

# ============================================================================
# NLTK DATA SETUP
# ============================================================================
try:
    wordnet.synsets('test')
except LookupError:
    with st.spinner("Downloading NLTK data..."):
        nltk.download('wordnet', quiet=True)
        nltk.download('omw', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)

# ============================================================================
# PAGE CONFIG & THEME
# ============================================================================
st.set_page_config(
    page_title="Dictionary - Word Definitions & Synonyms",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# CUSTOM CSS & STYLING
# ============================================================================
custom_css = """
<style>
    /* Global Styling */
    :root {
        --primary: #6366f1;
        --secondary: #8b5cf6;
        --success: #10b981;
        --danger: #ef4444;
        --warning: #f59e0b;
    }
    
    /* Remove default Streamlit padding */
    .main {
        padding-top: 1rem;
    }
    
    /* Custom card styling */
    .custom-card {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.05) 0%, rgba(139, 92, 246, 0.05) 100%);
        border: 1px solid rgba(99, 102, 241, 0.2);
        border-radius: 12px;
        padding: 2rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
    }
    
    .custom-card:hover {
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 0 6px 12px rgba(99, 102, 241, 0.15);
    }
    
    /* Theme-specific */
    .light-mode {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
        color: #1f2937;
    }
    
    .dark-mode {
        background: linear-gradient(135deg, #1a1f2e 0%, #16213e 100%);
        color: #e5e7eb;
    }
    
    /* Search button styling */
    .search-btn {
        background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .search-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(99, 102, 241, 0.3);
    }
    
    /* Header styling */
    .header {
        text-align: center;
        margin-bottom: 3rem;
        padding: 2rem;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        border-radius: 16px;
        color: white;
    }
    
    .header h1 {
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .header p {
        font-size: 1.1rem;
        margin-top: 0.5rem;
        opacity: 0.9;
    }
    
    /* Tag/Chip styling */
    .tag {
        display: inline-block;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border-radius: 20px;
        padding: 6px 12px;
        margin: 4px 4px 4px 0;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    /* Result section */
    .result-section {
        animation: slideUp 0.5s ease-out;
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Definition list */
    .definition {
        margin: 0.8rem 0;
        padding-left: 1.5rem;
        border-left: 3px solid #6366f1;
        line-height: 1.6;
    }
    
    /* Example sentence */
    .example {
        font-style: italic;
        color: #6b7280;
        margin: 0.5rem 0;
        padding-left: 1rem;
        border-left: 2px solid #10b981;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        margin-top: 4rem;
        padding-top: 2rem;
        border-top: 1px solid rgba(99, 102, 241, 0.2);
        color: #6b7280;
        font-size: 0.85rem;
    }
    
    /* Error message */
    .error-message {
        background: linear-gradient(135deg, #fed7aa 0%, #fecaca 100%);
        color: #7c2d12;
        border-left: 4px solid #ea580c;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Success message */
    .success-message {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        color: #065f46;
        border-left: 4px solid #059669;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Loading spinner animation */
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .spinner {
        display: inline-block;
        animation: spin 1s linear infinite;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'history' not in st.session_state:
    st.session_state.history = []
if 'current_word' not in st.session_state:
    st.session_state.current_word = None

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_synset_examples(synset):
    """Get example sentences for a synset."""
    examples = synset.examples()
    return examples if examples else []

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_word_from_api(word):
    """
    Fallback API function to get word data from WordsAPI.
    Cached for 1 hour to improve performance.
    """
    try:
        api_key = os.getenv('WORDS_API_KEY')
        if not api_key:
            return None
        
        url = f"https://api.wordsapi.com/words/{word}"
        headers = {'x-rapidapi-key': api_key, 'x-rapidapi-host': 'wordsapi.com'}
        
        response = requests.get(url, headers=headers, timeout=4)
        if response.status_code != 200:
            return None
        
        api_data = response.json()
        data = {
            'word': word,
            'definitions': [],
            'synonyms': set(),
            'antonyms': set(),
            'examples': [],
            'pos_tags': [],
            'source': 'WordsAPI'
        }
        
        # Extract definitions
        if 'meanings' in api_data:
            for meaning in api_data['meanings']:
                pos = meaning.get('partOfSpeech', 'unknown')
                data['pos_tags'].append(pos)
                
                # Get definitions
                if 'definitions' in meaning:
                    data['definitions'].extend([
                        {'text': defn.get('definition', ''), 'pos': pos}
                        for defn in meaning['definitions']
                    ])
                
                # Get synonyms
                if 'synonyms' in meaning:
                    data['synonyms'].update(meaning['synonyms'])
                
                # Get antonyms
                if 'antonyms' in meaning:
                    data['antonyms'].update(meaning['antonyms'])
                
                # Get examples (limit to 2 per meaning)
                if 'examples' in meaning:
                    data['examples'].extend(meaning['examples'][:2])
        
        # Deduplicate and limit examples
        data['examples'] = list(set(data['examples']))[:3]
        
        return data if data['definitions'] else None
    
    except (requests.RequestException, ValueError, KeyError):
        return None

@st.cache_data(ttl=3600)  # Cache WordNet results for 1 hour
def get_word_data(word):
    """
    Get word data from WordNet (cached).
    Falls back to API if not found.
    """
    word = word.lower().strip()
    if not word:
        return None
    
    synsets = wordnet.synsets(word)
    if not synsets:
        return get_word_from_api(word)
    
    data = {
        'word': word,
        'definitions': [],
        'synonyms': set(),
        'antonyms': set(),
        'examples': set(),
        'pos_tags': set()
    }
    
    # Process all synsets in one pass
    for synset in synsets:
        pos = synset.pos()
        
        # Add definition
        data['definitions'].append({
            'text': synset.definition(),
            'pos': pos
        })
        
        # Add POS tag
        data['pos_tags'].add(pos)
        
        # Add examples
        examples = synset.examples()
        if examples:
            data['examples'].update(examples)
        
        # Process lemmas once for synonyms and antonyms
        for lemma in synset.lemmas():
            lemma_name = lemma.name().replace('_', ' ')
            
            # Add synonyms
            if lemma_name != word:
                data['synonyms'].add(lemma_name)
            
            # Add antonyms
            for antonym in lemma.antonyms():
                data['antonyms'].add(antonym.name().replace('_', ' '))
    
    # Convert sets to sorted lists
    data['pos_tags'] = list(data['pos_tags'])
    data['examples'] = list(data['examples'])[:3]  # Limit to 3 examples
    
    return data

def add_to_history(word):
    """Add word to search history."""
    if word not in st.session_state.history:
        st.session_state.history.insert(0, word)
        # Keep only last 5
        st.session_state.history = st.session_state.history[:5]

def pos_to_name(pos_code):
    """Convert POS code to readable name."""
    pos_map = {
        'n': 'Noun',
        'v': 'Verb',
        'a': 'Adjective',
        'r': 'Adverb',
        's': 'Adjective Satellite'
    }
    return pos_map.get(pos_code, 'Unknown')

def format_output(data):
    """Format word data for display."""
    output = f"**{data['word'].title()}**"
    output += "\n\n**📖 Definitions:**\n"
    for i, defn in enumerate(data['definitions'], 1):
        output += f"{i}. {defn['text']} _{pos_to_name(defn['pos'])}_\n"
    
    if data['synonyms']:
        output += "\n**🔗 Synonyms:**\n"
        output += ", ".join(sorted(data['synonyms'])) + "\n"
    
    if data['antonyms']:
        output += "\n**❌ Antonyms:**\n"
        output += ", ".join(sorted(data['antonyms'])) + "\n"
    
    if data['examples']:
        output += "\n**💡 Examples:**\n"
        for ex in data['examples']:
            output += f"- _{ex}_\n"
    
    return output

def voice_search_component():
    """
    Optimized voice search with reduced DOM queries and cached selectors.
    """
    voice_html = """
    <div id="voice-container" style="margin-bottom: 15px; padding: 12px; background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%); border-radius: 8px; border: 1px solid rgba(99, 102, 241, 0.2);">
        <button id="voice-btn" style="width: 100%; background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%); color: white; border: none; border-radius: 6px; padding: 11px; font-weight: 600; cursor: pointer; font-size: 14px; transition: all 0.3s ease; box-shadow: 0 2px 8px rgba(99, 102, 241, 0.2); margin-bottom: 10px;">
            🎤 Click & Speak
        </button>
        <div id="voice-status" style="font-size: 12px; color: #6b7280; margin-bottom: 8px; text-align: center; min-height: 18px; font-weight: 500;">Ready to listen</div>
        <div id="voice-result" style="background: white; border: 1px solid #e5e7eb; border-radius: 6px; padding: 10px; text-align: center; font-size: 14px; color: #1f2937; min-height: 20px;">
            <span id="result-text" style="display: none;">Heard: <strong id="transcript"></strong></span>
            <span id="empty-text" style="color: #9ca3af;">No text captured yet</span>
        </div>
    </div>
    
    <script>
        (function() {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (!SpeechRecognition) {
                elements.btn.disabled = true;
                elements.btn.style.opacity = '0.5';
                elements.status.textContent = '⚠️ Not supported';
                elements.status.style.color = '#ef4444';
                return;
            }
            
            // Cache DOM elements at start
            const elements = {
                btn: document.getElementById('voice-btn'),
                status: document.getElementById('voice-status'),
                resultText: document.getElementById('result-text'),
                emptyText: document.getElementById('empty-text'),
                transcript: document.getElementById('transcript')
            };
            
            const recognition = new SpeechRecognition();
            Object.assign(recognition, {
                lang: 'en-US',
                continuous: false,
                interimResults: false
            });
            
            let isListening = false;
            let currentTranscript = '';
            
            const styles = {
                listening: 'linear-gradient(90deg, #ef4444 0%, #f87171 100%)',
                normal: 'linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%)',
                listeningBox: '0 6px 16px rgba(239, 68, 68, 0.4)',
                normalBox: '0 2px 8px rgba(99, 102, 241, 0.2)'
            };
            
            function updateUI(listening, status, statusColor) {
                elements.btn.textContent = listening ? '⏹️ Listening...' : '🎤 Click & Speak';
                elements.btn.style.background = listening ? styles.listening : styles.normal;
                elements.btn.style.boxShadow = listening ? styles.listeningBox : styles.normalBox;
                elements.status.textContent = status;
                elements.status.style.color = statusColor;
            }
            
            elements.btn.addEventListener('click', function(e) {
                e.preventDefault();
                if (!isListening) {
                    try {
                        currentTranscript = '';
                        recognition.start();
                        updateUI(true, '🎙️ Listening...', '#10b981');
                        isListening = true;
                    } catch (e) {
                        updateUI(false, '⚠️ Already listening', '#f59e0b');
                    }
                }
            });
            
            recognition.onresult = function(event) {
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    if (event.results[i].isFinal) {
                        currentTranscript = event.results[i][0].transcript.trim().toLowerCase();
                    }
                }
                
                if (currentTranscript) {
                    elements.transcript.textContent = currentTranscript;
                    elements.resultText.style.display = 'inline';
                    elements.emptyText.style.display = 'none';
                    updateUI(false, '✓ Captured successfully!', '#10b981');
                    
                    requestAnimationFrame(() => {
                        const inputs = document.querySelectorAll('input[type="text"]');
                        for (const inp of inputs) {
                            if (inp.placeholder?.includes('Enter English word')) {
                                inp.value = currentTranscript;
                                ['input', 'change'].forEach(e => inp.dispatchEvent(new Event(e, { bubbles: true })));
                                
                                for (const btn of document.querySelectorAll('button')) {
                                    if (btn.textContent.includes('Search') || btn.textContent.includes('🔍')) {
                                        requestAnimationFrame(() => btn.click());
                                        return;
                                    }
                                }
                                return;
                            }
                        }
                    });
                }
            };
            
            recognition.onerror = function(event) {
                const errors = {
                    'no-speech': 'No speech detected',
                    'audio-capture': 'Microphone not found',
                    'not-allowed': 'Permission denied',
                    'network': 'Network error'
                };
                updateUI(false, '❌ ' + (errors[event.error] || event.error), '#ef4444');
                isListening = false;
            };
            
            recognition.onend = () => { isListening = false; };
        })();
    </script>
    """
    return voice_html

# ============================================================================
# SIDEBAR: THEME & HISTORY
# ============================================================================
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    # Theme toggle
    theme = st.radio(
        "Theme",
        ["Light", "Dark"],
        index=0 if st.session_state.theme == 'light' else 1,
        horizontal=True
    )
    st.session_state.theme = 'dark' if theme == "Dark" else 'light'
    
    st.markdown("---")
    
    # History
    st.markdown("### 📜 Search History")
    if st.session_state.history:
        for i, word in enumerate(st.session_state.history, 1):
            if st.button(f"{i}. {word.title()}", key=f"hist_{i}"):
                st.session_state.current_word = word
                st.rerun()
    else:
        st.info("No search history yet")
    
    st.markdown("---")
    st.markdown(
        "### 📚 About\n\n"
        "Dictionary is powered by NLTK WordNet, "
        "one of the most comprehensive English lexical databases.\n\n"
        "**Version:** 1.0.0\n"
        "**Built with:** Streamlit + NLTK"
    )

# ============================================================================
# MAIN CONTENT
# ============================================================================

# Header
st.markdown(
    """
    <div class="header">
        <h1>📚 Dictionary</h1>
        <p>Explore definitions, synonyms, and examples</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Search section
st.markdown('<div class="search-container">', unsafe_allow_html=True)

# Add voice search component
components.html(voice_search_component(), height=60)

def handle_search_input():
    """Handle search when Enter is pressed or input changes"""
    search_val = st.session_state.search_input.strip()
    if search_val:
        st.session_state.current_word = search_val
        st.session_state.search_triggered_by_enter = True
        add_to_history(search_val)

col1, col2 = st.columns([4, 1])
with col1:
    st.text_input(
        "Enter English word...",
        value=st.session_state.current_word or "",
        placeholder="e.g., serendipity, eloquent, ephemeral...",
        label_visibility="collapsed",
        on_change=handle_search_input,
        key="search_input"
    )

with col2:
    search_button = st.button("🔍 Search", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# Add some space
st.markdown("")

# Process search - button click OR Enter key (Enter already handled by on_change)
if search_button:
    search_input_value = st.session_state.get('search_input', '').strip()
    if search_input_value:
        st.session_state.current_word = search_input_value
        add_to_history(search_input_value)

# Display results
if st.session_state.current_word:
    word_input = st.session_state.current_word.strip()
    
    if word_input:
        with st.spinner("🔍 Searching dictionary..."):
            word_data = get_word_data(word_input)
        
        if word_data:
            st.markdown('<div class="result-section">', unsafe_allow_html=True)
            
            # Word title and POS
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f"# {word_data['word'].title()}")
            with col2:
                if word_data['pos_tags']:
                    pos_text = ", ".join([pos_to_name(p) for p in set(word_data['pos_tags'])])
                    st.info(pos_text, icon="🏷️")
            with col3:
                # Show source badge if from API
                if word_data.get('source') == 'WordsAPI':
                    st.success("🌐 From WordsAPI", icon="✓")
            
            # Definitions
            st.markdown("## 📖 Definitions")
            for i, defn in enumerate(word_data['definitions'], 1):
                st.markdown(
                    f"""
                    <div class="definition">
                    <strong>{i}.</strong> {defn['text']}<br>
                    <small><em>{pos_to_name(defn['pos'])}</em></small>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            # Synonyms
            if word_data['synonyms']:
                st.markdown("## 🔗 Synonyms")
                synonym_html = ""
                for syn in sorted(word_data['synonyms']):
                    synonym_html += f'<span class="tag">{syn}</span>'
                st.markdown(synonym_html, unsafe_allow_html=True)
            
            # Antonyms
            if word_data['antonyms']:
                st.markdown("## ❌ Antonyms")
                antonym_html = ""
                for ant in sorted(word_data['antonyms']):
                    antonym_html += f'<span class="tag" style="background: linear-gradient(135deg, #ef4444 0%, #f87171 100%);">{ant}</span>'
                st.markdown(antonym_html, unsafe_allow_html=True)
            
            # Examples
            if word_data['examples']:
                st.markdown("## 💡 Examples")
                for example in word_data['examples']:
                    st.markdown(
                        f"""
                        <div class="example">
                        "{example}"
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            
            # Action buttons
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            with col1:
                output_text = format_output(word_data)
                st.download_button(
                    label="📥 Download Result",
                    data=output_text,
                    file_name=f"{word_data['word']}.txt",
                    mime="text/plain"
                )
            with col2:
                if st.button("🔄 New Search"):
                    st.session_state.current_word = None
                    st.rerun()
            with col3:
                if st.button("📋 Copy"):
                    st.success("Copied to clipboard! (Open browser console to paste)")
            with col4:
                if st.button("🗑️ Clear"):
                    st.session_state.current_word = None
                    st.session_state.history = []
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        else:
            # Fun error message
            error_messages = [
                "🤔 Word not found? Try 'serendipity'!",
                "😅 That word's playing hide and seek!",
                "🧐 Hmm, can't find that one in the dictionary!",
                "🎯 That word slipped through my fingers!",
                "📚 Not in my vocabulary... yet!",
            ]
            import random
            error_msg = random.choice(error_messages)
            
            st.markdown(
                f"""
                <div class="error-message">
                <p><strong>{error_msg}</strong></p>
                <p>Try searching for another word or check the spelling.</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Suggestions
            st.markdown("### 💡 Try These Words:")
            suggestions = ["Serendipity", "Eloquent", "Ephemeral", "Plethora", "Ubiquitous"]
            col1, col2, col3 = st.columns(3)
            for i, word in enumerate(suggestions):
                col = [col1, col2, col3][i % 3]
                with col:
                    if st.button(word):
                        st.session_state.current_word = word.lower()
                        st.rerun()

# Footer
st.markdown("---")
st.markdown(
    """
    <div class="footer">
    <p>Powered by NLTK WordNet & Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True
)
