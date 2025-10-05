# FightBot 🥊

An AI-powered debate simulation system where two chatbots engage in automated debates on various topics using OpenAI's GPT models.

## Overview

FightBot creates autonomous debates between two AI chatbots with opposing viewpoints. The system simulates realistic debate scenarios where each bot takes turns presenting arguments, counterarguments, and rebuttals on a given topic.

## Features

- **Interactive Topic Selection**: Enter any debate topic and positions through user prompts
- **Autonomous Debate System**: Two AI bots debate automatically without human intervention
- **Customizable Roles**: Configure each bot with specific debate strategies and viewpoints
- **Controlled Debate Length**: Set maximum rounds or run unlimited debates
- **Real-time Conversation**: Bots respond to each other in real-time with live output
- **File-based Communication**: Alternative file-based communication system for asynchronous debates
- **Flexible Bot Personas**: Assign names and personalities to each debating bot
- **Comprehensive Logging**: All activities logged to temporary files with timestamps
- **Log Management**: Built-in utilities to view, search, and manage debate logs
- **Per-Round Logging**: Each debate session creates a separate temporary log file
- **Flexible AI Backend**: Built on OpenAI's GPT models with easy configuration
- **Graceful Interruption**: Stop debates anytime with Ctrl+C

## Project Structure

```
fightbot/
├── chatbot.py              # Main ChatBot class with debate functionality
├── bot_factory.py          # Bot creation factory with personality management
├── bot_personalities.json  # Configuration file for bot personalities and styles
├── debate_topics.json      # Predefined debate topics with categories and difficulty
├── topic_manager.py        # Standalone topic management utility
├── chat_file.py           # File-based chatbot implementation
├── reqaopenai.py          # OpenAI API wrapper and utilities
├── config.json            # OpenAI API configuration
├── example.py             # Example script demonstrating features
├── log_viewer.py          # Utility for viewing and managing debate logs
├── __init__.py            # Package initialization
└── README.md              # This file
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/fengqian-ayce/fightbot.git
cd fightbot
```

2. Install required dependencies:
```bash
pip install requests
```

3. Create a `config.json` file in the project root with your OpenAI API key:
```json
{
  "openAI": {
    "token": "your-openai-api-key-here"
  }
}
```

## Usage

### Quick Start

Try these commands to get started:

```bash
# Start a debate with interactive mode selection
python chatbot.py

# Show help information
python chatbot.py help

# Show all available personalities and debate styles
python example.py personalities

# Run a quick demo with predefined bots
python example.py demo

# See custom personality creation
python example.py custom
```

### Interactive Debate Setup

Run the main script for an interactive debate experience:

```bash
python chatbot.py
```

The system will first ask you to choose an input mode:

#### **1. File Mode** 
Choose from predefined topics stored in `debate_topics.json`:
- Quick selection from curated debate topics
- Topics include positions, categories, and difficulty levels
- Great for structured debates on popular issues

#### **2. Interactive Mode**
Enter your own custom topic and positions:
- Complete freedom to create any debate topic
- Option to save custom topics to the file for future use
- Perfect for unique or specialized debate subjects

#### **3. Browse Mode**
Advanced topic exploration with filtering and search:
- Browse by category (Technology, Environment, Healthcare, etc.)
- Filter by difficulty (Beginner, Intermediate, Advanced)
- Search topics by keywords
- View detailed topic descriptions

After selecting your mode and topic, the system will prompt you for:
- Bot names (optional)
- Bot personalities (from 8 available options)
- Debate style (formal, casual, oxford, town_hall)
- Maximum rounds (optional)

### Programmatic Debate Setup

