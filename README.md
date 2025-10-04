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
- **Comprehensive Logging**: Monitor debate progress and conversation flow
- **Flexible AI Backend**: Built on OpenAI's GPT models with easy configuration
- **Graceful Interruption**: Stop debates anytime with Ctrl+C

## Project Structure

```
fightbot/
├── chatbot.py          # Main ChatBot class with debate functionality
├── chat_file.py        # File-based chatbot implementation
├── reqaopenai.py       # OpenAI API wrapper and utilities
├── __init__.py         # Package initialization
└── README.md           # This file
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

### Interactive Debate Setup

Run the main script for an interactive debate experience:

```bash
python chatbot.py
```

The system will prompt you to enter:
- Debate topic
- First position 
- Opposing position
- Bot names (optional)
- Maximum rounds (optional)

### Programmatic Debate Setup

```python
from chatbot import create_debate_bots, start_debate

# Create bots for any topic
topic = "Should artificial intelligence be regulated?"
position1 = "AI should be heavily regulated"
position2 = "AI should remain largely unregulated"

bot1, bot2 = create_debate_bots(topic, position1, position2, "Regulator", "FreemarketAI")

# Start the debate with optional round limit
start_debate(bot1, bot2, max_rounds=5)
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

## Troubleshooting

**API Key Issues**: Ensure your `config.json` file is properly formatted and contains a valid OpenAI API key.

**Request Errors**: Check your internet connection and API key validity. The system includes error handling for common API issues.

**File Permissions**: For file-based communication, ensure the application has read/write permissions in the working directory.
