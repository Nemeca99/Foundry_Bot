# Discord Directory

This directory contains the Discord bot interface that allows users to interact with the Authoring Bot through Discord.

## Files

### `authoring_bot.py`
The main Discord bot implementation that:
- Connects to Discord using the bot token
- Handles all Discord events (messages, reactions, etc.)
- Processes commands with `!` prefix for bot functionality
- Processes `@` mentions for direct model interaction
- Manages user sessions and conversation context
- Integrates with the framework plugins for all bot functionalities

## Core Directory (`core/`)
Currently empty, but designed for Discord-specific utilities and extensions.

## Command Structure

### `!` Commands (Bot Commands)
- `!help` - Shows available commands and usage
- `!create-project <name> <genre> <target_audience> <word_count>` - Creates a new writing project
- `!personality-test <type>` - Starts a personality test (writing_style, communication_style, learning_preferences)
- `!test-answer <session_id> <question_id> <answer_index>` - Submits answers to personality test questions
- `!learning-summary` - Shows Luna's learning progress and personality evolution
- `!modify-message <type> <message>` - Modifies messages for better understanding
- `!reward-learning <activity> <level>` - Rewards Luna for learning activities (testing)
- `!punish-learning <opportunity> <severity>` - Punishes Luna for missed learning opportunities (testing)
- `!personalize analyze` - Analyzes user's writing style
- `!personality show` - Shows Luna's current personality

### `@` Mentions (Direct Model Interaction)
- `@Luna <message>` - Direct interaction with the AI model for natural conversation
- Used for creative writing assistance, story development, character creation, etc.

## How It Works

1. **Bot Initialization**: The bot connects to Discord and loads all framework plugins
2. **Message Processing**: 
   - Messages starting with `!` are processed as bot commands
   - Messages mentioning the bot with `@` are sent to the AI model for natural language processing
3. **Plugin Integration**: All bot functionality is handled by framework plugins
4. **Session Management**: The bot maintains conversation context and user sessions
5. **Error Handling**: Graceful error handling for invalid commands and API failures

## Configuration

The bot uses settings from `config.py` including:
- Bot token and prefix
- Model connection settings
- Plugin configurations
- Logging settings

## Usage

Users interact with the bot through Discord by:
- Using `!` commands for structured bot functionality
- Using `@` mentions for natural language AI interaction
- The bot provides comprehensive authoring assistance including writing guidance, personality tests, learning features, and content generation 