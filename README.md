# AI Writing Companion

An advanced AI-powered writing assistant with multimodal capabilities, emotional intelligence, and comprehensive project management.

## 🚀 Quick Start

### Launch Script
Use the convenient launch script to access all components:

```bash
# System management
python launch.py dashboard     # Launch system dashboard
python launch.py analytics     # Launch analytics dashboard
python launch.py projects      # Launch project manager

# Bot management
python launch.py bot           # Start Discord bot
python launch.py tests         # Run test suite

# Documentation
python launch.py docs          # Open documentation
python launch.py help          # Show help
```

### Direct Script Access
```bash
# Core system components
python core/system_dashboard.py --monitor
python core/analytics_dashboard.py --system-report
python core/project_manager.py --list

# Scripts
python scripts/start_bot.py
python scripts/run_tests.py
python scripts/setup.py
```

## 📁 Project Structure

```
Foundry_Bot/
├── launch.py                          # Main launcher script
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── .gitignore                        # Git ignore rules
│
├── core/                             # Core system components
│   ├── system_dashboard.py           # System monitoring dashboard
│   ├── analytics_dashboard.py        # Analytics and insights
│   ├── project_manager.py            # Project management system
│   ├── health_check.py               # System health monitoring
│   ├── config.py                     # Configuration management
│   └── tests/                        # Test files
│       ├── test_enhanced_multimodal_systems.py
│       ├── test_enhanced_psychological_emotions.py
│       └── test_multimodal_system.py
│
├── framework/                        # Core framework
│   ├── framework_tool.py             # Main framework tool
│   └── plugins/                      # Framework plugins
│       ├── enhanced_image_generator.py
│       ├── enhanced_voice_generator.py
│       ├── enhanced_video_generator.py
│       ├── enhanced_audio_processor.py
│       ├── multimodal_orchestrator.py
│       ├── writing_assistant.py
│       ├── personality_engine.py
│       ├── personalization_engine.py
│       ├── learning_engine.py
│       ├── tool_manager.py
│       └── text_generator.py
│
├── discord/                          # Discord bot interface
│   ├── authoring_bot.py              # Main Discord bot
│   ├── enhanced_multimodal_commands.py
│   └── core/                         # Discord core components
│
├── astra_emotional_fragments/        # Emotional system
│   ├── emotional_blender.py          # Enhanced emotional blending
│   ├── dynamic_emotion_engine.py     # Dynamic emotion engine
│   ├── breaking.md                   # Emotional fragments
│   ├── cold.md
│   ├── defiant.md
│   ├── flustered.md
│   ├── nurturing.md
│   ├── obsessed.md
│   └── reverent.md
│
├── multimodal/                       # Multimodal systems
│   ├── image/                        # Image generation
│   │   ├── enhanced_image_generator.py
│   │   ├── input/
│   │   └── output/
│   ├── voice/                        # Voice generation
│   │   ├── enhanced_voice_generator.py
│   │   ├── input/
│   │   └── output/
│   ├── video/                        # Video generation
│   │   ├── enhanced_video_generator.py
│   │   ├── input/
│   │   └── output/
│   └── audio/                        # Audio processing
│       ├── enhanced_audio_processor.py
│       ├── input/
│       └── output/
│
├── profile/                          # User and personality management
│   ├── bot_profile/                  # AI personality profiles
│   │   ├── personality/
│   │   │   ├── personality_creator.py
│   │   │   └── personality_manager.py
│   │   └── CHARACTER_ROLEPLAY_GUIDE.md
│   ├── user_profile/                 # User profile management
│   │   └── user_profile_manager.py
│   ├── CHARACTER_ROLEPLAY_GUIDE.md
│   └── PERSONALITY_SYSTEM_GUIDE.md
│
├── data/                             # Data management
│   ├── user_data/                    # User interaction data
│   ├── training_data/                # AI training data
│   ├── analytics/                    # System analytics
│   ├── backups/                      # Data backups
│   └── exports/                      # Data exports
│
├── Book_Collection/                  # Writing projects
│   ├── Anna/                         # Author projects
│   ├── Eve/
│   ├── Mavlon/
│   ├── Random/
│   ├── Relic/
│   └── Shadow/
│
├── docs/                             # Documentation
│   ├── guides/                       # User guides
│   │   ├── ENHANCED_MULTIMODAL_GUIDE.md
│   │   └── DISCORD_COMMANDS_GUIDE.md
│   ├── summaries/                    # System summaries
│   │   ├── PSYCHOLOGICAL_EMOTIONAL_SYSTEM_SUMMARY.md
│   │   ├── MULTIMODAL_SYSTEM_SUMMARY.md
│   │   └── ENHANCED_FEATURES_SUMMARY.md
│   ├── PROJECT_STRUCTURE.md
│   └── LUNA_CAPABILITIES_DOCUMENTATION.md
│
├── scripts/                          # Utility scripts
│   ├── start_bot.py                  # Discord bot launcher
│   ├── run_tests.py                  # Test runner
│   └── setup.py                      # Setup script
│
├── models/                           # AI models and data
├── .venv/                           # Python virtual environment
└── __pycache__/                     # Python cache
```

## 🎯 Core Features

