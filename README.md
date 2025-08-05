# Authoring Bot - Your Personal AI Writing Assistant

**Authoring Bot** is a comprehensive AI-powered writing assistant that helps you create, manage, and monetize your authoring projects. Built with local LLM integration, it provides text, image, video, and voice generation capabilities through a Discord interface with personalized writing assistance.

## 📁 Project Structure

The project is organized into logical folders for easy navigation:

```
Foundry_Bot/
├── 📁 framework/          # Main framework and plugins
├── 📁 discord/           # Discord bot interface
├── 📁 scripts/           # Utility scripts and tools
│   ├── 📁 tests/        # Test scripts
│   ├── 📁 tools/        # Development tools
│   └── 📁 performance/  # Performance testing
├── 📁 docs/             # Documentation and guides
├── 📁 models/           # AI models and training data
├── 📁 Book_Collection/  # Your writing samples
└── 📁 media/           # Generated content output
```

See `PROJECT_STRUCTURE.md` for detailed folder organization.

## 🚀 Features

### **Text Generation**
- **Chapter Writing** - Generate complete chapters with plot progression
- **Character Development** - Create detailed character profiles and arcs
- **Plot Generation** - Develop comprehensive story outlines
- **Story Writing** - Write complete short stories and novels
- **Dialogue Generation** - Create character-specific dialogue
- **Description Writing** - Generate vivid scene descriptions

### **Media Generation**
- **Book Covers** - Generate professional book covers by genre
- **Book Trailers** - Create promotional video trailers
- **Audiobook Narration** - Convert chapters to audio narration
- **Character Art** - Generate character illustrations
- **Scene Illustrations** - Create visual scene depictions

### **Project Management**
- **Project Tracking** - Manage multiple writing projects
- **Progress Monitoring** - Track word count and completion goals
- **Character Database** - Organize character profiles and relationships
- **Plot Development** - Structure story arcs and plot points
- **Sales Tracking** - Monitor revenue and royalties

### **Business Tools**
- **Sales Analytics** - Track book performance and revenue
- **Market Analysis** - Research genre trends and opportunities
- **Writing Statistics** - Monitor writing habits and productivity
- **Financial Tracking** - Manage author income and expenses

### **AI-Powered Features**
- **Personalization Engine** - Learns from your writing style and adapts responses
- **Learning Engine** - Processes large datasets (Wikipedia, your books) for training
- **Tool Use** - Advanced function calling for enhanced authoring capabilities
- **Hardware Optimization** - Automatically optimized for your system specifications

## 🏗️ Architecture

### **Core Components**
- **Framework Core** (`framework/framework_tool.py`) - Main orchestration system
- **Discord Interface** (`discord/authoring_bot.py`) - Discord bot commands
- **Plugin System** - Modular capabilities for different media types

### **Plugin System**
- **Text Generator** (`framework/plugins/text_generator.py`) - Story and content generation
- **Image Generator** (`framework/plugins/image_generator.py`) - Visual content creation
- **Video Generator** (`framework/plugins/video_generator.py`) - Video content generation
- **Voice Generator** (`framework/plugins/voice_generator.py`) - Audio narration and TTS

## 🎯 Discord Commands

### **Project Management**
```
!create-project <name> <genre> <audience> <word_count>
!list-projects
!project-info <name>
```

### **Text Generation**
```
!write-chapter <project> <title> <requirements>
!develop-character <project> <name> <requirements>
!generate-plot <project> <requirements>
!write-story <genre> <audience> <requirements>
```

### **Media Generation**
```
!generate-cover <project> <description>
!create-trailer <project> <description>
!narrate-chapter <project> <chapter_number>
```

### **Business Tracking**
```
!track-sales <project> <revenue> <royalties>
!get-stats
!analyze-market <genre>
```

### **AI-Powered Commands**
```
!personalize analyze          # Analyze your writing style
!personalize suggestions      # Get personalized writing tips
!personalize stats           # Show personalization statistics
!tools <message>             # Use AI tools for advanced tasks
!learning-stats              # Show learning engine statistics
```

### **Message Handling**
The bot automatically handles long messages by splitting them into multiple parts when they exceed Discord's 2000 character limit. Each part is sent with a continuation indicator.

### **Utility**
```
!help
!status
```

## 🛠️ Setup Instructions

### **1. Environment Setup**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### **2. Hardware Optimization**
```bash
# Scan your system and get optimized settings
python scripts/tools/hardware_scan.py

# Test performance with optimized settings
python scripts/performance/test_optimized_performance.py
```

### **2. Configuration**
Create a `.env` file in the project root:
```env
DISCORD_TOKEN=your_discord_bot_token
OLLAMA_BASE_URL=http://localhost:1234
OLLAMA_MODEL_NAME=cognitivecomputations_dolphin-mistral-24b-venus-edition
ALLOWED_USERS=your_discord_user_id
ALLOWED_CHANNELS=your_discord_channel_id
BOT_PREFIX=!
```

