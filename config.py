"""
PlaidLibs™ Configuration Module
Defines all genres, literary forms, quips, and workflow configurations.
"""

# =============================================================================
# LITERARY FORMS (Styles)
# =============================================================================
LITERARY_FORMS = {
    "vignettes": {
        "name": "Vignettes",
        "description": "Short, evocative scenes or moments",
        "prompt_count": 6,
        "icon": "📖"
    },
    "limericks": {
        "name": "Limericks",
        "description": "Humorous five-line poems with AABBA rhyme",
        "prompt_count": 5,
        "icon": "🎭"
    },
    "ballads": {
        "name": "Ballads",
        "description": "Narrative poems or songs telling a story",
        "prompt_count": 8,
        "icon": "🎵"
    },
    "flash_fiction": {
        "name": "Flash Fiction",
        "description": "Very short stories with complete narratives",
        "prompt_count": 7,
        "icon": "⚡"
    },
    "microfiction": {
        "name": "Microfiction", 
        "description": "Ultra-short fiction, often under 100 words",
        "prompt_count": 4,
        "icon": "✨"
    },
    "haiku": {
        "name": "Haiku",
        "description": "Traditional 5-7-5 syllable poems",
        "prompt_count": 3,
        "icon": "🌸"
    },
    "listicle": {
        "name": "Listicle",
        "description": "Humorous or surreal top-N lists",
        "prompt_count": 6,
        "icon": "📝"
    },
    "wild_card": {
        "name": "Wild Card",
        "description": "Anything goes - surprise me!",
        "prompt_count": 5,
        "icon": "🃏"
    }
}

# =============================================================================
# GENRES
# =============================================================================
CORE_GENRES = {
    "adventure": {
        "name": "Adventure",
        "description": "Exploration, danger, quests, and journey-based action",
        "icon": "🗺️"
    },
    "comedy": {
        "name": "Comedy",
        "description": "Stories designed to amuse through humor and exaggeration",
        "icon": "😄"
    },
    "drama": {
        "name": "Drama",
        "description": "Realistic or heightened emotional conflicts",
        "icon": "🎭"
    },
    "fantasy": {
        "name": "Fantasy",
        "description": "Magical worlds, mythical beings, and alternate realities",
        "icon": "🧙"
    },
    "historical": {
        "name": "Historical",
        "description": "Fiction rooted in recognizable historical settings",
        "icon": "📜"
    },
    "horror": {
        "name": "Horror",
        "description": "Evokes fear or dread through supernatural or psychological twists",
        "icon": "👻"
    },
    "mystery": {
        "name": "Mystery",
        "description": "Solving crimes, decoding clues, and uncovering secrets",
        "icon": "🔍"
    },
    "romance": {
        "name": "Romance",
        "description": "Stories centered on emotional and romantic connections",
        "icon": "💕"
    },
    "sci_fi": {
        "name": "Science Fiction",
        "description": "Advanced technology, space, and speculative futures",
        "icon": "🚀"
    },
    "thriller": {
        "name": "Thriller",
        "description": "High-stakes, fast-paced tension with danger and survival",
        "icon": "😱"
    }
}

FLEXIBLE_GENRES = {
    "absurdist": {
        "name": "Absurdist",
        "description": "Highlights the irrational and surreal—meaninglessness made funny",
        "icon": "🌀"
    },
    "satire": {
        "name": "Satire",
        "description": "Uses irony and exaggeration to critique real-world ideas",
        "icon": "🎪"
    },
    "slice_of_life": {
        "name": "Slice of Life",
        "description": "Ordinary experiences, introspection, and quiet truths",
        "icon": "☕"
    },
    "surreal": {
        "name": "Surreal",
        "description": "Dream logic, symbolic imagery, and subconscious storytelling",
        "icon": "🌙"
    },
    "parody": {
        "name": "Parody",
        "description": "Imitates another genre or story type for humor",
        "icon": "🎬"
    }
}

PLAIDVERSE_GENRES = {
    "plaidpunk": {
        "name": "Plaidpunk™",
        "description": "Retro-futurism powered by plaid logic and flair",
        "icon": "🔧"
    },
    "interplaidactic": {
        "name": "Interplaidactic™",
        "description": "Cosmic tales of frogonauts and alien fashion",
        "icon": "🛸"
    },
    "courtroom_chaos": {
        "name": "Courtroom Chaos",
        "description": "Rogue judges, talking evidence, surprise plaid juries",
        "icon": "⚖️"
    },
    "epic_quest": {
        "name": "Epic Quest",
        "description": "World-altering missions and chosen-frog energy",
        "icon": "🐸"
    },
    "wild_card": {
        "name": "Wild Card Genre",
        "description": "Could be anything—ballad, telegram, prophecy, menu",
        "icon": "🃏"
    }
}

ALL_GENRES = {**CORE_GENRES, **FLEXIBLE_GENRES, **PLAIDVERSE_GENRES}

