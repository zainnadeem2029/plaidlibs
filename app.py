"""
PlaidLibs™ - Interactive Storytelling Platform
Main Streamlit Application
Powered by OpenAI Assistants API
"""

import streamlit as st
import os
from dotenv import load_dotenv
from assistant import PlaidLibsAssistant
from config import (
    LITERARY_FORMS, ALL_GENRES, ABSURDITY_LEVELS, 
    QUIP_PERSONAS, WORKFLOW_MODES, PROMPT_TYPES,
    get_system_prompt, get_stage_prompt
)

# Load environment variables
load_dotenv()

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="PlaidLibs™ - Interactive Storytelling",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# CUSTOM CSS
# =============================================================================
st.markdown("""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap');

/* Root Variables */
:root {
    --primary: #7C3AED;
    --primary-light: #A78BFA;
    --primary-dark: #5B21B6;
    --secondary: #06B6D4;
    --accent: #F59E0B;
    --success: #10B981;
    --warning: #F59E0B;
    --error: #EF4444;
    --bg-dark: #0F0F1A;
    --bg-card: #1A1A2E;
    --bg-elevated: #252542;
    --text-primary: #FAFAFA;
    --text-secondary: #A1A1AA;
    --border-color: #3F3F5A;
    --gradient-primary: linear-gradient(135deg, #7C3AED 0%, #06B6D4 100%);
    --gradient-warm: linear-gradient(135deg, #F59E0B 0%, #EF4444 100%);
    --gradient-cool: linear-gradient(135deg, #06B6D4 0%, #10B981 100%);
}

/* Global Styles */
.stApp {
    background: var(--bg-dark);
    font-family: 'Inter', sans-serif;
}

/* Main header */
.main-header {
    background: var(--gradient-primary);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-family: 'Outfit', sans-serif;
    font-weight: 800;
    font-size: 2.5rem;
    text-align: center;
    padding: 1rem 0;
    margin-bottom: 1rem;
}

.sub-header {
    color: var(--text-secondary);
    text-align: center;
    font-size: 1.1rem;
    margin-bottom: 2rem;
}

/* Chat container */
.chat-container {
    background: var(--bg-card);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    border: 1px solid var(--border-color);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

/* Message bubbles */
.user-message {
    background: var(--gradient-primary);
    color: white;
    padding: 1rem 1.5rem;
    border-radius: 20px 20px 4px 20px;
    margin: 0.5rem 0;
    max-width: 80%;
    margin-left: auto;
    font-size: 0.95rem;
    box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
}

.assistant-message {
    background: var(--bg-elevated);
    color: var(--text-primary);
    padding: 1rem 1.5rem;
    border-radius: 20px 20px 20px 4px;
    margin: 0.5rem 0;
    max-width: 85%;
    font-size: 0.95rem;
    border: 1px solid var(--border-color);
    line-height: 1.6;
}

/* Selection cards */
.selection-card {
    background: var(--bg-card);
    border: 2px solid var(--border-color);
    border-radius: 12px;
    padding: 1rem;
    margin: 0.5rem 0;
    cursor: pointer;
    transition: all 0.3s ease;
}

.selection-card:hover {
    border-color: var(--primary);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(124, 58, 237, 0.2);
}

.selection-card.selected {
    border-color: var(--primary);
    background: rgba(124, 58, 237, 0.1);
}

/* Buttons */
.stButton > button {
    background: var(--gradient-primary) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 2rem !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 16px rgba(124, 58, 237, 0.3) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(124, 58, 237, 0.4) !important;
}

/* Secondary button */
.secondary-btn > button {
    background: var(--bg-elevated) !important;
    border: 2px solid var(--border-color) !important;
}

.secondary-btn > button:hover {
    border-color: var(--primary) !important;
}

/* Input fields */
.stTextInput > div > div > input {
    background: var(--bg-elevated) !important;
    border: 2px solid var(--border-color) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    padding: 1rem !important;
    font-size: 1rem !important;
}

.stTextInput > div > div > input:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.2) !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background: var(--bg-elevated) !important;
    border: 2px solid var(--border-color) !important;
    border-radius: 12px !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: var(--bg-card) !important;
    border-right: 1px solid var(--border-color);
}

[data-testid="stSidebar"] .stMarkdown h3 {
    color: var(--primary-light);
    font-family: 'Outfit', sans-serif;
}

/* Progress indicator */
.progress-step {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: var(--bg-elevated);
    border: 2px solid var(--border-color);
    color: var(--text-secondary);
    font-weight: 600;
    margin: 0 0.25rem;
    transition: all 0.3s ease;
}

.progress-step.active {
    background: var(--gradient-primary);
    border-color: transparent;
    color: white;
}

.progress-step.completed {
    background: var(--success);
    border-color: transparent;
    color: white;
}

/* Mode badge */
.mode-badge {
    display: inline-flex;
    align-items: center;
    background: rgba(124, 58, 237, 0.2);
    color: var(--primary-light);
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-size: 0.875rem;
    font-weight: 600;
    margin-bottom: 1rem;
}

/* Quip avatar */
.quip-avatar {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: var(--gradient-primary);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    margin-right: 1rem;
}

/* Story output */
.story-output {
    background: linear-gradient(135deg, rgba(124, 58, 237, 0.1) 0%, rgba(6, 182, 212, 0.1) 100%);
    border: 2px solid var(--primary);
    border-radius: 16px;
    padding: 2rem;
    margin: 1rem 0;
    font-size: 1.1rem;
    line-height: 1.8;
}

/* Spinner */
.loading-spinner {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: var(--text-secondary);
    padding: 1rem;
}

/* Divider */
.custom-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border-color), transparent);
    margin: 1.5rem 0;
}

/* Animation */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.animate-in {
    animation: fadeIn 0.3s ease-out forwards;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: var(--bg-dark);
}

::-webkit-scrollbar-thumb {
    background: var(--border-color);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--primary);
}

/* Hide streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Word cloud styling */
.word-tag {
    display: inline-block;
    background: var(--bg-elevated);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 0.25rem 0.75rem;
    margin: 0.25rem;
    font-size: 0.875rem;
    color: var(--primary-light);
}

/* Confirmation box */
.confirm-box {
    background: rgba(16, 185, 129, 0.1);
    border: 2px solid var(--success);
    border-radius: 12px;
    padding: 1rem;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# =============================================================================
# SESSION STATE INITIALIZATION
# =============================================================================
def init_session_state():
    """Initialize all session state variables."""
    defaults = {
        "messages": [],
        "current_mode": "lib_ate",
        "current_quip": "macquip",
        "current_stage": "welcome",
        "selected_style": None,
        "selected_genre": None,
        "selected_absurdity": None,
        "collected_prompts": [],
        "prompt_index": 0,
        "total_prompts": 6,
        "story_generated": False,
        "thread_id": None,
        "assistant": None
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_workflow():
    """Reset the current workflow state."""
    st.session_state.current_stage = "welcome"
    st.session_state.selected_style = None
    st.session_state.selected_genre = None
    st.session_state.selected_absurdity = None
    st.session_state.collected_prompts = []
    st.session_state.prompt_index = 0
    st.session_state.story_generated = False
    st.session_state.messages = []
    
    # Reset assistant thread
    if st.session_state.assistant:
        st.session_state.assistant.reset_conversation()
        st.session_state.thread_id = st.session_state.assistant.thread_id


def get_assistant():
    """Get or create the PlaidLibs assistant instance."""
    if st.session_state.assistant is None:
        st.session_state.assistant = PlaidLibsAssistant()
        if st.session_state.thread_id:
            st.session_state.assistant.set_thread(st.session_state.thread_id)
    return st.session_state.assistant


# =============================================================================
# UI COMPONENTS
# =============================================================================
def render_sidebar():
    """Render the sidebar with workflow selection and settings."""
    with st.sidebar:
        st.markdown("### 🧵 PlaidLibs™")
        st.markdown("---")
        
        # Workflow selector
        st.markdown("#### Choose Workflow")
        mode_options = {k: f"{v['icon']} {v['name']}" for k, v in WORKFLOW_MODES.items()}
        selected_mode = st.selectbox(
            "Workflow Mode",
            options=list(mode_options.keys()),
            format_func=lambda x: mode_options[x],
            key="mode_selector",
            label_visibility="collapsed"
        )
        
        if selected_mode != st.session_state.current_mode:
            st.session_state.current_mode = selected_mode
            reset_workflow()
        
        st.markdown("---")
        
        # Quip selector
        st.markdown("#### Narrator / Host (Quip)")
        quip_options = {k: f"{v['icon']} {v['name']}" for k, v in QUIP_PERSONAS.items()}
        selected_quip = st.selectbox(
            "Select Quip",
            options=list(quip_options.keys()),
            format_func=lambda x: quip_options[x],
            key="quip_selector",
            label_visibility="collapsed"
        )
        
        if selected_quip != st.session_state.current_quip:
            st.session_state.current_quip = selected_quip
            # Note: In production, you'd update the assistant instructions here
        
        # Show current Quip info
        current_quip = QUIP_PERSONAS[selected_quip]
        st.markdown(f"""
        <div style="background: rgba(124, 58, 237, 0.1); border-radius: 12px; padding: 1rem; margin-top: 0.5rem;">
            <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">{current_quip['icon']}</div>
            <div style="font-size: 0.75rem; color: #A78BFA;">{current_quip['epithet']}</div>
            <div style="font-size: 0.8rem; color: #A1A1AA; margin-top: 0.5rem;">{current_quip['description']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Reset button
        if st.button("🔄 Reset This Mode", use_container_width=True):
            reset_workflow()
            st.rerun()
        
        # Progress indicator (for Lib-Ate mode)
        if st.session_state.current_mode == "lib_ate":
            st.markdown("---")
            st.markdown("#### Progress")
            stages = ["Style", "Genre", "Absurdity", "Prompts", "Story"]
            current_idx = {
                "welcome": -1,
                "style": 0,
                "genre": 1,
                "absurdity": 2,
                "prompts": 3,
                "story": 4
            }.get(st.session_state.current_stage, -1)
            
            progress_html = '<div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 4px;">'
            for i, stage in enumerate(stages):
                if i < current_idx:
                    cls = "completed"
                    icon = "✓"
                elif i == current_idx:
                    cls = "active"
                    icon = str(i + 1)
                else:
                    cls = ""
                    icon = str(i + 1)
                progress_html += f'<div class="progress-step {cls}">{icon}</div>'
            progress_html += '</div>'
            st.markdown(progress_html, unsafe_allow_html=True)
            
            # Show current selections
            if st.session_state.selected_style:
                st.markdown(f"✅ **Style:** {st.session_state.selected_style}")
            if st.session_state.selected_genre:
                st.markdown(f"✅ **Genre:** {st.session_state.selected_genre}")
            if st.session_state.selected_absurdity:
                st.markdown(f"✅ **Absurdity:** {st.session_state.selected_absurdity}")
            if st.session_state.collected_prompts:
                st.markdown(f"📝 **Words:** {len(st.session_state.collected_prompts)}/{st.session_state.total_prompts}")


def render_welcome():
    """Render the welcome screen."""
    quip = QUIP_PERSONAS[st.session_state.current_quip]
    mode = WORKFLOW_MODES[st.session_state.current_mode]
    
    st.markdown(f"""
    <div class="chat-container animate-in">
        <div style="display: flex; align-items: flex-start;">
            <div class="quip-avatar">{quip['icon']}</div>
            <div>
                <div style="font-weight: 600; color: #A78BFA; margin-bottom: 0.5rem;">{quip['name']}</div>
                <div class="assistant-message" style="margin: 0; max-width: 100%;">
                    <p>🎭 <strong>Welcome to PlaidLibs™!</strong></p>
                    <p>I'm {quip['name']}, {quip['epithet'].lower()}. Today we'll be creating something magical using the <strong>{mode['name']}</strong> workflow.</p>
                    <p>Ready to craft a story together? Let's begin!</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Let's Start!", use_container_width=True):
        st.session_state.current_stage = "style"
        st.rerun()


def render_style_selection():
    """Render the style selection screen."""
    quip = QUIP_PERSONAS[st.session_state.current_quip]
    
    st.markdown(f"""
    <div class="mode-badge">{quip['icon']} {quip['name']} • Step 1: Literary Style</div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="assistant-message animate-in">
        <p>🎭 <strong>Let's begin your PlaidLibs™ adventure!</strong></p>
        <p>First, choose your <strong>Literary Style</strong> — this determines the structure and rhythm of your story.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Style selection grid
    cols = st.columns(3)
    for i, (key, style) in enumerate(LITERARY_FORMS.items()):
        with cols[i % 3]:
            if st.button(
                f"{style['icon']} {style['name']}\n\n{style['description']}",
                key=f"style_{key}",
                use_container_width=True
            ):
                st.session_state.selected_style = style['name']
                st.session_state.total_prompts = style['prompt_count']
                st.session_state.current_stage = "genre"
                st.rerun()


def render_genre_selection():
    """Render the genre selection screen."""
    quip = QUIP_PERSONAS[st.session_state.current_quip]
    
    st.markdown(f"""
    <div class="mode-badge">{quip['icon']} {quip['name']} • Step 2: Genre</div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="confirm-box animate-in">
        ✅ <strong>Selected Style:</strong> {st.session_state.selected_style}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="assistant-message">
        <p>🎬 <strong>Excellent choice!</strong> Now, let's pick your <strong>Genre</strong> — this sets the atmosphere and promise of your story.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Genre tabs
    tab1, tab2, tab3 = st.tabs(["🎬 Core Genres", "🌀 Flexible Genres", "🧵 PlaidVerse™"])
    
    with tab1:
        cols = st.columns(3)
        core_genres = {k: v for k, v in ALL_GENRES.items() if k in ["adventure", "comedy", "drama", "fantasy", "historical", "horror", "mystery", "romance", "sci_fi", "thriller"]}
        for i, (key, genre) in enumerate(core_genres.items()):
            with cols[i % 3]:
                if st.button(f"{genre['icon']} {genre['name']}", key=f"genre_{key}", use_container_width=True, help=genre['description']):
                    st.session_state.selected_genre = genre['name']
                    st.session_state.current_stage = "absurdity"
                    st.rerun()
    
    with tab2:
        cols = st.columns(3)
        flex_genres = {k: v for k, v in ALL_GENRES.items() if k in ["absurdist", "satire", "slice_of_life", "surreal", "parody"]}
        for i, (key, genre) in enumerate(flex_genres.items()):
            with cols[i % 3]:
                if st.button(f"{genre['icon']} {genre['name']}", key=f"genre_{key}", use_container_width=True, help=genre['description']):
                    st.session_state.selected_genre = genre['name']
                    st.session_state.current_stage = "absurdity"
                    st.rerun()
    
    with tab3:
        cols = st.columns(3)
        plaid_genres = {k: v for k, v in ALL_GENRES.items() if k in ["plaidpunk", "interplaidactic", "courtroom_chaos", "epic_quest", "wild_card"]}
        for i, (key, genre) in enumerate(plaid_genres.items()):
            with cols[i % 3]:
                if st.button(f"{genre['icon']} {genre['name']}", key=f"genre_{key}", use_container_width=True, help=genre['description']):
                    st.session_state.selected_genre = genre['name']
                    st.session_state.current_stage = "absurdity"
                    st.rerun()


def render_absurdity_selection():
    """Render the absurdity level selection screen."""
    quip = QUIP_PERSONAS[st.session_state.current_quip]
    
    st.markdown(f"""
    <div class="mode-badge">{quip['icon']} {quip['name']} • Step 3: Absurdity Level</div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="confirm-box">
        ✅ <strong>Style:</strong> {st.session_state.selected_style} &nbsp;|&nbsp;
        ✅ <strong>Genre:</strong> {st.session_state.selected_genre}
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="assistant-message">
        <p>🌪️ <strong>Now for the fun part!</strong> How <em>weird</em> do you want this to get?</p>
        <p>Choose your <strong>Absurdity Level</strong> — this controls how much reality bends in your story.</p>
    </div>
    """, unsafe_allow_html=True)
    
    cols = st.columns(5)
    for i, (key, level) in enumerate(ABSURDITY_LEVELS.items()):
        with cols[i]:
            if st.button(
                f"{level['icon']}\n\n{level['name']}\n\n{level['description']}",
                key=f"absurdity_{key}",
                use_container_width=True
            ):
                st.session_state.selected_absurdity = level['name']
                st.session_state.current_stage = "prompts"
                st.rerun()


def render_prompt_collection():
    """Render the Mad Libs-style prompt collection screen."""
    quip = QUIP_PERSONAS[st.session_state.current_quip]
    prompt_idx = st.session_state.prompt_index
    total = st.session_state.total_prompts
    
    st.markdown(f"""
    <div class="mode-badge">{quip['icon']} {quip['name']} • Step 4: Word Collection</div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="confirm-box">
        ✅ <strong>Style:</strong> {st.session_state.selected_style} &nbsp;|&nbsp;
        ✅ <strong>Genre:</strong> {st.session_state.selected_genre} &nbsp;|&nbsp;
        ✅ <strong>Absurdity:</strong> {st.session_state.selected_absurdity}
    </div>
    """, unsafe_allow_html=True)
    
    # Show collected words so far
    if st.session_state.collected_prompts:
        words_html = '<div style="margin: 1rem 0;">'
        for word in st.session_state.collected_prompts:
            words_html += f'<span class="word-tag">{word}</span>'
        words_html += '</div>'
        st.markdown(words_html, unsafe_allow_html=True)
    
    if prompt_idx < total:
        # Get current prompt type
        prompt_type = PROMPT_TYPES[prompt_idx % len(PROMPT_TYPES)]
        
        st.markdown(f"""
        <div class="assistant-message animate-in">
            <p>📝 <strong>Prompt {prompt_idx + 1} of {total}</strong></p>
            <p>Give me a <strong>{prompt_type['label']}</strong>!</p>
            <p style="color: #A1A1AA; font-size: 0.85rem;">Examples: {prompt_type['example']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([4, 1])
        with col1:
            user_input = st.text_input(
                f"Enter a {prompt_type['label']}",
                key=f"prompt_input_{prompt_idx}",
                placeholder=f"Type a {prompt_type['label'].lower()}...",
                label_visibility="collapsed"
            )
        with col2:
            if st.button("Submit", key=f"submit_{prompt_idx}", use_container_width=True):
                if user_input.strip():
                    st.session_state.collected_prompts.append(user_input.strip())
                    st.session_state.prompt_index += 1
                    st.rerun()
                else:
                    st.warning("Please enter a word!")
    else:
        st.markdown(f"""
        <div class="assistant-message">
            <p>🎉 <strong>All prompts collected!</strong></p>
            <p>You've given me these wonderful ingredients:</p>
        </div>
        """, unsafe_allow_html=True)
        
        words_html = '<div style="margin: 1rem 0; padding: 1rem; background: rgba(124, 58, 237, 0.1); border-radius: 12px;">'
        for i, word in enumerate(st.session_state.collected_prompts):
            words_html += f'<span class="word-tag">{PROMPT_TYPES[i % len(PROMPT_TYPES)]["label"]}: {word}</span>'
        words_html += '</div>'
        st.markdown(words_html, unsafe_allow_html=True)
        
        if st.button("✨ Generate My Story!", use_container_width=True):
            st.session_state.current_stage = "story"
            st.rerun()


def render_story_generation():
    """Render the story generation screen with AI integration."""
    quip = QUIP_PERSONAS[st.session_state.current_quip]
    
    st.markdown(f"""
    <div class="mode-badge">{quip['icon']} {quip['name']} • Step 5: Your Story</div>
    """, unsafe_allow_html=True)
    
    # Prepare the story generation prompt
    prompt_pairs = []
    for i, word in enumerate(st.session_state.collected_prompts):
        prompt_type = PROMPT_TYPES[i % len(PROMPT_TYPES)]
        prompt_pairs.append(f"{prompt_type['label']}: {word}")
    
    generation_prompt = f"""
Generate a {st.session_state.selected_style} story in the {st.session_state.selected_genre} genre.

**Absurdity Level:** {st.session_state.selected_absurdity}

**Words to incorporate:**
{chr(10).join(prompt_pairs)}

Remember to:
1. Use the {st.session_state.selected_style} literary form structure
2. Make it clearly read as {st.session_state.selected_genre}
3. Match the {st.session_state.selected_absurdity} absurdity level
4. Naturally incorporate ALL the provided words
5. Be creative, engaging, and entertaining!
"""
    
    if not st.session_state.story_generated:
        with st.spinner("🪄 Weaving your story..."):
            try:
                assistant = get_assistant()
                
                # Send the initial context with system prompt
                if not st.session_state.thread_id:
                    assistant.get_or_create_thread()
                    st.session_state.thread_id = assistant.thread_id
                    
                    # Send system context
                    system_context = get_system_prompt(st.session_state.current_quip)
                    assistant.send_message(f"[SYSTEM CONTEXT]\n{system_context}\n\nPlease acknowledge you understand and are ready to generate stories.")
                
                # Generate the story
                response = assistant.send_message(generation_prompt)
                st.session_state.generated_story = response
                st.session_state.story_generated = True
                st.rerun()
                
            except Exception as e:
                st.error(f"Oops! Something went wrong: {str(e)}")
                st.info("Please check your OpenAI API key and Assistant ID in the .env file.")
                return
    
    # Display the generated story
    if hasattr(st.session_state, 'generated_story'):
        st.markdown(f"""
        <div class="story-output animate-in">
            <div style="font-size: 1.5rem; margin-bottom: 1rem; text-align: center;">
                📖 Your {st.session_state.selected_style}
            </div>
            {st.session_state.generated_story}
        </div>
        """, unsafe_allow_html=True)
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 Generate Another", use_container_width=True):
                st.session_state.story_generated = False
                st.rerun()
        with col2:
            if st.button("📝 New Story", use_container_width=True):
                reset_workflow()
                st.rerun()
        with col3:
            st.download_button(
                "💾 Download",
                st.session_state.generated_story,
                file_name="plaidlibs_story.txt",
                mime="text/plain",
                use_container_width=True
            )


def render_chat_mode():
    """Render the free-form chat mode (PlaidChat)."""
    quip = QUIP_PERSONAS[st.session_state.current_quip]
    
    st.markdown(f"""
    <div class="mode-badge">{quip['icon']} {quip['name']} • PlaidChat</div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="assistant-message">
        <p>💬 <strong>Welcome to PlaidChat!</strong></p>
        <p>I'm {quip['name']}, ready to chat about anything creative. Ask me to brainstorm, remix ideas, or just have a plaid-tastic conversation!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display message history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="user-message">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="assistant-message">{msg["content"]}</div>', unsafe_allow_html=True)
    
    # Chat input
    user_input = st.chat_input("Type your message...")
    
    if user_input:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Get assistant response
        try:
            assistant = get_assistant()
            response = assistant.send_message(user_input)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.session_state.messages.append({"role": "assistant", "content": f"Oops! I encountered an issue: {str(e)}"})
        
        st.rerun()


# =============================================================================
# MAIN APPLICATION
# =============================================================================
def main():
    """Main application entry point."""
    init_session_state()
    render_sidebar()
    
    # Main content area
    st.markdown('<h1 class="main-header">🧵 PlaidLibs™</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Interactive Storytelling Powered by AI</p>', unsafe_allow_html=True)
    
    # Check for API configuration
    if not os.getenv("OPENAI_API_KEY") or not os.getenv("OPENAI_ASSISTANT_ID"):
        st.warning("""
        ⚠️ **Configuration Required**
        
        Please set up your OpenAI credentials:
        1. Copy `.env.example` to `.env`
        2. Add your `OPENAI_API_KEY`
        3. Add your `OPENAI_ASSISTANT_ID`
        
        Need to create an assistant? Use the setup script or OpenAI's Playground.
        """)
        
        # Show setup instructions
        with st.expander("📋 Setup Instructions"):
            st.markdown("""
            ### Quick Setup Guide
            
            1. **Get an OpenAI API Key:**
               - Go to [OpenAI Platform](https://platform.openai.com)
               - Navigate to API Keys
               - Create a new key
            
            2. **Create an Assistant:**
               - Go to [OpenAI Assistants](https://platform.openai.com/assistants)
               - Click "Create"
               - Use the system prompt from our documentation
               - Copy the Assistant ID
            
            3. **Configure the App:**
               - Create a `.env` file in the project root
               - Add your credentials:
               ```
               OPENAI_API_KEY=sk-your-key-here
               OPENAI_ASSISTANT_ID=asst_your-id-here
               ```
            
            4. **Restart the App**
            """)
        return
    
    # Render appropriate content based on mode and stage
    current_mode = st.session_state.current_mode
    current_stage = st.session_state.current_stage
    
    if current_mode == "plaid_chat":
        render_chat_mode()
    elif current_mode == "lib_ate":
        if current_stage == "welcome":
            render_welcome()
        elif current_stage == "style":
            render_style_selection()
        elif current_stage == "genre":
            render_genre_selection()
        elif current_stage == "absurdity":
            render_absurdity_selection()
        elif current_stage == "prompts":
            render_prompt_collection()
        elif current_stage == "story":
            render_story_generation()
    else:
        # Other modes - show coming soon
        st.info(f"🚧 **{WORKFLOW_MODES[current_mode]['name']}** mode is coming soon!")
        if st.button("Try Lib-Ate Mode Instead"):
            st.session_state.current_mode = "lib_ate"
            reset_workflow()
            st.rerun()


if __name__ == "__main__":
    main()
