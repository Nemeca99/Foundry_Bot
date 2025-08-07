# 🔧 Configuration Guide

## Quick Setup

### 1. Run the Setup Script
```bash
python setup_bot.py
```

This interactive script will help you configure:
- Discord Bot Token
- Your Discord User ID
- Channel ID where the bot should respond

### 2. Manual Configuration

If you prefer to configure manually, create a `.env` file in the project root:

```env
# Discord Settings
DISCORD_TOKEN=your_discord_bot_token_here
ALLOWED_USERS=your_discord_user_id_here
ALLOWED_CHANNELS=your_channel_id_here
BOT_PREFIX=!

# LM Studio Settings
OLLAMA_BASE_URL=http://169.254.83.107:1234
OLLAMA_MODEL_NAME=qwen/qwen3-8b

# Text Generation Settings
MAX_TOKENS=1024
TEMPERATURE=0.85
TOP_P=0.92
TOP_K=50
REPEAT_PENALTY=1.15

# Learning Engine Settings
CHUNK_SIZE=1000
OVERLAP_SIZE=200
MAX_WORKERS=4
```

## Getting Your Discord Bot Token

### Step 1: Create a Discord Application
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Give your application a name (e.g., "Authoring Bot")
4. Click "Create"

### Step 2: Create a Bot
1. In your application, go to the "Bot" section
2. Click "Add Bot"
3. Click "Yes, do it!"

### Step 3: Get the Token
1. In the Bot section, click "Reset Token" or copy the existing token
2. **Keep this token secret!** Never share it publicly

### Step 4: Configure Bot Permissions
1. In the Bot section, scroll down to "Privileged Gateway Intents"
2. Enable:
   - ✅ Presence Intent
   - ✅ Server Members Intent
   - ✅ Message Content Intent

### Step 5: Invite Bot to Server
1. Go to the "OAuth2" > "URL Generator" section
2. Select scopes: `bot`
3. Select bot permissions:
   - ✅ Send Messages
   - ✅ Read Message History
   - ✅ Use Slash Commands
   - ✅ Embed Links
4. Copy the generated URL and open it in a browser
5. Select your server and authorize the bot

## Getting Your Discord User ID

### Method 1: Developer Mode
1. Open Discord
2. Go to User Settings > Advanced
3. Enable "Developer Mode"
4. Right-click your username
5. Select "Copy ID"

### Method 2: Bot Command
1. Add this bot to your server
2. Use the command: `!userid`
3. The bot will show your user ID

## Getting Channel ID

### Method 1: Developer Mode
1. Enable Developer Mode (see above)
2. Right-click the channel name
3. Select "Copy ID"

### Method 2: Bot Command
1. Use the command: `!channelid`
2. The bot will show the current channel ID

## Configuration Options

### Discord Settings
- `DISCORD_TOKEN`: Your bot's token from Discord Developer Portal
- `ALLOWED_USERS`: Comma-separated list of user IDs who can use the bot
- `ALLOWED_CHANNELS`: Comma-separated list of channel IDs where the bot responds
- `BOT_PREFIX`: Command prefix (default: `!`)

### LM Studio Settings
- `OLLAMA_BASE_URL`: LM Studio server URL (default: `http://169.254.83.107:1234`)
- `OLLAMA_MODEL_NAME`: Model name (default: `qwen/qwen3-8b`)

### Text Generation Settings
- `MAX_TOKENS`: Maximum tokens per response (default: `1024`)
- `TEMPERATURE`: Creativity level 0.0-1.0 (default: `0.85`)
- `TOP_P`: Nucleus sampling parameter (default: `0.92`)
- `TOP_K`: Top-k sampling parameter (default: `50`)
- `REPEAT_PENALTY`: Penalty for repetition (default: `1.15`)
- `REQUEST_TIMEOUT`: Request timeout in seconds (default: `600` - 10 minutes)

### Learning Engine Settings
- `CHUNK_SIZE`: Words per training chunk (default: `1000`)
- `OVERLAP_SIZE`: Overlap between chunks (default: `200`)
- `MAX_WORKERS`: Parallel processing threads (default: `4`)

## Testing Configuration

### Check Configuration
```bash
python config.py
```

### Test Model Connection
```bash
python test_model_connection.py
```

### Test Learning Engine
```bash
python test_learning.py
```

## Security Notes

### ⚠️ Important Security Guidelines:
1. **Never share your bot token** - Keep it secret
2. **Don't commit .env files** - They're in .gitignore for safety
3. **Use specific channels** - Don't allow bot in all channels
4. **Limit user access** - Only add trusted users to ALLOWED_USERS
5. **Regular token rotation** - Reset tokens periodically

### Environment File Security
The `.env` file is automatically ignored by git to protect your secrets:
```
# .gitignore
.env
*.env
```

## Troubleshooting

### Common Issues

**Bot not responding:**
- Check if bot is online in Discord
- Verify channel ID is correct
- Ensure bot has proper permissions

**"Not authorized" error:**
- Add your user ID to ALLOWED_USERS
- Check user ID format (numbers only)

**Model connection failed:**
- Verify LM Studio is running
- Check OLLAMA_BASE_URL is correct
- Ensure model is loaded in LM Studio

**Configuration errors:**
- Run `python config.py` to see detailed errors
- Check .env file format (no spaces around =)
- Verify all required fields are set

### Getting Help
1. Check the configuration: `python config.py`
2. Test model connection: `python test_model_connection.py`
3. Review the logs for error messages
4. Verify Discord bot permissions and channel access

## Example Configuration

Here's a complete example `.env` file:

```env
# Discord Settings
DISCORD_TOKEN=your_discord_bot_token_here
ALLOWED_USERS=123456789012345678,987654321098765432
ALLOWED_CHANNELS=1234567890123456789,9876543210987654321
BOT_PREFIX=!

# LM Studio Settings
OLLAMA_BASE_URL=http://169.254.83.107:1234
OLLAMA_MODEL_NAME=qwen/qwen3-8b

# Text Generation Settings
MAX_TOKENS=1024
TEMPERATURE=0.85
TOP_P=0.92
TOP_K=50
REPEAT_PENALTY=1.15
REQUEST_TIMEOUT=600

# Learning Engine Settings
CHUNK_SIZE=1000
OVERLAP_SIZE=200
MAX_WORKERS=4
```

## Next Steps

After configuration:
1. **Test the bot**: `python test_model_connection.py`
2. **Start the bot**: `python start_authoring_bot.py`
3. **Test Discord commands**: Try `!help` in your Discord channel
4. **Start learning**: `python start_learning.py --wikipedia-max-files 100` 