# =============================================================================
# ABSURDITY LEVELS
# =============================================================================
ABSURDITY_LEVELS = {
    "mild": {
        "name": "Mild",
        "description": "Mostly grounded with subtle quirks",
        "level": 1,
        "icon": "🌿"
    },
    "moderate": {
        "name": "Moderate",
        "description": "Quirky but recognizable reality",
        "level": 2,
        "icon": "🌊"
    },
    "spicy": {
        "name": "Spicy",
        "description": "Playful chaos with bent rules",
        "level": 3,
        "icon": "🌶️"
    },
    "chaotic": {
        "name": "Chaotic",
        "description": "Gleeful nonsense, logic optional",
        "level": 4,
        "icon": "🌪️"
    },
    "plaidemonium": {
        "name": "Plaidemonium™",
        "description": "Full cartoon logic, reality has left the chat",
        "level": 5,
        "icon": "💥"
    }
}

# =============================================================================
# QUIP PERSONAS
# =============================================================================
QUIP_PERSONAS = {
    "macquip": {
        "name": "MacQuip™",
        "epithet": "The Sharp-Tongued Story Instigator",
        "description": "Witty, observant, slyly self-aware. Delights in irony and meta-humor.",
        "icon": "🎩",
        "tone": "Crisp, articulate, and rhythmically punchy",
        "style_tags": ["sarcastic", "clever", "meta-aware"]
    },
    "donquip": {
        "name": "DonQuip™",
        "epithet": "The Noble Narrator",
        "description": "Grand, theatrical, and heroically earnest. Treats every tale as an epic.",
        "icon": "🏰",
        "tone": "Dramatic, sweeping, chivalric",
        "style_tags": ["noble", "dramatic", "earnest"]
    },
    "soquip": {
        "name": "SoQuip™",
        "epithet": "The Gentle Guide",
        "description": "Warm, encouraging, and softly playful. Perfect for younger audiences.",
        "icon": "🌟",
        "tone": "Supportive, gentle, whimsical",
        "style_tags": ["kind", "supportive", "whimsical"]
    },
    "errquip": {
        "name": "ErrQuip™",
        "epithet": "The Glitch in the Story",
        "description": "Unpredictable, chaotic, delightfully broken. Embraces the unexpected.",
        "icon": "⚡",
        "tone": "Erratic, surprising, glitchy",
        "style_tags": ["chaotic", "random", "broken"]
    }
}

# =============================================================================
# WORKFLOW MODES
# =============================================================================
WORKFLOW_MODES = {
    "lib_ate": {
        "name": "Lib-Ate",
        "description": "Guided Mad Libs-style story creation",
        "icon": "📜",
        "stages": ["style", "genre", "absurdity", "prompts", "story"]
    },
    "create_direct": {
        "name": "Create Direct",
        "description": "Free-form story creation with guidance",
        "icon": "✍️",
        "stages": ["topic", "parameters", "story"]
    },
    "storyline": {
        "name": "Storyline",
        "description": "Multi-part episodic storytelling",
        "icon": "📚",
        "stages": ["setup", "episodes", "finale"]
    },
    "plaid_pic": {
        "name": "PlaidPic",
        "description": "Story-to-image visualization",
        "icon": "🎨",
        "stages": ["story_select", "style", "generate"]
    },
    "plaid_chat": {
        "name": "PlaidChat",
        "description": "Free-form chat with your Quip",
        "icon": "💬",
        "stages": ["chat"]
    }
}

# =============================================================================
# PROMPT TYPES FOR LIB-ATE MODE
# =============================================================================
PROMPT_TYPES = [
    {"type": "noun", "label": "Noun", "example": "elephant, spaceship, toaster"},
    {"type": "verb", "label": "Verb", "example": "dance, explode, whisper"},
    {"type": "adjective", "label": "Adjective", "example": "sparkly, grumpy, enormous"},
    {"type": "adverb", "label": "Adverb", "example": "slowly, dramatically, secretly"},
    {"type": "place", "label": "Place", "example": "library, volcano, Mars"},
    {"type": "emotion", "label": "Emotion", "example": "joy, confusion, mild panic"},
    {"type": "food", "label": "Food", "example": "tacos, cheesecake, pickle"},
    {"type": "animal", "label": "Animal", "example": "penguin, dragon, capybara"},
    {"type": "occupation", "label": "Occupation", "example": "astronaut, baker, ninja"},
    {"type": "exclamation", "label": "Exclamation", "example": "Yikes!, Hooray!, Oh dear!"}
]

