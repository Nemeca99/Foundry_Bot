#!/usr/bin/env python3
"""
Personalization Engine Plugin for Authoring Bot
Learns from user's writing style and conversation patterns
"""
import json
import logging
import re
import statistics
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.util import ngrams

logger = logging.getLogger(__name__)

class PersonalizationEngine:
    """Learns from user's writing style and provides personalized assistance"""
    
    def __init__(self, framework):
        self.framework = framework
        self.config = framework.config
        
        # Paths
        from config import Config
        self.book_collection_path = Config.BOOK_COLLECTION_PATH
        self.personalization_dir = Config.MODELS_DIR / "personalization"
        self.personalization_dir.mkdir(parents=True, exist_ok=True)
        
        # Writing style analysis
        self.writing_fingerprint = {}
        self.conversation_history = []
        self.style_preferences = {}
        
        # NLTK setup
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt', quiet=True)
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords', quiet=True)
        
        # Load existing data
        self._load_personalization_data()
        
        logger.info("✅ Personalization Engine plugin initialized")
    
    def _load_personalization_data(self):
        """Load existing personalization data"""
        fingerprint_file = self.personalization_dir / "writing_fingerprint.json"
        history_file = self.personalization_dir / "conversation_history.json"
        preferences_file = self.personalization_dir / "style_preferences.json"
        
        if fingerprint_file.exists():
            with open(fingerprint_file, 'r', encoding='utf-8') as f:
                self.writing_fingerprint = json.load(f)
        
        if history_file.exists():
            with open(history_file, 'r', encoding='utf-8') as f:
                self.conversation_history = json.load(f)
        
        if preferences_file.exists():
            with open(preferences_file, 'r', encoding='utf-8') as f:
                self.style_preferences = json.load(f)
    
    def _save_personalization_data(self):
        """Save personalization data"""
        fingerprint_file = self.personalization_dir / "writing_fingerprint.json"
        history_file = self.personalization_dir / "conversation_history.json"
        preferences_file = self.personalization_dir / "style_preferences.json"
        
        with open(fingerprint_file, 'w', encoding='utf-8') as f:
            json.dump(self.writing_fingerprint, f, indent=2, ensure_ascii=False)
        
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(self.conversation_history, f, indent=2, ensure_ascii=False)
        
        with open(preferences_file, 'w', encoding='utf-8') as f:
            json.dump(self.style_preferences, f, indent=2, ensure_ascii=False)
    
    def analyze_writing_style(self) -> Dict[str, Any]:
        """Analyze user's writing style from Book_Collection"""
        logger.info("🔍 Analyzing writing style from Book_Collection...")
        
        style_data = {
            "vocabulary": {},
            "sentence_structure": {},
            "themes": {},
            "characteristics": {}
        }
        
        total_words = 0
        total_sentences = 0
        all_words = []
        all_sentences = []
        
        # Process all text files in Book_Collection
        for text_file in self.book_collection_path.rglob("*.txt"):
            try:
                with open(text_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Tokenize
                words = word_tokenize(content.lower())
                sentences = sent_tokenize(content)
                
                all_words.extend(words)
                all_sentences.extend(sentences)
                total_words += len(words)
                total_sentences += len(sentences)
                
            except Exception as e:
                logger.warning(f"⚠️ Could not read {text_file}: {e}")
        
        if not all_words:
            logger.warning("⚠️ No text found in Book_Collection")
            return style_data
        
        # Analyze vocabulary
        word_freq = Counter(all_words)
        stop_words = set(stopwords.words('english'))
        
        # Most common words (excluding stop words)
        common_words = {word: count for word, count in word_freq.most_common(50) 
                       if word.lower() not in stop_words and len(word) > 2}
        
        # Analyze sentence structure
        sentence_lengths = [len(word_tokenize(sent)) for sent in all_sentences]
        avg_sentence_length = statistics.mean(sentence_lengths) if sentence_lengths else 0
        
        # Analyze themes (common phrases)
        bigrams = list(ngrams(all_words, 2))
        bigram_freq = Counter(bigrams)
        common_phrases = {f"{w1} {w2}": count for (w1, w2), count in bigram_freq.most_common(20)}
        
        # Writing characteristics
        characteristics = {
            "avg_sentence_length": avg_sentence_length,
            "total_words_analyzed": total_words,
            "total_sentences_analyzed": total_sentences,
            "vocabulary_richness": len(set(all_words)) / len(all_words) if all_words else 0,
            "avg_word_length": statistics.mean([len(word) for word in all_words if len(word) > 0]) if all_words else 0
        }
        
        style_data.update({
            "vocabulary": dict(common_words),
            "sentence_structure": {"avg_length": avg_sentence_length},
            "themes": dict(common_phrases),
            "characteristics": characteristics
        })
        
        self.writing_fingerprint = style_data
        self._save_personalization_data()
        
        logger.info("✅ Writing style analysis complete")
        return style_data
    
    def record_conversation(self, user_message: str, bot_response: str, context: str = ""):
        """Record a conversation interaction for learning"""
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "user_message": user_message,
            "bot_response": bot_response,
            "context": context,
            "message_length": len(user_message),
            "response_length": len(bot_response)
        }
        
        self.conversation_history.append(interaction)
        
        # Keep only last 1000 interactions
        if len(self.conversation_history) > 1000:
            self.conversation_history = self.conversation_history[-1000:]
        
        self._save_personalization_data()
    
    def analyze_conversation_patterns(self) -> Dict[str, Any]:
        """Analyze conversation patterns to understand user preferences"""
        if not self.conversation_history:
            return {}
        
        patterns = {
            "avg_message_length": 0,
            "avg_response_length": 0,
            "common_topics": {},
            "preferred_response_style": {},
            "interaction_frequency": {}
        }
        
        # Calculate averages
        message_lengths = [interaction["message_length"] for interaction in self.conversation_history]
        response_lengths = [interaction["response_length"] for interaction in self.conversation_history]
        
        patterns["avg_message_length"] = statistics.mean(message_lengths) if message_lengths else 0
        patterns["avg_response_length"] = statistics.mean(response_lengths) if response_lengths else 0
        
        # Analyze topics (simple keyword extraction)
        all_messages = " ".join([interaction["user_message"] for interaction in self.conversation_history])
        words = word_tokenize(all_messages.lower())
        word_freq = Counter(words)
        
        # Most common words (excluding stop words)
        stop_words = set(stopwords.words('english'))
        common_topics = {word: count for word, count in word_freq.most_common(20) 
                        if word.lower() not in stop_words and len(word) > 2}
        
        patterns["common_topics"] = dict(common_topics)
        
        return patterns
    
    def generate_personalized_prompt(self, base_prompt: str, context: str = "") -> str:
        """Generate a personalized prompt based on user's writing style"""
        if not self.writing_fingerprint:
            return base_prompt
        
        # Extract writing characteristics
        characteristics = self.writing_fingerprint.get("characteristics", {})
        vocabulary = self.writing_fingerprint.get("vocabulary", {})
        
        # Create personalized instructions
        personalization = []
        
        if characteristics.get("avg_sentence_length", 0) > 15:
            personalization.append("Use longer, more descriptive sentences")
        elif characteristics.get("avg_sentence_length", 0) < 10:
            personalization.append("Use shorter, concise sentences")
        
        if characteristics.get("vocabulary_richness", 0) > 0.7:
            personalization.append("Use rich, varied vocabulary")
        
        # Add common themes/words from user's writing
        if vocabulary:
            top_words = list(vocabulary.keys())[:5]
            personalization.append(f"Incorporate themes similar to: {', '.join(top_words)}")
        
        if personalization:
            personalized_prompt = f"{base_prompt}\n\nPersonalized Style: {'; '.join(personalization)}"
            return personalized_prompt
        
        return base_prompt
    
    def get_writing_suggestions(self, project_name: str = None) -> Dict[str, Any]:
        """Get personalized writing suggestions based on user's style"""
        suggestions = {
            "style_recommendations": [],
            "vocabulary_suggestions": [],
            "structure_advice": [],
            "thematic_elements": []
        }
        
        if not self.writing_fingerprint:
            return suggestions
        
        characteristics = self.writing_fingerprint.get("characteristics", {})
        vocabulary = self.writing_fingerprint.get("vocabulary", {})
        themes = self.writing_fingerprint.get("themes", {})
        
        # Style recommendations
        avg_length = characteristics.get("avg_sentence_length", 0)
        if avg_length > 20:
            suggestions["style_recommendations"].append("Consider breaking up long sentences for better readability")
        elif avg_length < 8:
            suggestions["style_recommendations"].append("Try varying sentence length for more dynamic prose")
        
        # Vocabulary suggestions
        if vocabulary:
            top_words = list(vocabulary.keys())[:10]
            suggestions["vocabulary_suggestions"] = [
                f"Consider using: {word}" for word in top_words
            ]
        
        # Structure advice
        if characteristics.get("vocabulary_richness", 0) < 0.5:
            suggestions["structure_advice"].append("Consider expanding vocabulary variety")
        
        # Thematic elements
        if themes:
            top_themes = list(themes.keys())[:5]
            suggestions["thematic_elements"] = [
                f"Theme suggestion: {theme}" for theme in top_themes
            ]
        
        return suggestions
    
    def create_style_profile(self) -> Dict[str, Any]:
        """Create a comprehensive style profile"""
        profile = {
            "writing_style": self.writing_fingerprint,
            "conversation_patterns": self.analyze_conversation_patterns(),
            "preferences": self.style_preferences,
            "last_updated": datetime.now().isoformat()
        }
        
        return profile
    
    def update_style_preferences(self, preferences: Dict[str, Any]):
        """Update user's style preferences"""
        self.style_preferences.update(preferences)
        self._save_personalization_data()
    
    def get_personalization_stats(self) -> Dict[str, Any]:
        """Get statistics about personalization data"""
        return {
            "writing_fingerprint_analyzed": bool(self.writing_fingerprint),
            "conversation_history_count": len(self.conversation_history),
            "style_preferences_count": len(self.style_preferences),
            "last_analysis": self.writing_fingerprint.get("last_analyzed", "Never"),
            "total_words_analyzed": self.writing_fingerprint.get("characteristics", {}).get("total_words_analyzed", 0),
            "avg_sentence_length": self.writing_fingerprint.get("characteristics", {}).get("avg_sentence_length", 0)
        }

def initialize(framework):
    """Initialize the personalization engine plugin"""
    return PersonalizationEngine(framework) 