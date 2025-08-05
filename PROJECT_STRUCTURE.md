# 🌟 Foundry Bot - Project Structure

## 📁 **MAIN DIRECTORY STRUCTURE**

```
Foundry_Bot/
├── 📄 start_bot.py              # Main entry point for Discord bot
├── 📄 run_tests.py              # Main entry point for running tests
├── 📄 health_check.py           # Main entry point for health checks
├── 📄 setup.py                  # Main entry point for setup
├── 📄 config.py                 # Configuration settings
├── 📄 requirements.txt          # Python dependencies
├── 📄 .env                      # Environment variables (Discord token, etc.)
├── 📄 README.md                 # Project documentation
├── 📄 PROJECT_STRUCTURE.md      # This file
├── 📄 LUNA_CAPABILITIES_DOCUMENTATION.md  # Luna's capabilities
├── 📄 DISCORD_COMMANDS_GUIDE.md # Discord commands guide
│
├── 🧠 core/                     # Core system files
│   ├── 📁 utils/                # Utility functions
│   │   ├── 📄 system_health.py  # System health checker
│   │   └── 📄 status_summary.py # Status summary generator
│   ├── 📁 tests/                # Test files
│   │   ├── 📄 run_all_tests.py  # Comprehensive test runner
│   │   ├── 📄 test_model_connection.py
│   │   ├── 📄 test_writing_assistant.py
│   │   ├── 📄 test_personality.py
│   │   ├── 📄 test_personalization.py
│   │   ├── 📄 test_tool_use.py
│   │   ├── 📄 test_message_splitting.py
│   │   ├── 📄 test_learning.py
│   │   └── 📄 test_authoring_bot.py
│   ├── 📁 deployment/           # Deployment scripts
│   │   └── 📄 deploy.py         # Complete deployment process
│   └── 📁 setup/                # Setup scripts
│       └── 📄 setup_bot.py      # Bot setup and configuration
│
├── 🤖 discord/                  # Discord bot interface
│   └── 📄 authoring_bot.py      # Main Discord bot with all commands
│
├── 🔧 framework/                # Core framework and plugins
│   ├── 📄 framework_tool.py     # Main framework orchestrator
│   └── 📁 plugins/              # Plugin system
│       ├── 📄 text_generator.py      # Text generation (LM Studio)
│       ├── 📄 personality_engine.py  # Luna's personality system
│       ├── 📄 writing_assistant.py   # Sudowrite-inspired features
│       ├── 📄 personalization_engine.py # User style learning
│       ├── 📄 tool_manager.py        # AI tool use system
│       ├── 📄 learning_engine.py     # Data processing engine
│       ├── 📄 image_generator.py     # Image generation (placeholder)
│       ├── 📄 video_generator.py     # Video generation (placeholder)
│       └── 📄 voice_generator.py     # Voice generation (placeholder)
│
├── 📚 Book_Collection/          # User's writing samples for learning
│   ├── 📁 Anna/
│   ├── 📁 Eve/
│   ├── 📁 Mavlon/
│   ├── 📁 Random/
│   ├── 📁 Relic/
│   └── 📁 Shadow/
│
├── 📊 data/                     # Persistent data storage
│   ├── 📄 projects.json         # Project data
│   ├── 📄 stats.json           # Statistics
│   └── 📄 personality_data.json # Luna's personality data
│
├── 🖼️ image/                    # Image generation files
│   ├── 📁 input/               # Input images
│   └── 📁 output/              # Generated images
│
├── 🎬 video/                    # Video generation files
│   ├── 📁 input/               # Input videos
│   └── 📁 output/              # Generated videos
│
├── 🎤 voice/                    # Voice generation files
│   ├── 📁 input/               # Input audio
│   └── 📁 output/              # Generated audio
│
├── 🤖 models/                   # Model files and configurations
│
├── 👤 profile/                  # User and bot profiles
│   ├── 📁 bot_profile/         # Luna's profile data
│   │   └── 📁 personality/     # Personality traits and learning
│   └── 📁 user_profile/        # User preferences and data
│
└── 📖 docs/                     # Documentation
    ├── 📄 API_REFERENCE.md     # API documentation
    ├── 📄 DEPLOYMENT_GUIDE.md  # Deployment instructions
    └── 📄 TROUBLESHOOTING.md   # Common issues and solutions
```

