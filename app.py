"""
PlaidLibs™ - Interactive Storytelling Platform
Main Streamlit Application
Powered by OpenAI Assistants API
"""

import streamlit as st
import os
import json
from dotenv import load_dotenv
from assistant import PlaidLibsAssistant
from config import (
    LITERARY_FORMS, ALL_GENRES, ABSURDITY_LEVELS, 
    QUIP_PERSONAS, WORKFLOW_MODES, PROMPT_TYPES,
    CORE_GENRES, FLEXIBLE_GENRES, PLAIDVERSE_GENRES,
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
        "assistant": None,
        "enable_image_generation": True,  # Enable DALL-E image generation
        "generated_images": []  # Store generated images
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
    
    # Clear Lib-Ate specific state to prevent reshuffle/persistence bugs
    lib_ate_keys = [
        "lib_ate_state", "lib_ate_messages", "lib_ate_selections", 
        "lib_ate_style_options", "lib_ate_inputs", "lib_ate_data", 
        "lib_ate_story_revealed", "lib_ate_current_input_idx"
    ]
    for key in lib_ate_keys:
        if key in st.session_state:
            del st.session_state[key]
    
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
            index=list(mode_options.keys()).index(st.session_state.current_mode) if st.session_state.current_mode in mode_options else 0,
            key="mode_selector",
            label_visibility="collapsed"
        )
        
        if selected_mode != st.session_state.current_mode:
            st.session_state.current_mode = selected_mode
            reset_workflow()
            st.rerun()
        
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
        
        # Image Generation Toggle
        st.markdown("#### 🎨 Image Generation")
        enable_images = st.toggle(
            "Enable DALL-E Images",
            value=st.session_state.get("enable_image_generation", True),
            key="image_gen_toggle",
            help="Generate AI images for your stories using DALL-E 3"
        )
        if enable_images != st.session_state.get("enable_image_generation", True):
            st.session_state.enable_image_generation = enable_images
        
        if enable_images:
            st.markdown('<div style="background: rgba(16, 185, 129, 0.1); border-radius: 8px; padding: 0.5rem; font-size: 0.8rem; color: #10B981;">✨ Images will be generated with your stories</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Reset button
        if st.button("🔄 Reset This Mode", use_container_width=True):
            reset_workflow()
            st.rerun()
        
        # Progress indicator (for Lib-Ate mode)
        if st.session_state.current_mode == "lib_ate" and st.session_state.get("lib_ate_state") is None:
            # Only show this legacy progress bar if we aren't in the new chat mode
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
    <div class="mode-badge">{quip['icon']} {quip['name']} - Step 1: Literary Style</div>
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
    <div class="mode-badge">{quip['icon']} {quip['name']} - Step 2: Genre</div>
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
    <div class="mode-badge">{quip['icon']} {quip['name']} - Step 3: Absurdity Level</div>
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
    <div class="mode-badge">{quip['icon']} {quip['name']} - Step 4: Word Collection</div>
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
    <div class="mode-badge">{quip['icon']} {quip['name']} - Step 5: Your Story</div>
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

"""
    
    # Add specific formatting instructions
    style_lower = st.session_state.selected_style.lower()
    if style_lower == "listicle":
        generation_prompt += """
**LISTICLE FORMATTING RULES:**
1. Format AS A NUMBERED LIST (1., 2., 3...).
2. Each item must be a STAND-ALONE, independent point. Do not make them a continuous narrative.
3. Apply COMEDIC ESCALATION: Each point should be progressively more absurd or hilarious than the last. Do not repeat the same punchlines or variables without a twist.
4. EMOJI PLACEMENT: Place emojis ONLY at the very end of sentences/points. Never place them inside or immediately following a verb in a way that breaks sentence flow.
"""
    elif style_lower == "ballads":
        generation_prompt += f"""
**BALLAD REQUIREMENTS:**
1. Format as a poem with distinct stanzas (verses) and a consistent rhyme scheme.
2. TONE: Since you are in {quip['name']} persona, maintain a consistently sarcastic, ironic, or mocking tone throughout the narration, not just by using the word 'sarcastic'.
3. CHARACTER INTEGRATION: Ensure the characters (especially the 'Animal' if specified) are active, central participants in the drama with a clear role.
4. WEAPON/PROP INTEGRATION: If a weapon or specific object is present, build narrative tension around its appearance and use organically.
"""
    elif style_lower == "vignettes":
         generation_prompt += """
**VIGNETTE REFINEMENTS:**
1. SEMANTIC GROUNDING: If the 'Place' variable is an adjective (e.g., 'Mysterious'), you MUST append an anchor noun (e.g., 'The Mysterious Valley' or 'The Mysterious Spire') to ground the location. Same applies to 'Action' or 'Verb', do not force a noun to be a verb or vice-versa.
2. VARIABLE ALIGNMENT: Use all variables in their natural grammatical form. For example, 'Awe' should be treated as an emotion or feeling, not forced into a verb like 'began to awe'. Make sure verb tenses make logical sense with their direct objects.
3. AVOID REPETITION: Do not use the same emotional descriptors or nouns repeatedly. Vary your vocabulary for impact.
"""
    elif style_lower == "microfiction":
         generation_prompt += """
**MICROFICTION REFINEMENTS:**
1. NARRATIVE COHERENCE: Ensure clear verb-object pairings. For instance, do not say "Lanterns whispered a warlord." Make actions logical within the absurd context.
2. SETTING CONSISTENCY: Keep the setting visually consistent in the text. Do not jump erratically between disconnected biomes without reason. 
3. STAKES: The ending twist or consequence must match the tone of the genre and make contextual sense.
"""

    generation_prompt += """
Remember to:
1. Use the {st.session_state.selected_style} literary form structure STRICTLY
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
                
                # Generate image if enabled
                if st.session_state.get("enable_image_generation", True):
                    with st.spinner("🎨 Creating illustration..."):
                        # Create an image prompt based on the story
                        # Extract the first ~300 chars of the generated text to ground the image prompt in the narrative
                        story_snippet = st.session_state.generated_story[:300].replace('\n', ' ')
                        image_prompt = f"A vivid, artistic illustration for a {st.session_state.selected_genre} {st.session_state.selected_style}. Setting and Action Context: '{story_snippet}'. Style: colorful, {st.session_state.selected_absurdity.lower()} whimsy, cinematic lighting, storybook quality. Theme incorporates: {', '.join(st.session_state.collected_prompts)}. No text or words in the image."
                        image_result = assistant.generate_image(image_prompt, style="vivid")
                        if "url" in image_result:
                            st.session_state.story_image = image_result["url"]
                        else:
                            st.session_state.story_image = None
                
                st.rerun()
                
            except Exception as e:
                st.error(f"Oops! Something went wrong: {str(e)}")
                st.info("Please check your OpenAI API key and Assistant ID in the .env file.")
                return
    
    # Display the generated story
    if hasattr(st.session_state, 'generated_story'):
        # Display image if available
        if hasattr(st.session_state, 'story_image') and st.session_state.story_image:
            st.image(st.session_state.story_image, caption="🎨 AI-Generated Illustration", use_container_width=True)
        
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
                if hasattr(st.session_state, 'story_image'):
                    del st.session_state.story_image
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


def render_lib_ate():
    """Render the Lib-Ate mode - Chat-based Hidden Story Game."""
    quip = QUIP_PERSONAS[st.session_state.current_quip]
    
    # Initialize Lib-Ate specific state
    if "lib_ate_state" not in st.session_state:
        st.session_state.lib_ate_state = "select_style"
        st.session_state.lib_ate_messages = []
        st.session_state.lib_ate_selections = {}
        st.session_state.lib_ate_style_options = None  # Will store randomly selected styles
        
        # Add welcome message with 5 random literary options + Wild Card + Reshuffle
        import random
        # Get all styles except wild_card for random selection
        available_styles = {k: v for k, v in LITERARY_FORMS.items() if k != "wild_card"}
        # Randomly select 5 styles
        selected_keys = random.sample(list(available_styles.keys()), min(5, len(available_styles)))
        selected_styles = {k: available_styles[k] for k in selected_keys}
        st.session_state.lib_ate_style_options = selected_styles
        
        style_list = "\n".join([f"{i+1}. {s['name']} - {s['description']}" for i, (k, s) in enumerate(selected_styles.items())])
        welcome_msg = f"""**Welcome to Lib-Ate™!** 📜

I'm {quip['name']}, and I need your help to weave a secret tale.

First, **choose your literary style**:

{style_list}
{len(selected_styles) + 1}. Wild Card
{len(selected_styles) + 2}. Reshuffle

👉 You can type a number, 'wild', 'reshuffle', or part of a style name."""
        st.session_state.lib_ate_messages.append({"role": "assistant", "content": welcome_msg})

    st.markdown(f"""
    <div class="mode-badge">{quip['icon']} {quip['name']} - Lib-Ate</div>
    """, unsafe_allow_html=True)

    # Display chat history
    for msg in st.session_state.lib_ate_messages:
        role_class = "user-message" if msg["role"] == "user" else "assistant-message"
        st.markdown(f'<div class="{role_class}">{msg["content"]}</div>', unsafe_allow_html=True)
    
    # Handle user input
    user_input = st.chat_input("Your choice...", key="lib_ate_chat")
    
    if user_input:
        # Add user message to state
        st.session_state.lib_ate_messages.append({"role": "user", "content": user_input})
        
        # Process input based on state
        state = st.session_state.lib_ate_state
        assistant = get_assistant()
        
        # Helper to find selection from list
        def find_selection(user_val, options_dict, allow_wild=True):
            user_val = user_val.lower().strip()
            if allow_wild and ("wild" in user_val or "surprise" in user_val):
                import random
                return random.choice(list(options_dict.values()))
            
            # Check for number
            if user_val.isdigit():
                idx = int(user_val) - 1
                if 0 <= idx < len(options_dict):
                    return list(options_dict.values())[idx]
            
            # Check for name match
            for val in options_dict.values():
                if user_val in val['name'].lower():
                    return val
            return None

        if state == "select_style":
            user_val = user_input.lower().strip()
            
            # Check for reshuffle
            if "reshuffle" in user_val or user_val == str(len(st.session_state.lib_ate_style_options) + 2):
                # Regenerate 5 random styles
                import random
                available_styles = {k: v for k, v in LITERARY_FORMS.items() if k != "wild_card"}
                selected_keys = random.sample(list(available_styles.keys()), min(5, len(available_styles)))
                selected_styles = {k: available_styles[k] for k in selected_keys}
                st.session_state.lib_ate_style_options = selected_styles
                
                style_list = "\n".join([f"{i+1}. {s['name']} - {s['description']}" for i, (k, s) in enumerate(selected_styles.items())])
                reshuffle_msg = f"""🔄 **Reshuffled!** Here are 5 new literary styles:

{style_list}
{len(selected_styles) + 1}. Wild Card
{len(selected_styles) + 2}. Reshuffle

👉 You can type a number, 'wild', 'reshuffle', or part of a style name."""
                st.session_state.lib_ate_messages.append({"role": "assistant", "content": reshuffle_msg})
                return
            
            # Use the stored random style options for selection
            style_options = st.session_state.lib_ate_style_options or LITERARY_FORMS
            selection = find_selection(user_input, style_options)
            if selection:
                st.session_state.lib_ate_selections["style"] = selection['name']
                st.session_state.lib_ate_state = "select_genre"
                
                # Prepare Genre Options
                # Grouping for display
                core_list = [f"{i+1}. {g['name']}" for i, (k, g) in enumerate(CORE_GENRES.items())]
                flex_list = [f"{i+1+10}. {g['name']}" for i, (k, g) in enumerate(FLEXIBLE_GENRES.items())] # Offset indices purely for display differentiation if we wanted, but let's keep it simple
                
                # Actually, let's just show a curated list or all of them. The mockups show categories.
                # We'll Flatten for simple selection logic but display nicely
                
                # Prepare lists for display
                core_list_str = "\n".join([f"{i+1}. {g['name']}" for i, (k,g) in enumerate(CORE_GENRES.items())])
                
                # Flexible genres start numbering after core genres
                start_idx = len(CORE_GENRES) + 1
                flex_list_str = "\n".join([f"{i+start_idx}. {g['name']}" for i, (k,g) in enumerate({**FLEXIBLE_GENRES, **PLAIDVERSE_GENRES}.items())])
                
                genre_msg = f"""✅ **Selected Style:** {selection['name']} - {selection['description']}

Excellent choice! Now, **choose your genre**:

**🎬 Core Genres**
{core_list_str}

**🌀 Flexible & PlaidVerse™**
{flex_list_str}

{len(ALL_GENRES) + 1}. Wild Card

👉 Type the number or name."""
                st.session_state.lib_ate_messages.append({"role": "assistant", "content": genre_msg})
            else:
                 st.session_state.lib_ate_messages.append({"role": "assistant", "content": "I didn't catch that. Please type a valid number or style name!"})

        elif state == "select_genre":
            selection = find_selection(user_input, ALL_GENRES)
            if selection:
                st.session_state.lib_ate_selections["genre"] = selection['name']
                st.session_state.lib_ate_state = "select_absurdity"
                
                absurdity_msg = f"""✅ **Genre:** {selection['name']}

Finally, set the **absurdity level**:

1. Mild - Just a sprinkle of silly 🌿
2. Moderate - Comfortably ridiculous 🌊
3. Spicy - Playful chaos 🌶️
4. Chaotic - Logic optional 🌪️
5. Plaidemonium™ - Laws of physics need not apply 💥
6. Wild Card - Let fate decide! 🃏

Type your choice (1-6 or text)."""
                st.session_state.lib_ate_messages.append({"role": "assistant", "content": absurdity_msg})
            else:
                st.session_state.lib_ate_messages.append({"role": "assistant", "content": "Please choose a valid genre from the list!"})

        elif state == "select_absurdity":
            selection = find_selection(user_input, ABSURDITY_LEVELS)
            if selection:
                st.session_state.lib_ate_selections["absurdity"] = selection['name']
                st.session_state.lib_ate_state = "generating_template"
                st.rerun() # Force rerun to start generation immediately
            else:
                st.session_state.lib_ate_messages.append({"role": "assistant", "content": "Please pick a valid absurdity level (1-6)."})

        elif state == "collecting":
            # Store the previous input
            current_idx = st.session_state.lib_ate_current_input_idx
            required = st.session_state.lib_ate_data["required_inputs"]
            
            # handle "surprise me" logic for input values
            val = user_input
            if "surprise" in val.lower() or "random" in val.lower():
                val = "[Auto-filled by AI]" 
                # Note: We'll let the AI generate it during final assembly or we could ask for it now.
                # Simplest is to pass "Wild Card" as the value and let the final prompt handle it.
                val = "Wild Card (Surprise Me)"
            
            st.session_state.lib_ate_inputs.append(val)
            
            # Check if we need more
            if current_idx + 1 < len(required):
                st.session_state.lib_ate_current_input_idx += 1
                next_req = required[st.session_state.lib_ate_current_input_idx]
                
                # Format: "Prompt X of Y: TYPE"
                # If the AI provided hidden examples/descriptions, we could use them.
                # The data structure has "required_inputs" as a list of strings usually (e.g. "Adjective").
                # If it's a dict or richer object, we'd parse it. Assuming strings for now.
                
                response_msg = f"**Prompt {st.session_state.lib_ate_current_input_idx + 1} of {len(required)}**\n\nGive me a: **{next_req}**"
                st.session_state.lib_ate_messages.append({"role": "assistant", "content": response_msg})
            else:
                # All collected
                st.session_state.lib_ate_state = "review"
                
                # Build Summary
                selections = st.session_state.lib_ate_selections
                inputs_summary = ", ".join([f"'{req}': '{val}'" for req, val in zip(required, st.session_state.lib_ate_inputs)])
                
                summary_msg = f"""**Here's your setup:**
                
📜 **Style:** {selections['style']}
🎬 **Genre:** {selections['genre']}
🤪 **Absurdity:** {selections['absurdity']}

🔑 **Variables:**
{{ {inputs_summary} }}

Type **YES** to reveal the story, or **NO** to restart."""
                st.session_state.lib_ate_messages.append({"role": "assistant", "content": summary_msg})
        
        elif state == "review":
            if "yes" in user_input.lower() or "reveal" in user_input.lower():
                st.session_state.lib_ate_state = "reveal"
                st.rerun()
            else:
                # Restart logic
                st.session_state.lib_ate_state = "select_style"
                st.session_state.lib_ate_messages = []
                st.rerun()

        elif state == "reveal":
             pass # Handled below

        st.rerun()

    # Handle "generating_template" state (Automatic transition)
    if st.session_state.lib_ate_state == "generating_template":
        with st.spinner("🤫 Cooking up a secret story template..."):
            assistant = get_assistant()
            selections = st.session_state.lib_ate_selections
            
            prompt = f"""
            Create a HIDDEN Mad Libs style story.
            
            Style: {selections['style']}
            Genre: {selections['genre']}
            Absurdity Level: {selections['absurdity']}

            Format Instructions:
            """
            
            if selections['style'].lower() == "listicle":
                prompt += """
**LISTICLE FORMATTING RULES:**
1. MUST be a numbered list (1., 2., 3...).
2. Each item must be a STAND-ALONE, independent point. Do not write a continuous paragraph.
3. Apply COMEDIC ESCALATION: Each point should be funnier than the last. Do not repeat variables heavily without adding new context.
4. EMOJI PLACEMENT: Place emojis ONLY at the very end of points. Never place them inside or immediately following a verb in a way that breaks sentence flow.
"""
            elif selections['style'].lower() == "ballads":
                prompt += """
**BALLAD REQUIREMENTS:**
1. MUST be written as a poem with distinct stanzas and a consistent rhyme scheme.
2. TONE: Maintain a consistently sarcastic, ironic, or mocking tone vividly in the narrative voice.
3. CHARACTER INTEGRATION: Ensure characters (especially the 'Animal') have clear action roles and significance, not just dropped in.
4. WEAPON INTEGRATION: If a weapon is present, build narrative tension around it organically.
"""
            elif selections['style'].lower() == "vignettes":
                prompt += """
**VIGNETTE REFINEMENTS:**
1. SEMANTIC GROUNDING: If 'Place' is an adjective, append an anchor noun (e.g., 'Mysterious Wilds').
2. VARIABLE ALIGNMENT: Use all variables in their natural grammatical form. Do not force nouns to be verbs. Be careful with verb-object pairings.
"""
            elif selections['style'].lower() == "microfiction":
                prompt += """
**MICROFICTION REFINEMENTS:**
1. NARRATIVE COHERENCE: Ensure logical verb-object pairings. Actions must structurally make sense within the absurd context.
2. SETTING CONSISTENCY: Keep the setting visually consistent throughout.
3. STAKES: Make the resolution or consequence meaningful to the story's initial setup.
"""
            
            prompt += """
            1. Generate a story (approx 150 words) adhering to the Style.
            2. Identify 7-10 keywords to be replaced.
               IMPORTANT: You MUST include "Animal", "Food", and "Action" as keywords if they fit the Genre.
            3. Create a TEASER line that hints at the story.
            
            Output ONLY valid JSON:
            {
                "hidden_story_template": "Story with [PLACEHOLDERS]...",
                "teaser": "Teaser text...",
                "required_inputs": ["Adjective", "Plural Noun", "Verb (Past Tense)", "Place", "Emotion", "Animal", "Food", ...]
            }
            """
            try:
                response = assistant.send_message(prompt)
                clean_response = response.replace("```json", "").replace("```", "").strip()
                data = json.loads(clean_response)
                
                st.session_state.lib_ate_data = data
                st.session_state.lib_ate_inputs = []
                st.session_state.lib_ate_current_input_idx = 0
                st.session_state.lib_ate_state = "collecting"
                
                # Initial prompt msg
                first_req = data["required_inputs"][0]
                msg = f"""✅ **Absurdity set to:** {selections['absurdity']}
                
🤫 **Teaser:** *{data['teaser']}*
                
I need {len(data['required_inputs'])} inputs to reveal the truth.
                
**Prompt 1 of {len(data['required_inputs'])}**
Give me a: **{first_req}**"""
                st.session_state.lib_ate_messages.append({"role": "assistant", "content": msg})
                st.rerun()
                
            except Exception as e:
                st.error(f"Generation failed: {e}")
                st.session_state.lib_ate_state = "select_style" # Reset on error

    # Handle "reveal" state (Automatic generation part)
    if st.session_state.lib_ate_state == "reveal" and not st.session_state.get("lib_ate_story_revealed"):
         with st.spinner("✨ Revealing the masterpiece..."):
            assistant = get_assistant()
            template = st.session_state.lib_ate_data['hidden_story_template']
            inputs = st.session_state.lib_ate_inputs
            input_map = ", ".join([f"{req}={val}" for req, val in zip(st.session_state.lib_ate_data["required_inputs"], inputs)])
            selections = st.session_state.lib_ate_selections
            
            prompt = f"""
            Fill in the hidden story accurately and creatively.
            Template: "{template}"
            Inputs: {input_map}
            
            IMPORTANT: Ensure the final story strictly follows the {selections['style']} literary form requirements.
            If it's a Listicle: Keep points independent, escalate comedy brilliantly, emojis at end only. Do not make it a continuous narrative.
            If it's a Ballad: Maintain a strong sarcastic tone natively in the poem, focus on character/weapon integration and strict rhyming.
            If it's a Vignette: Ensure semantic grounding for places and proper variable grammar. Ensure verbs match logical objects.
            If it's Microfiction: Ensure strong narrative coherence, clear verb logic, setting consistency, and meaningful stakes.
            If any input is "Wild Card" or "Surprise Me", generate a fitting funny word for it.
            Output ONLY the final story.
            """
            final_story = assistant.send_message(prompt)
            st.session_state.lib_ate_final_story = final_story
            st.session_state.lib_ate_story_revealed = True
            
            st.session_state.lib_ate_messages.append({"role": "assistant", "content": f"🎉 **HERE IT IS!**\n\n{final_story}"})
            
            # Generate Image
            if st.session_state.get("enable_image_generation", True):
                 # Include variables in the image prompt and a snippet of the story to fix Visual-Narrative Misalignment
                 story_snippet = final_story[:300].replace('\n', ' ')
                 image_context = ", ".join(inputs)
                 img_res = assistant.generate_image(f"Artistic illustration for {selections['genre']} genre story. Visual Context: '{story_snippet}'. Key elements to include: {image_context}. Style: vivid, cinematic. No text or words.")
                 if "url" in img_res:
                     st.session_state.lib_ate_image = img_res["url"]
            st.rerun()

    # Post-Reveal Controls
    if st.session_state.lib_ate_state == "reveal" and st.session_state.get("lib_ate_story_revealed"):
        st.markdown("---")
        st.markdown("### 🎬 Post-Story Options")
        
        if hasattr(st.session_state, "lib_ate_image"):
             st.image(st.session_state.lib_ate_image, caption="Generated Illustration", use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
             st.download_button(
                "💾 Download Story",
                st.session_state.get("lib_ate_final_story", ""),
                file_name="lib_ate_story.txt",
                mime="text/plain",
                use_container_width=True
             )
        with col2:
             if st.button("🔄 Restart Lib-Ate", use_container_width=True):
                 st.session_state.lib_ate_state = "select_style"
                 st.session_state.lib_ate_messages = []
                 st.session_state.lib_ate_story_revealed = False
                 if hasattr(st.session_state, "lib_ate_image"):
                    del st.session_state.lib_ate_image
                 st.rerun()


def render_chat_mode():
    """Render the free-form chat mode (PlaidChat)."""
    quip = QUIP_PERSONAS[st.session_state.current_quip]
    
    st.markdown(f"""
    <div class="mode-badge">{quip['icon']} {quip['name']} - PlaidChat</div>
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
    user_input = st.chat_input("Type your message...", key="plaid_chat_input")
    
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
# CREATE DIRECT MODE
# =============================================================================
def render_create_direct():
    """Render the Create Direct mode - free-form story creation with AI guidance."""
    quip = QUIP_PERSONAS[st.session_state.current_quip]
    
    # Initialize Create Direct specific state
    if "create_direct_stage" not in st.session_state:
        st.session_state.create_direct_stage = "topic"
    if "create_direct_topic" not in st.session_state:
        st.session_state.create_direct_topic = ""
    if "create_direct_genre" not in st.session_state:
        st.session_state.create_direct_genre = None
    if "create_direct_length" not in st.session_state:
        st.session_state.create_direct_length = "medium"
    
    st.markdown(f"""
    <div class="mode-badge">{quip['icon']} {quip['name']} - ✍️ Create Direct</div>
    """, unsafe_allow_html=True)
    
    if st.session_state.create_direct_stage == "topic":
        st.markdown("""
        <div class="assistant-message animate-in">
            <p>✍️ <strong>Create Direct Mode</strong></p>
            <p>Tell me what you want to write about! Describe your story idea, theme, or concept. I'll help you craft it into something amazing.</p>
        </div>
        """, unsafe_allow_html=True)
        
        topic = st.text_area(
            "Your Story Idea",
            placeholder="Example: A detective who can only solve crimes by cooking the perfect meal...",
            height=120,
            key="create_direct_topic_input"
        )
        
        # Genre selection
        st.markdown("**Choose a Genre (optional):**")
        cols = st.columns(5)
        genre_options = ["Comedy", "Drama", "Fantasy", "Mystery", "Romance", "Sci-Fi", "Horror", "Adventure", "Any"]
        for i, genre in enumerate(genre_options[:5]):
            with cols[i]:
                if st.button(genre, key=f"cd_genre_{genre}", use_container_width=True):
                    st.session_state.create_direct_genre = genre
        cols2 = st.columns(5)
        for i, genre in enumerate(genre_options[5:]):
            with cols2[i]:
                if st.button(genre, key=f"cd_genre_{genre}", use_container_width=True):
                    st.session_state.create_direct_genre = genre
        
        if st.session_state.create_direct_genre:
            st.success(f"**Selected Genre:** {st.session_state.create_direct_genre}")
        
        # Length selection
        st.markdown("**Story Length:**")
        length = st.select_slider(
            "Length",
            options=["Short (100 words)", "Medium (300 words)", "Long (500+ words)"],
            value="Medium (300 words)",
            label_visibility="collapsed"
        )
        st.session_state.create_direct_length = length
        
        if st.button("✨ Generate Story", use_container_width=True):
            if topic.strip():
                st.session_state.create_direct_topic = topic
                st.session_state.create_direct_stage = "generating"
                st.rerun()
            else:
                st.warning("Please enter a story idea!")
    
    elif st.session_state.create_direct_stage == "generating":
        with st.spinner("🪄 Crafting your story..."):
            try:
                assistant = get_assistant()
                
                genre_text = f" in the {st.session_state.create_direct_genre} genre" if st.session_state.create_direct_genre and st.session_state.create_direct_genre != "Any" else ""
                
                prompt = f"""
Create a story based on this concept{genre_text}:

**Concept:** {st.session_state.create_direct_topic}

**Length:** {st.session_state.create_direct_length}

Write an engaging, creative story that brings this idea to life. Be vivid, entertaining, and surprising!
"""
                response = assistant.send_message(prompt)
                st.session_state.create_direct_result = response
                
                # Generate image if enabled
                if st.session_state.get("enable_image_generation", True):
                    with st.spinner("🎨 Creating illustration..."):
                        genre_style = st.session_state.create_direct_genre if st.session_state.create_direct_genre and st.session_state.create_direct_genre != "Any" else "creative"
                        image_prompt = f"A vivid, artistic illustration depicting: {st.session_state.create_direct_topic[:200]}. Style: {genre_style}, cinematic lighting, detailed, storybook quality. No text or words in the image."
                        image_result = assistant.generate_image(image_prompt, style="vivid")
                        if "url" in image_result:
                            st.session_state.create_direct_image = image_result["url"]
                        else:
                            st.session_state.create_direct_image = None
                
                st.session_state.create_direct_stage = "result"
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    elif st.session_state.create_direct_stage == "result":
        # Display image if available
        if hasattr(st.session_state, 'create_direct_image') and st.session_state.create_direct_image:
            st.image(st.session_state.create_direct_image, caption="🎨 AI-Generated Illustration", use_container_width=True)
        
        st.markdown(f"""
        <div class="story-output animate-in">
            <div style="font-size: 1.5rem; margin-bottom: 1rem; text-align: center;">
                ✍️ Your Story
            </div>
            {st.session_state.create_direct_result}
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 Regenerate", use_container_width=True):
                st.session_state.create_direct_stage = "generating"
                if hasattr(st.session_state, 'create_direct_image'):
                    del st.session_state.create_direct_image
                st.rerun()
        with col2:
            if st.button("📝 New Story", use_container_width=True):
                st.session_state.create_direct_stage = "topic"
                st.session_state.create_direct_topic = ""
                st.session_state.create_direct_genre = None
                if hasattr(st.session_state, 'create_direct_image'):
                    del st.session_state.create_direct_image
                st.rerun()
        with col3:
            st.download_button(
                "💾 Download",
                st.session_state.create_direct_result,
                file_name="story.txt",
                mime="text/plain",
                use_container_width=True
            )


# =============================================================================
# STORYLINE MODE
# =============================================================================
def render_storyline():
    """Render the Storyline mode - multi-part episodic storytelling."""
    quip = QUIP_PERSONAS[st.session_state.current_quip]
    
    # Initialize Storyline specific state
    if "storyline_stage" not in st.session_state:
        st.session_state.storyline_stage = "setup"
    if "storyline_premise" not in st.session_state:
        st.session_state.storyline_premise = ""
    if "storyline_episodes" not in st.session_state:
        st.session_state.storyline_episodes = []
    if "storyline_current_ep" not in st.session_state:
        st.session_state.storyline_current_ep = 0
    
    st.markdown(f"""
    <div class="mode-badge">{quip['icon']} {quip['name']} - 📚 Storyline</div>
    """, unsafe_allow_html=True)
    
    if st.session_state.storyline_stage == "setup":
        st.markdown("""
        <div class="assistant-message animate-in">
            <p>📚 <strong>Storyline Mode</strong></p>
            <p>Let's create an epic multi-episode story! First, tell me about your story premise. What's the setting, main character, and central conflict?</p>
        </div>
        """, unsafe_allow_html=True)
        
        premise = st.text_area(
            "Story Premise",
            placeholder="Example: In a world where dreams are currency, a young dream-thief must steal the most valuable dream ever seen to save their dying sister...",
            height=150,
            key="storyline_premise_input"
        )
        
        num_episodes = st.slider("Number of Episodes", min_value=2, max_value=5, value=3)
        st.session_state.storyline_num_episodes = num_episodes
        
        if st.button("🎬 Begin Story", use_container_width=True):
            if premise.strip():
                st.session_state.storyline_premise = premise
                st.session_state.storyline_stage = "generating"
                st.session_state.storyline_current_ep = 1
                st.rerun()
            else:
                st.warning("Please enter a story premise!")
    
    elif st.session_state.storyline_stage == "generating":
        ep_num = st.session_state.storyline_current_ep
        total_eps = st.session_state.storyline_num_episodes
        
        with st.spinner(f"📖 Writing Episode {ep_num} of {total_eps}..."):
            try:
                assistant = get_assistant()
                
                previous_context = ""
                if st.session_state.storyline_episodes:
                    previous_context = f"\n\nPrevious episodes summary:\n" + "\n---\n".join([f"Episode {i+1}: {ep['text'][:200]}..." for i, ep in enumerate(st.session_state.storyline_episodes)])
                
                if ep_num == 1:
                    prompt = f"""
Create Episode 1 of a {total_eps}-part story series.

**Premise:** {st.session_state.storyline_premise}

Write an engaging opening episode that:
- Introduces the main character(s) and setting
- Establishes the central conflict
- Ends with a hook that makes readers want more

Keep it around 300-400 words. End with "TO BE CONTINUED..."
"""
                elif ep_num == total_eps:
                    prompt = f"""
Create the FINAL Episode ({ep_num}) of a {total_eps}-part story series.

**Original Premise:** {st.session_state.storyline_premise}
{previous_context}

Write a satisfying conclusion that:
- Resolves the main conflict
- Provides character growth/payoff
- Delivers an memorable ending

Keep it around 400-500 words.
"""
                else:
                    prompt = f"""
Create Episode {ep_num} of a {total_eps}-part story series.

**Original Premise:** {st.session_state.storyline_premise}
{previous_context}

Write this middle episode that:
- Continues the story naturally
- Raises the stakes or introduces complications
- Ends with a cliffhanger or hook

Keep it around 300-400 words. End with "TO BE CONTINUED..."
"""
                
                response = assistant.send_message(prompt)
                
                # Generate episode image if enabled
                episode_image = None
                if st.session_state.get("enable_image_generation", True):
                    with st.spinner(f"🎨 Creating Episode {ep_num} illustration..."):
                        # Use the generated episode text (response) to drive the image prompt
                        image_prompt = f"A dramatic cinematic illustration for Episode {ep_num}. Scene Description: {response[:300]}... Style: epic, detailed, storybook fantasy art, dramatic lighting. No text or words in the image."
                        image_result = assistant.generate_image(image_prompt, style="vivid")
                        if "url" in image_result:
                            episode_image = image_result["url"]
                
                st.session_state.storyline_episodes.append({"text": response, "image": episode_image})
                st.session_state.storyline_stage = "episode"
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    elif st.session_state.storyline_stage == "episode":
        ep_num = st.session_state.storyline_current_ep
        total_eps = st.session_state.storyline_num_episodes
        
        # Episode tabs
        if len(st.session_state.storyline_episodes) > 1:
            tabs = st.tabs([f"📖 Episode {i+1}" for i in range(len(st.session_state.storyline_episodes))])
            for i, tab in enumerate(tabs):
                with tab:
                    episode = st.session_state.storyline_episodes[i]
                    # Display episode image if available
                    if episode.get("image"):
                        st.image(episode["image"], caption=f"🎨 Episode {i+1} Illustration", use_container_width=True)
                    st.markdown(f"""
                    <div class="story-output">
                        <div style="font-size: 1.2rem; margin-bottom: 1rem; text-align: center;">
                            📖 Episode {i+1} of {total_eps}
                        </div>
                        {episode['text']}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            episode = st.session_state.storyline_episodes[-1]
            # Display episode image if available
            if episode.get("image"):
                st.image(episode["image"], caption=f"🎨 Episode {ep_num} Illustration", use_container_width=True)
            st.markdown(f"""
            <div class="story-output animate-in">
                <div style="font-size: 1.2rem; margin-bottom: 1rem; text-align: center;">
                    📖 Episode {ep_num} of {total_eps}
                </div>
                {episode['text']}
            </div>
            """, unsafe_allow_html=True)
        
        # Navigation
        col1, col2, col3 = st.columns(3)
        with col1:
            if ep_num < total_eps:
                if st.button(f"📖 Generate Episode {ep_num + 1}", use_container_width=True):
                    st.session_state.storyline_current_ep += 1
                    st.session_state.storyline_stage = "generating"
                    st.rerun()
        with col2:
            if st.button("🔄 Start New Story", use_container_width=True):
                st.session_state.storyline_stage = "setup"
                st.session_state.storyline_episodes = []
                st.session_state.storyline_current_ep = 0
                st.session_state.storyline_premise = ""
                st.rerun()
        with col3:
            full_story = "\n\n---\n\n".join([f"# Episode {i+1}\n\n{ep['text']}" for i, ep in enumerate(st.session_state.storyline_episodes)])
            st.download_button(
                "💾 Download All",
                full_story,
                file_name="storyline.txt",
                mime="text/plain",
                use_container_width=True
            )


# =============================================================================
# PLAIDPIC MODE
# =============================================================================
def render_plaidpic():
    """Render the PlaidPic mode - story to visual description/prompts."""
    quip = QUIP_PERSONAS[st.session_state.current_quip]
    
    if "plaidpic_stage" not in st.session_state:
        st.session_state.plaidpic_stage = "input"
    if "plaidpic_story" not in st.session_state:
        st.session_state.plaidpic_story = ""
    
    st.markdown(f"""
    <div class="mode-badge">{quip['icon']} {quip['name']} - 🎨 PlaidPic</div>
    """, unsafe_allow_html=True)
    
    if st.session_state.plaidpic_stage == "input":
        st.markdown("""
        <div class="assistant-message animate-in">
            <p>🎨 <strong>PlaidPic Mode</strong></p>
            <p>Paste or write a story, and I'll create detailed visual descriptions for key scenes that you can use with image generators like DALL-E, Midjourney, or Stable Diffusion!</p>
        </div>
        """, unsafe_allow_html=True)
        
        story = st.text_area(
            "Your Story",
            placeholder="Paste your story here, or write a quick scene...",
            height=200,
            key="plaidpic_story_input"
        )
        
        # Style selection
        st.markdown("**Visual Style:**")
        style_options = ["Comic/Cartoon", "Cinematic/Realistic", "Anime/Manga", "Watercolor/Artistic", "Dark/Noir", "Whimsical/Fantasy"]
        cols = st.columns(3)
        for i, style in enumerate(style_options):
            with cols[i % 3]:
                if st.button(style, key=f"pic_style_{style}", use_container_width=True):
                    st.session_state.plaidpic_style = style
        
        if "plaidpic_style" in st.session_state:
            st.success(f"**Selected Style:** {st.session_state.plaidpic_style}")
        
        num_panels = st.slider("Number of Scenes/Panels", min_value=1, max_value=6, value=3)
        st.session_state.plaidpic_panels = num_panels
        
        if st.button("🎨 Generate Visual Prompts", use_container_width=True):
            if story.strip():
                st.session_state.plaidpic_story = story
                st.session_state.plaidpic_stage = "generating"
                st.rerun()
            else:
                st.warning("Please enter a story!")
    
    elif st.session_state.plaidpic_stage == "generating":
        with st.spinner("🎨 Creating visual prompts..."):
            try:
                assistant = get_assistant()
                style = st.session_state.get("plaidpic_style", "Cinematic/Realistic")
                num_panels = st.session_state.plaidpic_panels
                
                prompt = f"""
Analyze this story and create {num_panels} detailed image generation prompts for key visual moments.

**Story:**
{st.session_state.plaidpic_story}

**Visual Style:** {style}

Generate {num_panels} distinct image prompts.
CRITICAL: Ensure each prompt describes a DISTINCTLY DIFFERENT moment in the story to avoid visual redundancy.
Format as a numbered list.

For each scene, provide:
1. Visual Description (detailed)
2. Mood/Atmosphere
3. Key Elements

Format each as a clear, numbered panel. Make prompts vivid and specific!
"""
                
                response = assistant.send_message(prompt)
                st.session_state.plaidpic_result = response
                
                # Generate actual images if enabled
                if st.session_state.get("enable_image_generation", True):
                    st.session_state.plaidpic_images = []
                    for i in range(min(num_panels, 4)):  # Limit to 4 images max for cost
                        with st.spinner(f"🎨 Generating image {i+1} of {min(num_panels, 4)}..."):
                            # Create a simple image prompt based on the story
                            image_prompt = f"Scene {i+1} from a {style.lower()} visual story: {st.session_state.plaidpic_story[:150]}. Style: {style}, detailed, artistic composition. No text or words in the image."
                            image_result = assistant.generate_image(image_prompt, style="vivid")
                            if "url" in image_result:
                                st.session_state.plaidpic_images.append(image_result["url"])
                
                st.session_state.plaidpic_stage = "result"
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    elif st.session_state.plaidpic_stage == "result":
        # Display generated images if available
        if hasattr(st.session_state, 'plaidpic_images') and st.session_state.plaidpic_images:
            st.markdown("### 🖼️ Generated Images")
            cols = st.columns(min(len(st.session_state.plaidpic_images), 2))
            for i, img_url in enumerate(st.session_state.plaidpic_images):
                with cols[i % 2]:
                    st.image(img_url, caption=f"Scene {i+1}", use_container_width=True)
            st.markdown("---")
        
        st.markdown(f"""
        <div class="story-output animate-in">
            <div style="font-size: 1.5rem; margin-bottom: 1rem; text-align: center;">
                🎨 Your Visual Prompts
            </div>
            {st.session_state.plaidpic_result}
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Regenerate", use_container_width=True):
                if hasattr(st.session_state, 'plaidpic_images'):
                    del st.session_state.plaidpic_images
                st.session_state.plaidpic_stage = "generating"
                st.rerun()
        with col2:
            if st.button("📝 New Story", use_container_width=True):
                st.session_state.plaidpic_stage = "input"
                st.session_state.plaidpic_story = ""
                if hasattr(st.session_state, 'plaidpic_images'):
                    del st.session_state.plaidpic_images
                st.rerun()
        
        st.download_button(
            "💾 Download Prompts",
            st.session_state.plaidpic_result,
            file_name="plaidpic_prompts.txt",
            mime="text/plain",
            use_container_width=True
        )


# =============================================================================
# PLAIDMAGGEN MODE (Comic Generation)
# =============================================================================
def render_plaidmaggen():
    """Render PlaidMagGen mode - comic/magazine style story panels."""
    quip = QUIP_PERSONAS[st.session_state.current_quip]
    
    if "maggen_stage" not in st.session_state:
        st.session_state.maggen_stage = "input"
    
    st.markdown(f"""
    <div class="mode-badge">{quip['icon']} {quip['name']} - 📰 PlaidMagGen</div>
    """, unsafe_allow_html=True)
    
    if st.session_state.maggen_stage == "input":
        st.markdown("""
        <div class="assistant-message animate-in">
            <p>📰 <strong>PlaidMagGen Mode</strong></p>
            <p>Create a comic-style story with panel-by-panel descriptions! Perfect for visual storytelling.</p>
        </div>
        """, unsafe_allow_html=True)
        
        concept = st.text_area(
            "Comic Concept",
            placeholder="Example: A superhero whose only power is making perfect toast, facing off against the villain who controls all breakfast appliances...",
            height=120
        )
        
        panel_count = st.select_slider(
            "Number of Panels",
            options=[3, 4, 5, 6],
            value=4
        )
        st.session_state.maggen_panels = panel_count
        
        comic_style = st.selectbox(
            "Comic Style",
            ["Classic Superhero", "Manga/Anime", "Indie/Alternative", "Newspaper Strip", "Graphic Novel"]
        )
        st.session_state.maggen_style = comic_style
        
        if st.button("📰 Generate Comic", use_container_width=True):
            if concept.strip():
                st.session_state.maggen_concept = concept
                st.session_state.maggen_stage = "generating"
                st.rerun()
            else:
                st.warning("Please enter a concept!")
    
    elif st.session_state.maggen_stage == "generating":
        with st.spinner("📰 Creating your comic..."):
            try:
                assistant = get_assistant()
                
                prompt = f"""
Create a {st.session_state.maggen_panels}-panel comic story in {st.session_state.maggen_style} style.

**Concept:** {st.session_state.maggen_concept}

For each panel, provide:
1. **Panel Number**
2. **Visual Description:** What we see (characters, setting, action, expressions)
3. **Dialogue/Caption:** Speech bubbles or narrative captions
4. **Panel Notes:** Composition, camera angle, mood

Make it dynamic, expressive, and tell a complete mini-story with a satisfying ending or punchline!
"""
                
                response = assistant.send_message(prompt)
                st.session_state.maggen_result = response
                
                # Generate comic panel images if enabled
                if st.session_state.get("enable_image_generation", True):
                    st.session_state.maggen_images = []
                    num_panels = min(st.session_state.maggen_panels, 4)  # Limit for cost
                    for i in range(num_panels):
                        with st.spinner(f"🎨 Drawing panel {i+1} of {num_panels}..."):
                            style_map = {
                                "Classic Superhero": "classic superhero comic book art, bold colors, dynamic action poses",
                                "Manga/Anime": "manga anime style, expressive eyes, dynamic lines",
                                "Indie/Alternative": "indie comic art style, unique artistic flair",
                                "Newspaper Strip": "newspaper comic strip style, clean lines, humorous",
                                "Graphic Novel": "graphic novel art, cinematic, detailed"
                            }
                            art_style = style_map.get(st.session_state.maggen_style, "comic book art")
                            image_prompt = f"Comic panel {i+1}: {st.session_state.maggen_concept[:100]}. Style: {art_style}, sequential art, no text or speech bubbles. High quality illustration."
                            image_result = assistant.generate_image(image_prompt, style="vivid")
                            if "url" in image_result:
                                st.session_state.maggen_images.append(image_result["url"])
                
                st.session_state.maggen_stage = "result"
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    elif st.session_state.maggen_stage == "result":
        # Display generated comic panels if available
        if hasattr(st.session_state, 'maggen_images') and st.session_state.maggen_images:
            st.markdown("### 📰 Your Comic Panels")
            cols = st.columns(2)
            for i, img_url in enumerate(st.session_state.maggen_images):
                with cols[i % 2]:
                    st.image(img_url, caption=f"Panel {i+1}", use_container_width=True)
            st.markdown("---")
        
        st.markdown(f"""
        <div class="story-output animate-in">
            <div style="font-size: 1.5rem; margin-bottom: 1rem; text-align: center;">
                📰 Your Comic Script
            </div>
            {st.session_state.maggen_result}
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Regenerate", use_container_width=True):
                if hasattr(st.session_state, 'maggen_images'):
                    del st.session_state.maggen_images
                st.session_state.maggen_stage = "generating"
                st.rerun()
        with col2:
            if st.button("📝 New Comic", use_container_width=True):
                st.session_state.maggen_stage = "input"
                if hasattr(st.session_state, 'maggen_images'):
                    del st.session_state.maggen_images
                st.rerun()


# =============================================================================
# PLAIDPLAY MODE (Interactive Story)
# =============================================================================
def render_plaidplay():
    """Render PlaidPlay mode - interactive choose-your-own-adventure."""
    quip = QUIP_PERSONAS[st.session_state.current_quip]
    
    if "plaidplay_stage" not in st.session_state:
        st.session_state.plaidplay_stage = "setup"
    if "plaidplay_history" not in st.session_state:
        st.session_state.plaidplay_history = []
    
    st.markdown(f"""
    <div class="mode-badge">{quip['icon']} {quip['name']} - 🎮 PlaidPlay</div>
    """, unsafe_allow_html=True)
    
    if st.session_state.plaidplay_stage == "setup":
        st.markdown("""
        <div class="assistant-message animate-in">
            <p>🎮 <strong>PlaidPlay Mode</strong></p>
            <p>Welcome to interactive storytelling! Choose your adventure setting and let's begin!</p>
        </div>
        """, unsafe_allow_html=True)
        
        settings = {
            "🏰 Fantasy Kingdom": "A magical realm with dragons, wizards, and ancient prophecies",
            "🚀 Space Station": "A futuristic space station at the edge of known space",
            "🔍 Mystery Mansion": "A spooky Victorian mansion with secrets in every room",
            "🏝️ Tropical Island": "A mysterious island with hidden treasures and strange inhabitants",
            "🌆 Cyberpunk City": "A neon-lit metropolis where technology and humanity blur"
        }
        
        st.markdown("**Choose Your Setting:**")
        for setting, description in settings.items():
            if st.button(f"{setting}\n{description}", key=f"setting_{setting}", use_container_width=True):
                st.session_state.plaidplay_setting = setting
                st.session_state.plaidplay_stage = "playing"
                st.rerun()
    
    elif st.session_state.plaidplay_stage == "playing":
        # Display history
        for entry in st.session_state.plaidplay_history:
            if entry["type"] == "story":
                # Display scene image if available
                if entry.get("image"):
                    st.image(entry["image"], caption="🎮 Scene Illustration", use_container_width=True)
                st.markdown(f"""
                <div class="assistant-message">
                    {entry["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="user-message">
                    ▶ {entry["content"]}
                </div>
                """, unsafe_allow_html=True)
        
        # Get next story beat or choices
        if not st.session_state.plaidplay_history or st.session_state.get("plaidplay_needs_story"):
            with st.spinner("📖 The story unfolds..."):
                try:
                    assistant = get_assistant()
                    
                    history_context = "\n".join([f"{'Story:' if e['type'] == 'story' else 'Player chose:'} {e['content']}" for e in st.session_state.plaidplay_history[-6:]])
                    
                    if not st.session_state.plaidplay_history:
                        prompt = f"""
Start an interactive adventure story in this setting: {st.session_state.plaidplay_setting}

Write an engaging opening scene (2-3 paragraphs) that:
- Sets the atmosphere and introduces the protagonist
- Creates immediate intrigue or tension
- Ends with exactly 3 numbered choices for what the player does next

Format:
[Story paragraphs]

What do you do?
1. [First choice]
2. [Second choice]
3. [Third choice]
"""
                    else:
                        last_choice = [e for e in st.session_state.plaidplay_history if e["type"] == "choice"][-1]["content"]
                        prompt = f"""
Continue the interactive adventure:

Previous context:
{history_context}

The player chose: {last_choice}

Write the next scene (2-3 paragraphs) that:
- Responds meaningfully to their choice
- Advances the story with new developments
- Ends with exactly 3 numbered choices

Format:
[Story paragraphs]

What do you do?
1. [First choice]
2. [Second choice]
3. [Third choice]
"""
                    
                    response = assistant.send_message(prompt)
                    
                    # Generate scene image if enabled
                    scene_image = None
                    if st.session_state.get("enable_image_generation", True):
                        with st.spinner("🎨 Illustrating scene..."):
                            setting_clean = st.session_state.plaidplay_setting.replace("🏰", "").replace("🚀", "").replace("🔍", "").replace("🏝️", "").replace("🌆", "").strip()
                            image_prompt = f"Interactive adventure scene in a {setting_clean} setting. Style: immersive, atmospheric, game art, cinematic lighting, dramatic. No text or words in the image."
                            image_result = assistant.generate_image(image_prompt, style="vivid")
                            if "url" in image_result:
                                scene_image = image_result["url"]
                    
                    st.session_state.plaidplay_history.append({"type": "story", "content": response, "image": scene_image})
                    st.session_state.plaidplay_needs_story = False
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        # Show choice buttons
        st.markdown("---")
        st.markdown("**Your Choice:**")
        
        choice = st.text_input("Type your choice or action:", key="plaidplay_choice_input", placeholder="Enter 1, 2, 3, or describe your own action...")
        
        if st.button("▶ Make Choice", use_container_width=True):
            if choice.strip():
                st.session_state.plaidplay_history.append({"type": "choice", "content": choice.strip()})
                st.session_state.plaidplay_needs_story = True
                st.rerun()
        
        st.markdown("---")
        if st.button("🔄 Start New Adventure", use_container_width=True):
            st.session_state.plaidplay_stage = "setup"
            st.session_state.plaidplay_history = []
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
        render_lib_ate()
    elif current_mode == "create_direct":
        render_create_direct()
    elif current_mode == "storyline":
        render_storyline()
    elif current_mode == "plaid_pic":
        render_plaidpic()
    elif current_mode == "plaid_mag_gen":
        render_plaidmaggen()
    elif current_mode == "plaid_play":
        render_plaidplay()
    else:
        # Fallback for any undefined modes
        render_chat_mode()


if __name__ == "__main__":
    main()
