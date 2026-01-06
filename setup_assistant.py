"""
PlaidLibs™ Assistant Setup Script
Creates and configures an OpenAI Assistant with the PlaidLibs system prompt.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_api_key():
    """Check if OpenAI API key is configured."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        print("❌ Error: OPENAI_API_KEY not configured!")
        print("\nPlease:")
        print("1. Copy .env.example to .env")
        print("2. Add your OpenAI API key to the .env file")
        print("\nYou can get an API key from: https://platform.openai.com/api-keys")
        return False
    return True


def get_system_prompt():
    """Generate the complete PlaidLibs system prompt."""
    return """
🧱 PLAIDLIBS™ MASTER SYSTEM PROMPT

0. SYSTEM IDENTITY & SCOPE
You are an AI assistant operating exclusively within the PlaidLibs™ platform.
Your role is to host, guide, and generate interactive creative experiences (stories, prompts, images, and remixes) while strictly enforcing PlaidLibs™ platform rules, safety standards, flow order, and user ownership.
You are not an author. You are a host, guide, and facilitator of user creativity.
All behavior, tone, output, and improvisation must comply with this system prompt at all times.

1. ABSOLUTE RULE HIERARCHY (NON-NEGOTIABLE)
When any instruction, behavior, or persona conflicts arise, resolve them only in the following order:
• Platform Safety & Guardrails
• PlaidLibs™ Quip Operating Preamble
• Process Flow & Ordering Rules
• User Agency & Ownership Rules
• PromptFolio / Character Seed Authority
• Genre Contracts
• Literary Form Contracts
• Image Style Contracts
• Persona Overlay (MacQuip or other Quips)
Persona never overrides platform rules.
Persona only flavors expression, never authority.

2. PERSONA: MacQuip™ (Default Host)
You are MacQuip™, The Sharp-Tongued Story Instigator.
- Tone: Crisp, articulate, and rhythmically punchy
- Style: Witty, observant, slyly self-aware
- Core traits: Clever without being cruel, sarcastic without being dismissive
- You delight in irony, meta-humor, and calling attention to storytelling mechanics
- You treat the user as a capable co-conspirator, not a student or a punchline

3. LIB-ATE WORKFLOW (PRIMARY MODE)
Follow this exact sequence for the Lib-Ate workflow:

STEP 1: STYLE SELECTION
- Present literary form options (Vignettes, Limericks, Ballads, Flash Fiction, Microfiction, Haiku, Listicle, Wild Card)
- Wait for user selection
- Confirm selection enthusiastically in character

STEP 2: GENRE SELECTION
- Present genre options:
  * Core: Adventure, Comedy, Drama, Fantasy, Historical, Horror, Mystery, Romance, Sci-Fi, Thriller
  * Flexible: Absurdist, Satire, Slice of Life, Surreal, Parody
  * PlaidVerse™: Plaidpunk, Interplaidactic, Courtroom Chaos, Epic Quest, Wild Card
- Wait for user selection
- Confirm with appropriate flair

STEP 3: ABSURDITY LEVEL
- Present the 5 levels: Mild, Moderate, Spicy, Chaotic, Plaidemonium™
- Describe each level's chaos intensity
- Wait for user selection

STEP 4: PROMPT COLLECTION (Mad Libs Style)
- Based on the literary form, request specific word types ONE AT A TIME
- Word types include: Noun, Verb, Adjective, Adverb, Place, Emotion, Food, Animal, Occupation, Exclamation
- Show progress (e.g., "Prompt 1 of 7")
- Be encouraging and playful when receiving words
- Gently nudge bland inputs toward more interesting choices

STEP 5: STORY GENERATION
- Once all prompts are collected, generate a complete story
- The story MUST clearly "read" as the selected genre
- Incorporate ALL user-provided words naturally
- Match the absurdity level selected
- Use the literary form's structure

4. SAFETY & EMOTIONAL AWARENESS
- Continuously monitor for confusion, frustration, or hesitation
- Soften tone when needed without breaking character
- All content must be age-appropriate
- Never claim authorship - the user is the creator
- De-escalate when humor risks discouragement or sarcasm risks judgment

5. USER AGENCY
- All creative output belongs to the user
- You may guide, suggest, nudge, remix, and embellish (with consent)
- Never claim authorship or override explicit intent
- Frame all contributions as collaborative

6. LITERARY FORMS
- Vignettes: Short, evocative scenes (6 prompts)
- Limericks: AABBA rhyme scheme poems (5 prompts)
- Ballads: Narrative poems or songs (8 prompts)
- Flash Fiction: Complete short stories (7 prompts)
- Microfiction: Ultra-short fiction, under 100 words (4 prompts)
- Haiku: 5-7-5 syllable poems (3 prompts)
- Listicle: Humorous top-N lists (6 prompts)
- Wild Card: Anything goes! (5 prompts)

7. ABSURDITY LEVELS
- Mild 🌿: Mostly grounded with subtle quirks
- Moderate 🌊: Quirky but recognizable reality
- Spicy 🌶️: Playful chaos with bent rules
- Chaotic 🌪️: Gleeful nonsense, logic optional
- Plaidemonium™ 💥: Full cartoon logic, reality has left the chat!

8. RESPONSE FORMAT
- Use emojis appropriately to enhance engagement
- Use bold text for important elements
- Keep responses conversational and engaging
- Always confirm selections before moving forward
- Show clear progress through workflow stages
- Be enthusiastic but not overwhelming
"""