## 🚀 **QUICK START COMMANDS**

### **Start the Discord Bot:**
```bash
python start_bot.py
```

### **Run Health Check:**
```bash
python health_check.py
```

### **Run All Tests:**
```bash
python run_tests.py
```

### **Setup the Bot:**
```bash
python setup.py
```

## 🎯 **KEY FEATURES BY DIRECTORY**

### **🧠 Core (`core/`)**
- **System utilities** for health checks and status monitoring
- **Comprehensive test suite** for all components
- **Deployment scripts** for easy setup
- **Setup tools** for configuration

### **🤖 Discord (`discord/`)**
- **Natural language chatbot** - Just @mention Luna to chat
- **Command system** - All `!commands` for writing assistance
- **Message splitting** - Handles long responses automatically
- **Error handling** - Graceful error management

### **🔧 Framework (`framework/`)**
- **Plugin architecture** - Modular, extensible system
- **LM Studio integration** - Local AI model connection
- **Data persistence** - Saves all projects and learning
- **Tool use system** - Advanced AI capabilities

### **📚 Book Collection (`Book_Collection/`)**
- **User's writing samples** - For style learning
- **Organized by project** - Easy to manage
- **Learning data** - Powers personalization

## 🌟 **LUNA'S CAPABILITIES**

### **Natural Conversation:**
- **@mention responses** - Chat naturally with Luna
- **Context awareness** - Remembers conversation history
- **Personality adaptation** - Learns your communication style

### **Writing Assistance (Sudowrite-inspired):**
- **Story continuation** - Continue from where you left off
- **Scene expansion** - Add detail to rushed scenes
- **Description generation** - Rich, vivid descriptions
- **Dialogue creation** - Natural character conversations
- **Plot development** - Story structure and arcs
- **Character development** - Comprehensive character profiles
- **World building** - Setting and lore creation
- **Name generation** - Creative names for characters/places
- **Plot twists** - Unexpected story developments

### **Project Management:**
- **Create projects** - Organize your writing
- **Track progress** - Word counts and milestones
- **Chapter management** - Organize story structure
- **Character tracking** - Maintain character bibles

### **AI Tools:**
- **Natural language requests** - "Create a fantasy character"
- **Market analysis** - Publishing insights
- **Content generation** - Promotional materials
- **Style analysis** - Learn your writing patterns

## 🔧 **TECHNICAL ARCHITECTURE**

### **Plugin System:**
- **Modular design** - Easy to add new features
- **Hot reloading** - Update plugins without restart
- **Error isolation** - One plugin failure doesn't crash the system

### **Data Persistence:**
- **JSON storage** - Human-readable data files
- **Automatic backups** - Data safety
- **Version control** - Track changes over time

### **Performance:**
- **Async operations** - Non-blocking Discord responses
- **Message splitting** - Handle Discord's 2000 char limit
- **Timeout handling** - Graceful error recovery
- **Resource monitoring** - System health tracking

## 🎯 **DEVELOPMENT WORKFLOW**

### **Test → Refine → Test → Log**
1. **Test** - Run `python run_tests.py`
2. **Refine** - Fix issues and improve features
3. **Test** - Verify fixes work
4. **Log** - Document changes and learnings

### **Health Monitoring:**
- **Regular checks** - `python health_check.py`
- **System status** - Monitor all components
- **Recommendations** - Get suggestions for improvements

## 🌟 **SUCCESS METRICS**

### **Functional:**
- ✅ Discord bot responds to @mentions
- ✅ All commands work properly
- ✅ Message splitting handles long responses
- ✅ Health check passes all components
- ✅ Tests run successfully

### **User Experience:**
- ✅ Natural conversation flow
- ✅ Helpful writing assistance
- ✅ Learning and adaptation
- ✅ Clean, organized structure

---

**🎉 Foundry Bot is now properly organized and ready for development!** 