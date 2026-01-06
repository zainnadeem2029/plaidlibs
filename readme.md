# PlaidLibs™ - Interactive Storytelling Platform

<p align="center">
  <img src="https://img.shields.io/badge/Powered%20by-OpenAI%20Assistants%20API-412991?style=for-the-badge&logo=openai" alt="OpenAI">
  <img src="https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit" alt="Streamlit">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python" alt="Python">
</p>

## 🧵 Overview

PlaidLibs™ is an interactive storytelling platform that uses OpenAI's Assistants API to create engaging, Mad Libs-style creative writing experiences. Users are guided through a multi-step workflow by AI "Quip" personas to generate unique stories, poems, and other literary forms.

### ✨ Features

- **🎭 Multiple Quip Personas**: Choose from witty MacQuip™, noble DonQuip™, gentle SoQuip™, or chaotic ErrQuip™
- **📚 Literary Forms**: Vignettes, Limericks, Ballads, Flash Fiction, Microfiction, Haiku, Listicles, and Wild Cards
- **🎬 Rich Genre Selection**: Core genres, flexible meta-genres, and exclusive PlaidVerse™ bonus genres
- **🌪️ Absurdity Levels**: From Mild to full Plaidemonium™
- **💬 OpenAI Assistants API**: Persistent conversation threads and stateful interactions
- **🎨 Premium Dark UI**: Beautiful, responsive design with smooth animations

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- OpenAI API key with access to GPT-4 and Assistants API

### Installation

1. **Clone or download this repository**
   ```bash
   cd openaiassistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-api-key-here
   ```

4. **Create the OpenAI Assistant**
   ```bash
   python setup_assistant.py
   ```
   
   This script will:
   - Create a new Assistant with the PlaidLibs system prompt
   - Display the Assistant ID
   - Optionally update your `.env` file

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open your browser** to `http://localhost:8501`

## 📁 Project Structure

```
openaiassistant/
├── app.py                 # Main Streamlit application
├── assistant.py           # OpenAI Assistants API integration
├── config.py              # Configuration (genres, forms, prompts)
├── setup_assistant.py     # Assistant creation script
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
├── .streamlit/
│   └── config.toml        # Streamlit theme configuration
├── documentation/         # PlaidLibs™ documentation
│   ├── 01_PLAIDLIBS™ MasterSystemPromptGold.docx
│   ├── 1_PlaidLibsCompleteGuardRailsSafetyGuide.docx
│   ├── 2_PlaidLibsCompleteProcessFlowNoMisstepGuide.docx
│   └── ...
└── readme.md              # This file
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | Your OpenAI API key | ✅ Yes |
| `OPENAI_ASSISTANT_ID` | The Assistant ID created by setup script | ✅ Yes |

### Customizing the Assistant

You can modify the system prompt in `setup_assistant.py` or update an existing assistant:

```python
from assistant import update_assistant, get_system_prompt

# Update instructions
update_assistant(
    assistant_id="asst_xxxxx",
    instructions=get_system_prompt("macquip")
)
```

## 🎮 Usage

### Lib-Ate Mode (Guided Story Creation)

1. **Choose Your Style**: Select a literary form (Limericks, Flash Fiction, etc.)
2. **Pick Your Genre**: From Comedy to PlaidVerse™ exclusives
3. **Set Absurdity Level**: How weird should it get?
4. **Provide Words**: Mad Libs-style word prompts
5. **Generate!**: Watch your unique story come to life

### PlaidChat Mode

Free-form conversation with your chosen Quip persona for brainstorming, remixing, or creative exploration.

## 🎨 Customization

### Adding New Quip Personas

Edit `config.py` to add new personalities:

```python
QUIP_PERSONAS["newquip"] = {
    "name": "NewQuip™",
    "epithet": "The Creative Catalyst",
    "description": "Your persona description",
    "icon": "🌟",
    "tone": "Warm and encouraging",
    "style_tags": ["friendly", "creative", "supportive"]
}
```

### Adding New Genres

```python
ALL_GENRES["new_genre"] = {
    "name": "New Genre",
    "description": "Description of this genre",
    "icon": "📖"
}
```

## 🔄 Updating Your Assistant

After modifying the system prompt or configuration, you can update your OpenAI Assistant:

```python
from openai import OpenAI
from config import get_system_prompt

client = OpenAI()
client.beta.assistants.update(
    assistant_id="asst_your_id",
    instructions=get_system_prompt("macquip")
)
```

## 📚 API Reference

### PlaidLibsAssistant Class

```python
from assistant import PlaidLibsAssistant

# Initialize
assistant = PlaidLibsAssistant()

# Create a new thread
thread_id = assistant.create_thread()

# Send a message and get response
response = assistant.send_message("Hello!")

# Stream a response
for chunk in assistant.stream_message("Tell me a story"):
    print(chunk, end="")

# Reset conversation
assistant.reset_conversation()
```

## 🛠️ Development

### Running in Development Mode

```bash
streamlit run app.py --server.runOnSave true
```

### Testing the Assistant

```python
python -c "
from assistant import PlaidLibsAssistant
a = PlaidLibsAssistant()
print(a.send_message('Hello, MacQuip!'))
"
```

## 📋 Deployment

### Streamlit Cloud

1. Push to GitHub
2. Connect to [Streamlit Cloud](https://streamlit.io/cloud)
3. Add secrets in the Streamlit dashboard:
   - `OPENAI_API_KEY`
   - `OPENAI_ASSISTANT_ID`

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

## 🔒 Security Notes

- Never commit your `.env` file
- Use environment variables in production
- The Assistant ID is safe to share; the API key is not
- All conversations are stored in OpenAI threads (review their data retention policies)

## 📖 Documentation

For detailed PlaidLibs™ documentation, see the `documentation/` folder:

- **Master System Prompt**: Core AI behavior and rules
- **Guardrails & Safety Guide**: Content moderation and safety
- **Process Flow Guide**: Detailed workflow specifications
- **Genre Compendium**: All available genres and their contracts
- **Literary Forms**: Supported writing formats
- **Quip Personas**: Character personality overlays

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is provided as-is for educational and creative purposes.

---

<p align="center">
  Made with 🧵 and ✨ by the PlaidLibs™ Team
</p>