### 🤖 AI Writing Assistant
- **Writing Assistance**: Generate chapters, develop characters, create plots
- **Content Enhancement**: Rewrite, expand, and improve existing content
- **Creative Collaboration**: Brainstorm ideas and develop story elements
- **Genre Adaptation**: Adapt writing style for different genres

### 🎭 Emotional Intelligence
- **Psychological Models**: Plutchik's Wheel of Emotions and Maslow's Hierarchy
- **Dynamic Emotions**: Real-time emotional adaptation and context switching
- **Emotional Blending**: Sophisticated emotional state management
- **Personality Development**: Character personality evolution

### 🎨 Multimodal Capabilities
- **Image Generation**: Stable Diffusion integration with multiple styles
- **Voice Generation**: Multiple TTS engines (pyttsx3, gTTS, ElevenLabs)
- **Video Generation**: Video creation with various APIs and effects
- **Audio Processing**: Sound effects, ambient audio, and audio enhancement
- **Multimodal Orchestration**: Unified coordination of all media types

### 📊 Project Management
- **Project Organization**: Comprehensive project tracking and management
- **Chapter Management**: Chapter creation, editing, and progress tracking
- **Character Development**: Character profiles and development tracking
- **AI Integration**: AI-powered suggestions and assistance
- **Progress Analytics**: Detailed progress tracking and statistics

### 📈 Analytics & Monitoring
- **System Dashboard**: Real-time system health monitoring
- **Analytics Dashboard**: User behavior and system performance analytics
- **Performance Insights**: Data-driven optimization recommendations
- **Usage Tracking**: Comprehensive usage pattern analysis

### 🎮 Discord Integration
- **Natural Language**: @mention functionality for natural conversation
- **Command System**: Comprehensive Discord command interface
- **Multimodal Commands**: Image, voice, video, and audio generation
- **Enhanced Commands**: Advanced multimodal capabilities
- **Real-time Interaction**: Live system interaction and monitoring

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- Discord Bot Token
- Required API keys (optional for enhanced features)

### Installation
```bash
# Clone the repository
git clone https://github.com/Nemeca99/Foundry_Bot.git
cd Foundry_Bot

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp config.py.example config.py
# Edit config.py with your settings
```

### Quick Launch
```bash
# Launch system dashboard
python launch.py dashboard

# Start Discord bot
python launch.py bot

# Run analytics
python launch.py analytics --system-report

# Manage projects
python launch.py projects --list
```

## 📚 Documentation

### User Guides
- [Enhanced Multimodal Guide](docs/guides/ENHANCED_MULTIMODAL_GUIDE.md)
- [Discord Commands Guide](docs/guides/DISCORD_COMMANDS_GUIDE.md)

### System Documentation
- [Project Structure](docs/PROJECT_STRUCTURE.md)
- [Luna Capabilities](docs/LUNA_CAPABILITIES_DOCUMENTATION.md)

### System Summaries
- [Psychological Emotional System](docs/summaries/PSYCHOLOGICAL_EMOTIONAL_SYSTEM_SUMMARY.md)
- [Multimodal System](docs/summaries/MULTIMODAL_SYSTEM_SUMMARY.md)
- [Enhanced Features](docs/summaries/ENHANCED_FEATURES_SUMMARY.md)

## 🎯 Use Cases

### For Writers
- **Creative Writing**: AI-assisted story development and character creation
- **Content Enhancement**: Improve and expand existing content
- **Genre Exploration**: Experiment with different writing styles
- **Project Management**: Organize and track writing projects

### For Developers
- **AI Integration**: Advanced AI writing assistant capabilities
- **Multimodal Systems**: Image, voice, video, and audio generation
- **Emotional Intelligence**: Sophisticated emotional modeling
- **Analytics**: Comprehensive system monitoring and analytics

### For Researchers
- **Psychological Modeling**: Advanced emotional and psychological systems
- **Multimodal AI**: Comprehensive multimodal AI capabilities
- **User Behavior Analysis**: Detailed analytics and insights
- **System Architecture**: Modular, extensible system design

## 🔧 Configuration

### Environment Variables
```bash
# Discord Bot
DISCORD_TOKEN=your_discord_bot_token
BOT_PREFIX=!

# API Keys (optional)
OPENAI_API_KEY=your_openai_key
ELEVENLABS_API_KEY=your_elevenlabs_key
STABILITY_API_KEY=your_stability_key
```

### Configuration File
Edit `core/config.py` to customize:
- Discord bot settings
- API configurations
- System preferences
- Feature toggles

## 🧪 Testing

### Run All Tests
```bash
python launch.py tests
```

### Individual Test Suites
```bash
# Multimodal systems
python core/tests/test_enhanced_multimodal_systems.py

# Emotional systems
python core/tests/test_enhanced_psychological_emotions.py

# Basic multimodal
python core/tests/test_multimodal_system.py
```

## 📊 Monitoring

### System Dashboard
```bash
python launch.py dashboard --monitor --interval 60
```

### Analytics Dashboard
```bash
python launch.py analytics --system-report --period month
```

### Health Check
```bash
python core/health_check.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Discord.py**: Discord bot framework
- **Stable Diffusion**: Image generation capabilities
- **Plutchik's Wheel**: Emotional modeling foundation
- **Maslow's Hierarchy**: Psychological framework

---

**AI Writing Companion** - Where creativity meets artificial intelligence, and every story finds its voice. 