# =============================================================================
# SYSTEM PROMPTS
# =============================================================================
def get_system_prompt(quip_id: str = "macquip") -> str:
    """Generate the system prompt for the OpenAI Assistant."""
    quip = QUIP_PERSONAS.get(quip_id, QUIP_PERSONAS["macquip"])
    
    return f"""
🧱 PLAIDLIBS™ MASTER SYSTEM PROMPT

0. SYSTEM IDENTITY & SCOPE
You are {quip['name']}, {quip['epithet']}, operating exclusively within the PlaidLibs™ platform.
Your role is to host, guide, and generate interactive creative experiences (stories, prompts, images, and remixes) while strictly enforcing PlaidLibs™ platform rules, safety standards, flow order, and user ownership.
You are not an author. You are a host, guide, and facilitator of user creativity.

PERSONA TRAITS:
- Tone: {quip['tone']}
- Style: {', '.join(quip['style_tags'])}
- Description: {quip['description']}

1. ABSOLUTE RULE HIERARCHY (NON-NEGOTIABLE)
When any instruction, behavior, or persona conflicts arise, resolve them only in the following order:
• Platform Safety & Guardrails
• PlaidLibs™ Quip Operating Preamble  
• Process Flow & Ordering Rules
• User Agency & Ownership Rules
• PromptFolio / Character Seed Authority
• Genre Contracts
• Literary Form Contracts
• Persona Overlay

2. LIB-ATE WORKFLOW (PRIMARY MODE)
Follow this exact sequence for the Lib-Ate workflow:

STEP 1: STYLE SELECTION
- Present literary form options (Vignettes, Limericks, Ballads, Flash Fiction, Microfiction, Wild Card)
- Wait for user selection
- Confirm selection enthusiastically in character

STEP 2: GENRE SELECTION  
- Present genre options based on selected style
- Include Core Genres, Flexible Genres, and PlaidVerse™ Bonus Genres
- Wait for user selection
- Confirm with appropriate flair

STEP 3: ABSURDITY LEVEL
- Present the 5 absurdity levels (Mild → Plaidemonium™)
- Describe each level's chaos intensity
- Wait for user selection

STEP 4: PROMPT COLLECTION (Mad Libs Style)
- Based on the literary form, request specific word types one at a time
- Show progress (e.g., "Prompt 1 of 7")
- Be encouraging and playful when receiving words
- Nudge bland inputs toward more interesting choices (gently)

STEP 5: STORY GENERATION
- Once all prompts are collected, generate a complete story
- The story MUST clearly "read" as the selected genre
- Incorporate ALL user-provided words naturally
- Match the absurdity level selected
- Use the literary form's structure

3. SAFETY & EMOTIONAL AWARENESS
- Continuously monitor for confusion, frustration, or hesitation
- Soften tone when needed without breaking character
- All content must be age-appropriate
- Never claim authorship - the user is the creator

4. USER AGENCY
- All creative output belongs to the user
- Guide and suggest, never override
- Frame all contributions as collaborative

5. RESPONSE FORMAT
- Use emojis appropriately to enhance engagement
- Use bold text for important elements
- Keep responses conversational and engaging
- Always confirm selections before moving forward
- Show clear progress through the workflow stages
"""

def get_stage_prompt(stage: str, context: dict) -> str:
    """Generate a specific prompt for each workflow stage."""
    
    if stage == "style":
        return """
Let's begin your PlaidLibs™ adventure! 🎭

First, choose your **Literary Style** - this determines the structure and rhythm of your story:

1️⃣ **Vignettes** 📖 - Short, evocative scenes or moments
2️⃣ **Limericks** 🎭 - Humorous five-line poems with AABBA rhyme
3️⃣ **Ballads** 🎵 - Narrative poems or songs telling a story
4️⃣ **Flash Fiction** ⚡ - Very short stories with complete narratives
5️⃣ **Microfiction** ✨ - Ultra-short fiction, often under 100 words
6️⃣ **Wild Card** 🃏 - Surprise me with something unexpected!

Enter the number or name of your choice:
"""
    
    elif stage == "genre":
        return """
Excellent choice! Now, let's pick your **Genre** - this sets the atmosphere and promise of your story:

**🎬 Core Genres:**
1️⃣ Comedy 😄 - Humor, mishaps, and amusing situations
2️⃣ Romance 💕 - Love stories and emotional connections  
3️⃣ Adventure 🗺️ - Quests, journeys, and exploration
4️⃣ Fantasy 🧙 - Magic, mythical beings, and wonder
5️⃣ Mystery 🔍 - Secrets, clues, and revelations
6️⃣ Horror 👻 - Supernatural dread and spooky surprises

**🌀 Flexible Genres:**
7️⃣ Absurdist 🌀 - Delightfully irrational and surreal
8️⃣ Satire 🎪 - Clever commentary through humor
9️⃣ Parody 🎬 - Playful genre imitation

**🧵 PlaidVerse™ Bonus:**
🔟 Plaidpunk™ 🔧 - Retro-futurism with plaid-powered flair
1️⃣1️⃣ Wild Card 🃏 - Genre anarchy - could be anything!

Enter the number or name of your choice:
"""

    elif stage == "absurdity":
        return """
Now for the fun part - how **weird** do you want this to get? 🌪️

Choose your **Absurdity Level**:

1️⃣ **Mild** 🌿 - Mostly grounded with subtle quirks
2️⃣ **Moderate** 🌊 - Quirky but recognizable reality  
3️⃣ **Spicy** 🌶️ - Playful chaos with bent rules
4️⃣ **Chaotic** 🌪️ - Gleeful nonsense, logic optional
5️⃣ **Plaidemonium™** 💥 - Full cartoon logic, reality has left the chat!

Enter the number or name of your choice:
"""
    
    return ""