```python
from bot_factory import BotFactory
from chatbot import start_debate

# Create factory and list available options
factory = BotFactory()
print("Available personalities:", list(factory.list_personalities().keys()))
print("Available styles:", list(factory.list_debate_styles().keys()))

# Create bots for any topic with specific personalities
topic = "Should artificial intelligence be regulated?"
position1 = "AI should be heavily regulated"
position2 = "AI should remain largely unregulated"

bot1, bot2 = factory.create_debate_pair(
    topic, position1, position2, 
    "Regulator", "FreemarketAI",
    personality1="logical",     # Uses facts and data
    personality2="contrarian",  # Challenges popular opinions
    debate_style="formal"       # Formal debate format
)

# Start the debate with appropriate opening
opening_prompt = factory.get_opening_prompt("formal")
start_debate(bot1, bot2, initial_prompt=opening_prompt, max_rounds=5)
```

### Manual Configuration

For advanced users who want full control:

```python
from chatbot import ChatBot

# Configure first bot manually
cb1_config = [{
    "role": "system",
    "content": "Act like you're in a public debate. Your strength is emotional arguments. You support universal healthcare."
}]

# Configure second bot manually
cb2_config = [{
    "role": "system", 
    "content": "Act like you're in a public debate. Use balanced strategy and watch for logical fallacies. You support private healthcare."
}]

# Create and initialize bots
cb1 = ChatBot('UniversalCare')
cb1.create_role(cb1_config)

cb2 = ChatBot('PrivateCare')  
cb2.create_role(cb2_config)

# Start manual debate loop
response = cb2.add_response("Universal healthcare is too expensive")
while True:
    response1 = cb1.add_response(response)
    response2 = cb2.add_response(response1)
    response = response2
```

### File-based Communication

For asynchronous debates using file I/O:

```python
from chat_file import ChatBot

# Create bots that communicate via files
cb1 = ChatBot(filename='./chat1.txt', response='./chat2.txt')
cb2 = ChatBot(filename='./chat2.txt', response='./chat1.txt')

# Start file-based communication
cb1.read()  # Bot 1 monitors chat1.txt and responds to chat2.txt
cb2.read()  # Bot 2 monitors chat2.txt and responds to chat1.txt
```

### Direct API Usage

You can also use the OpenAI wrapper directly:

```python
from reqaopenai import AutoText

at = AutoText()

# Single chat completion
response = at.chat_single("Hello, how are you?")

# Chat with conversation history
messages = [{"role": "system", "content": "You are a helpful assistant"}]
response = at.chat("What's the weather like?", messages)
```

## Configuration

### Bot Personalities

The system includes 8 pre-configured bot personalities in `bot_personalities.json`:

1. **Emotional**: Makes passionate, emotional arguments with personal stories
2. **Logical**: Uses facts, data, and logical reasoning
3. **Balanced**: Mixed approach attacking opponent's points while explaining own position
4. **Aggressive**: Directly challenges opponents with strong rhetoric
5. **Diplomatic**: Uses respectful language while finding common ground
6. **Contrarian**: Enjoys challenging popular opinions and finding argument flaws
7. **Academic**: Uses scholarly language and theoretical frameworks
8. **Populist**: Appeals to common people with simple, relatable language

### Debate Topics

The system includes 10 predefined debate topics in `debate_topics.json` covering various categories:

**Categories Available:**
- **Technology**: AI regulation, social media, cryptocurrency
- **Environment**: Climate vs economy, nuclear energy
- **Healthcare**: Universal healthcare systems
- **Workplace**: Remote work, gig economy
- **Science**: Space exploration, genetic engineering
- **Finance**: Traditional vs crypto banking

**Difficulty Levels:**
- **Beginner**: Simple topics with clear sides (remote work, social media)
- **Intermediate**: Balanced complexity (AI regulation, healthcare, space)
- **Advanced**: Complex topics requiring expertise (climate policy, nuclear energy, genetics)

### Debate Styles

Four debate formats are available:

- **Formal**: Structured debate with formal opening statements
- **Casual**: Conversational but substantive discussion
- **Oxford**: Oxford Union style with formal language
- **Town Hall**: Community meeting format for citizen concerns

### Factory Configuration