### **3. Local LLM Setup**
Ensure you have LM Studio or Ollama running locally with a compatible model.

### **4. Start the Bot**
```bash
python scripts/start_authoring_bot.py
```

## 🧪 Testing & Development

### **Running Tests**
```bash
# Test the main bot functionality
python scripts/tests/test_authoring_bot.py

# Test personalization features
python scripts/tests/test_personalization.py

# Test tool use functionality
python scripts/tests/test_tool_use.py

# Test learning engine
python scripts/tests/test_learning.py
```

### **Development Tools**
```bash
# Debug LM Studio connection
python scripts/tools/debug_lm_studio.py

# Quick connection test
python scripts/tools/quick_test.py

# Hardware scan and optimization
python scripts/tools/hardware_scan.py
```

## 🎯 Hardware Optimization

Your system has been scanned and optimized:
- **OS**: Windows 11
- **CPU**: 8-core Intel (16 logical cores)
- **RAM**: 32GB (High Performance)
- **GPU**: NVIDIA GeForce RTX 3060 Ti (8GB VRAM)
- **Performance Score**: 10/10 (Perfect!)

The bot is configured with optimal settings for your high-performance system.

## 📊 Usage Examples

### **Creating Your First Project**
```
!create-project "My Fantasy Novel" "Fantasy" "Young Adult" 80000
```

### **Writing a Chapter**
```
!write-chapter "My Fantasy Novel" "The Dragon's Call" "Write an opening chapter that introduces a young wizard discovering their magical abilities"
```

### **Developing a Character**
```
!develop-character "My Fantasy Novel" "Aria" "A 16-year-old wizard apprentice with a mysterious past and hidden powers"
```

### **Generating a Book Cover**
```
!generate-cover "My Fantasy Novel" "A mystical forest with glowing runes and a young wizard in robes"
```

### **Creating a Book Trailer**
```
!create-trailer "My Fantasy Novel" "Epic fantasy adventure with magic, dragons, and a young hero's journey"
```

### **Tracking Sales**
```
!track-sales "My Fantasy Novel" 1500.00 450.00
```

## 🔧 Plugin Development

### **Creating a New Plugin**
1. Create a new file in `framework/plugins/`
2. Implement the plugin class with an `initialize(framework)` function
3. The framework will automatically load and register the plugin

### **Plugin Interface**
```python
class MyPlugin:
    def __init__(self, framework):
        self.framework = framework
        # Initialize plugin
    
    def my_function(self, *args):
        # Plugin functionality
        pass

def initialize(framework):
    return MyPlugin(framework)
```

## 📈 Monetization Strategy

### **Revenue Streams**
- **Book Sales** - Track revenue from book sales
- **Audiobook Sales** - Monitor audiobook performance
- **Merchandise** - Track related product sales
- **Speaking Engagements** - Monitor speaking income
- **Teaching** - Track writing course revenue

### **Business Analytics**
- **Sales Tracking** - Monitor book performance over time
- **Market Analysis** - Research genre trends and opportunities
- **Reader Analytics** - Understand your audience
- **Financial Planning** - Plan for sustainable author income

## 🎭 Personality & Style

The Authoring Bot maintains a professional, encouraging personality that:
- **Motivates** - Provides positive reinforcement for writing progress
- **Guides** - Offers constructive feedback and suggestions
- **Organizes** - Helps structure and manage complex projects
- **Analyzes** - Provides data-driven insights for business decisions
- **Creates** - Generates high-quality content across all media types

## 🔒 Security & Permissions

- **User Authorization** - Only authorized users can access the bot
- **Channel Restrictions** - Commands only work in designated channels
- **Data Privacy** - All project data is stored locally
- **Content Safety** - Generated content follows ethical guidelines

## 🚀 Future Enhancements

### **Planned Features**
- **Advanced AI Models** - Integration with cutting-edge language models
- **Real-time Collaboration** - Multi-author project support
- **Publishing Integration** - Direct publishing platform connections
- **Advanced Analytics** - Deep market and reader insights
- **Mobile Interface** - Mobile app for on-the-go writing

### **Media Generation**
- **Advanced Image Generation** - High-quality book covers and illustrations
- **Video Production** - Professional book trailers and promotional content
- **Audiobook Creation** - Full audiobook production pipeline
- **3D Content** - Interactive 3D book previews

## 🤝 Contributing

This project follows the Astra framework architecture. When contributing:
1. Follow the BULMA header protocol
2. Test all changes thoroughly
3. Maintain backward compatibility
4. Document new features
5. Follow the existing code style

## 📄 License

This project is built on the Astra framework and follows its licensing terms.

---

**Ready to start your authoring journey?** Set up the bot and begin creating your next masterpiece! 🚀 