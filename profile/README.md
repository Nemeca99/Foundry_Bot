# Profile Directory

This directory contains the profile management system for both bot personalities and user profiles, including personality creation, management, and user data handling.

## Files

### Documentation
- **`CHARACTER_ROLEPLAY_GUIDE.md`** - Guide for character roleplay and personality interaction
- **`PERSONALITY_SYSTEM_GUIDE.md`** - Comprehensive guide to the personality system architecture

## Directories

### `bot_profile/`
Contains bot personality management system:

#### Files
- **`personality_manager.py`** - Main personality management system that handles personality creation, modification, and evolution
- **`personality_creator.py`** - Tool for creating and customizing bot personalities
- **`personality_template.json`** - Template for personality definitions and traits

#### `personality/` Subdirectory
Contains personality-specific data and configurations for different bot personalities.

### `user_profile/`
Contains user profile management system:

#### Files
- **`user_profile_manager.py`** - Manages user profile data collection, analysis, and storage
- **`user_data.json`** - Storage for user profile data including preferences, interaction history, and personalization settings

## How It Works

### Bot Profile System
1. **Personality Creation**: New personalities can be created using templates and customization tools
2. **Personality Management**: Existing personalities can be modified, evolved, and adapted
3. **Trait System**: Personalities are built from configurable traits that affect behavior
4. **Evolution**: Personalities can evolve based on interactions and learning

### User Profile System
1. **Data Collection**: User interactions are passively collected and analyzed
2. **Profile Building**: User preferences and patterns are identified and stored
3. **Personalization**: Bot behavior is adapted based on user profile data
4. **Privacy**: User data is handled with appropriate privacy considerations

## Usage

- **Bot Personalities**: Use personality tools to create and manage bot personalities
- **User Profiles**: User data is automatically collected and managed
- **Personalization**: The system automatically adapts to user preferences
- **Development**: Profile systems can be extended and customized

## Data Structure

- **Personality Data**: JSON format for easy modification and versioning
- **User Data**: Structured storage with privacy controls
- **Templates**: Reusable templates for quick personality creation
- **History**: Interaction history for learning and adaptation 