```python
from bot_factory import BotFactory

# Create custom personality
factory = BotFactory()
factory.add_personality(
    personality_id="custom_id",
    name="Custom Personality",
    description="Your custom description",
    system_prompt="Your custom system prompt template"
)
```

### ChatBot Parameters

- `name`: Identifier for the bot (used in logging)
- `output`: File path for saving responses (default: 'response.txt')
- `config`: List of system messages defining the bot's role and behavior

### AutoText Parameters

- `text_source`: AI service to use (currently only 'openai' supported)
- `token`: OpenAI API key (can be passed directly or loaded from config.json)

## API Features

The `AutoText` class provides:

- **Model Management**: List and retrieve available OpenAI models
- **Completions**: Generate text completions using GPT models
- **Chat**: Interactive chat with conversation context
- **Error Handling**: Robust error handling for API requests

## Example Debate Topics

The system works well with controversial topics that have clear opposing sides:

- Big Government vs Small Government (included example)
- Climate Change Policy
- Economic Systems (Capitalism vs Socialism)
- Technology Ethics
- Educational Policy
- Healthcare Systems

## Logging

The system includes comprehensive logging:
- Bot responses and conversation flow
- API request details
- Error handling and debugging information
- Conversation history tracking

## Requirements

- Python 3.6+
- `requests` library
- OpenAI API key
- Internet connection for API calls

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source. Please check the repository for license details.

## Notes

- The system uses OpenAI's GPT-3.5-turbo model by default
- API costs apply for OpenAI usage
- Debates can run indefinitely - implement stopping conditions as needed
- File-based communication allows for persistent debates across sessions

## Logging System

FightBot includes comprehensive logging that captures all debate activities in temporary files.

### Automatic Logging

Every debate session automatically creates:
- **Temporary log directory**: Created in system temp folder with unique timestamp
- **Debate log file**: Contains full conversation history, round-by-round
- **Bot-specific logs**: Individual bot responses and internal processing
- **Error logs**: API errors, connection issues, and other problems

### Log Management Utility

Use the `log_viewer.py` utility to manage debate logs:

```bash
# List all available logs
python log_viewer.py list

# View a specific log (use index from list command)
python log_viewer.py view --index 1

# View last 20 lines of a log
python log_viewer.py view --index 1 --lines 20 --tail

# Search for specific terms in logs
python log_viewer.py search --term "climate change"

# Clean up logs older than 7 days
python log_viewer.py cleanup --days 7
```

### Topic Management Utility

Use the standalone topic manager for advanced topic management:

```bash
# Interactive topic management
python topic_manager.py

# List all available topics
python topic_manager.py list

# View topics organized by category  
python topic_manager.py categories

# View topics organized by difficulty
python topic_manager.py difficulties

# Show help for topic manager
python topic_manager.py help
```

### Log Format

Logs use structured format with timestamps:
```
2025-10-03 22:23:30 - DebateSession - INFO - === DEBATE STARTED ===
2025-10-03 22:23:30 - DebateSession - INFO - Bot 1: EconomyFirst
2025-10-03 22:23:30 - DebateSession - INFO - Bot 2: GreenAdvocate
2025-10-03 22:23:31 - DebateSession - INFO - ROUND 1 - EconomyFirst: Economic growth is essential...
```

### Log Types

- **DebateSession**: Main debate flow and conversation
- **ChatBot_[name]**: Individual bot responses and processing
- **BotFactory**: Bot creation and personality loading
- **OpenAIAPI**: API requests and responses (debug level)
- **Console**: User interface and real-time feedback

## Troubleshooting

**API Key Issues**: Ensure your `config.json` file is properly formatted and contains a valid OpenAI API key.

**Request Errors**: Check your internet connection and API key validity. The system includes error handling for common API issues.

**File Permissions**: For file-based communication, ensure the application has read/write permissions in the working directory.

**Log Files**: If you can't find debate logs, use `python log_viewer.py list` to see all available logs with their locations.