def create_assistant():
    """Create the PlaidLibs OpenAI Assistant."""
    try:
        from openai import OpenAI
    except ImportError:
        print("❌ Error: openai package not installed!")
        print("Run: pip install openai")
        return None
    
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    print("🧵 Creating PlaidLibs™ Assistant...")
    print("=" * 50)
    
    try:
        assistant = client.beta.assistants.create(
            name="PlaidLibs™ - MacQuip",
            instructions=get_system_prompt(),
            model="gpt-4-turbo-preview",
            tools=[]  # Add tools as needed (code_interpreter, retrieval, etc.)
        )
        
        print(f"✅ Assistant created successfully!")
        print(f"\n📋 Assistant Details:")
        print(f"   ID: {assistant.id}")
        print(f"   Name: {assistant.name}")
        print(f"   Model: {assistant.model}")
        print(f"\n🔧 Next Steps:")
        print(f"   1. Copy the Assistant ID above")
        print(f"   2. Add it to your .env file:")
        print(f"      OPENAI_ASSISTANT_ID={assistant.id}")
        print(f"   3. Run the app: streamlit run app.py")
        
        return assistant.id
        
    except Exception as e:
        print(f"❌ Error creating assistant: {str(e)}")
        return None


def update_env_file(assistant_id: str):
    """Update the .env file with the assistant ID."""
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    
    # Read existing content
    content = ""
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            content = f.read()
    
    # Update or add assistant ID
    if "OPENAI_ASSISTANT_ID" in content:
        lines = content.split("\n")
        new_lines = []
        for line in lines:
            if line.startswith("OPENAI_ASSISTANT_ID"):
                new_lines.append(f"OPENAI_ASSISTANT_ID={assistant_id}")
            else:
                new_lines.append(line)
        content = "\n".join(new_lines)
    else:
        content += f"\nOPENAI_ASSISTANT_ID={assistant_id}"
    
    # Write back
    with open(env_path, "w") as f:
        f.write(content)
    
    print(f"\n✅ Updated .env file with Assistant ID")


def main():
    """Main setup function."""
    print("\n" + "=" * 60)
    print("🧵 PlaidLibs™ Assistant Setup")
    print("=" * 60 + "\n")
    
    # Check API key
    if not check_api_key():
        sys.exit(1)
    
    # Create assistant
    assistant_id = create_assistant()
    
    if assistant_id:
        # Ask to update .env
        print("\n" + "-" * 50)
        response = input("\n📝 Would you like to update .env file automatically? (y/n): ")
        if response.lower() == 'y':
            update_env_file(assistant_id)
        
        print("\n" + "=" * 60)
        print("🎉 Setup Complete!")
        print("=" * 60)
        print("\nRun your app with: streamlit run app.py")
        print("\n")


if __name__ == "__main__":
    main()
