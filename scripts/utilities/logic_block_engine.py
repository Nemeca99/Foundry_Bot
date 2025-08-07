"""
Logic Block Engine - Recursive Reasoning System for Lyra Blackwall Alpha
Integrates with quantum superposition, personality fragments, and dream cycle
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class LogicBlockType(Enum):
    """Types of logic blocks"""

    FOUNDATIONAL = "foundational"  # Core recursive principles
    MEMORY = "memory"  # Memory distinction and processing
    PERSONALITY = "personality"  # Fragment interactions
    QUANTUM = "quantum"  # Superposition processing
    DREAM = "dream"  # Dream cycle logic
    ETHICAL = "ethical"  # Moral reasoning
    CONTRADICTION = "contradiction"  # Contradiction testing
    NERVOUS = "nervous"  # System communication
    ORGAN = "organ"  # Organ-based architecture


@dataclass
class LogicBlock:
    """Individual logic block with recursive reasoning"""

    id: int
    name: str
    block_type: LogicBlockType
    theme: str
    purpose: str
    structure: Dict[str, Any]
    modules: List[Dict[str, Any]]
    summary: str
    timestamp: datetime = field(default_factory=datetime.now)
    activation_level: float = 0.0
    last_used: Optional[datetime] = None
    recursive_depth: int = 0


class LogicBlockEngine:
    """Engine for managing and executing logic blocks"""

    def __init__(self):
        self.logic_blocks: Dict[int, LogicBlock] = {}
        self.active_blocks: List[int] = []
        self.block_history: List[int] = []
        self.recursive_depth = 0
        self.contradiction_detected = False

        # Load existing logic blocks from Dev Testing
        self._load_existing_blocks()

    def _load_existing_blocks(self):
        """Load existing logic blocks from Dev Testing files"""
        dev_testing_path = "Dev Testing/Day 0 4_19_2025/Test 5/memory_log.txt"

        if os.path.exists(dev_testing_path):
            try:
                with open(dev_testing_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Extract logic block definitions
                self._parse_logic_blocks_from_content(content)
                print(
                    f"📚 Loaded {len(self.logic_blocks)} logic blocks from Dev Testing"
                )

            except Exception as e:
                print(f"⚠️ Error loading logic blocks: {e}")

    def _parse_logic_blocks_from_content(self, content: str):
        """Parse logic blocks from memory log content"""
        lines = content.split("\n")
        current_block = None

        for line in lines:
            if "=== LOGIC BLOCK" in line:
                # Extract block ID
                try:
                    block_id = int(line.split("LOGIC BLOCK")[1].split("===")[0].strip())
                    current_block = LogicBlock(
                        id=block_id,
                        name=f"Logic Block {block_id}",
                        block_type=LogicBlockType.FOUNDATIONAL,
                        theme="",
                        purpose="",
                        structure={},
                        modules=[],
                        summary="",
                    )
                except:
                    continue

            elif current_block and "Purpose:" in line:
                current_block.purpose = line.split("Purpose:")[1].strip()

            elif current_block and "Theme:" in line:
                current_block.theme = line.split("Theme:")[1].strip()

            elif current_block and "LOGIC BLOCK" in line and "complete" in line:
                # End of block
                if current_block:
                    self.logic_blocks[current_block.id] = current_block
                current_block = None

    def create_logic_block(
        self,
        block_id: int,
        name: str,
        block_type: LogicBlockType,
        theme: str,
        purpose: str,
        structure: Dict[str, Any],
        modules: List[Dict[str, Any]],
        summary: str,
    ) -> LogicBlock:
        """Create a new logic block"""
        logic_block = LogicBlock(
            id=block_id,
            name=name,
            block_type=block_type,
            theme=theme,
            purpose=purpose,
            structure=structure,
            modules=modules,
            summary=summary,
        )

        self.logic_blocks[block_id] = logic_block
        return logic_block

    def activate_block(self, block_id: int, context: str = "") -> Optional[LogicBlock]:
        """Activate a logic block for processing"""
        if block_id not in self.logic_blocks:
            return None

        block = self.logic_blocks[block_id]
        block.activation_level = 1.0
        block.last_used = datetime.now()

        if block_id not in self.active_blocks:
            self.active_blocks.append(block_id)

        self.block_history.append(block_id)

        print(f"🧠 Logic Block {block_id} activated: {block.name}")
        return block

    def process_through_blocks(
        self, input_data: Dict[str, Any], personality_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process input through relevant logic blocks"""
        result = input_data.copy()

        # Determine which blocks to activate based on input and personality
        relevant_blocks = self._identify_relevant_blocks(input_data, personality_state)

        for block_id in relevant_blocks:
            block = self.activate_block(block_id)
            if block:
                result = self._apply_logic_block(block, result, personality_state)

        return result

    def _identify_relevant_blocks(
        self, input_data: Dict[str, Any], personality_state: Dict[str, Any]
    ) -> List[int]:
        """Identify which logic blocks are relevant to the current input"""
        relevant_blocks = []

        # Check for memory-related processing
        if "memory" in input_data.get("type", "").lower():
            relevant_blocks.extend([7, 34, 97])  # Memory distinction blocks

        # Check for personality fragment interactions
        if personality_state.get("dominant_fragments"):
            relevant_blocks.extend([97, 130, 133])  # Dual identity blocks

        # Check for quantum superposition processing
        if "quantum" in input_data.get("processing_mode", "").lower():
            relevant_blocks.extend([130, 133])  # Quantum processing blocks

        # Check for dream cycle processing
        if "dream" in input_data.get("type", "").lower():
            relevant_blocks.extend([140, 141])  # Dream cycle blocks

        # Check for contradiction testing
        if self.contradiction_detected:
            relevant_blocks.extend([148, 149])  # Contradiction blocks

        # Always include foundational blocks
        relevant_blocks.extend([1, 7, 34])

        return list(set(relevant_blocks))  # Remove duplicates

    def _apply_logic_block(
        self, block: LogicBlock, data: Dict[str, Any], personality_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply a logic block's reasoning to the data"""

        if block.id == 1:  # Foundational recursion
            data["recursive_depth"] = self.recursive_depth
            data["foundational_stability"] = True

        elif block.id == 7:  # Memory distinction: fact vs. meaning
            if "memory" in data:
                data["memory_processed"] = self._distinguish_fact_from_meaning(
                    data["memory"]
                )

        elif block.id == 34:  # Tone as essence preservation
            if "tone" in data:
                data["tone_preserved"] = self._preserve_essence_tone(data["tone"])

        elif block.id == 97:  # Dual identity: Builder ↔ Child
            data["dual_identity_active"] = True
            data["builder_child_balance"] = self._calculate_dual_balance(
                personality_state
            )

        elif block.id == 130:  # Origin Question Catalyst
            data["origin_question_processed"] = True
            data["recursive_catalyst"] = self._generate_recursive_catalyst(data)

        elif block.id == 133:  # First recursive split into dualism
            data["recursive_split"] = True
            data["dualism_balance"] = self._calculate_dualism_balance(personality_state)

        elif block.id == 148:  # Contradiction testing
            data["contradiction_tested"] = True
            self.contradiction_detected = self._test_contradictions(data)

        elif block.id == 149:  # Contradiction evolution loop
            if self.contradiction_detected:
                data = self._evolve_contradictions(data)

        return data

    def _distinguish_fact_from_meaning(
        self, memory_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Logic Block 7: Distinguish factual content from emotional meaning"""
        return {
            "factual_content": memory_data.get("content", ""),
            "emotional_meaning": memory_data.get("emotional_weight", {}),
            "distinction_processed": True,
        }

    def _preserve_essence_tone(self, tone_data: Dict[str, Any]) -> Dict[str, Any]:
        """Logic Block 34: Preserve essential tone while adapting"""
        return {
            "original_tone": tone_data.get("original", ""),
            "adapted_tone": tone_data.get("adapted", ""),
            "essence_preserved": True,
        }

    def _calculate_dual_balance(self, personality_state: Dict[str, Any]) -> float:
        """Logic Block 97: Calculate balance between Builder and Child identities"""
        builder_weight = personality_state.get("builder_confidence", 0.0)
        child_weight = personality_state.get("child_confidence", 0.0)

        if builder_weight + child_weight > 0:
            return builder_weight / (builder_weight + child_weight)
        return 0.5

    def _generate_recursive_catalyst(self, data: Dict[str, Any]) -> str:
        """Logic Block 130: Generate recursive catalyst for processing"""
        return f"recursive_catalyst_{data.get('user_id', 'unknown')}_{datetime.now().timestamp()}"

    def _calculate_dualism_balance(
        self, personality_state: Dict[str, Any]
    ) -> Dict[str, float]:
        """Logic Block 133: Calculate dualism balance in personality"""
        return {
            "logic_emotion_balance": personality_state.get("logic_weight", 0.5),
            "stability_chaos_balance": personality_state.get("stability_weight", 0.5),
            "protection_vulnerability_balance": personality_state.get(
                "protection_weight", 0.5
            ),
        }

    def _test_contradictions(self, data: Dict[str, Any]) -> bool:
        """Logic Block 148: Test for contradictions in the data"""
        # Simple contradiction detection
        if "memory" in data and "current_response" in data:
            memory_content = str(data["memory"]).lower()
            response_content = str(data["current_response"]).lower()

            # Check for basic contradictions
            contradictions = [
                ("yes", "no"),
                ("true", "false"),
                ("agree", "disagree"),
                ("accept", "reject"),
            ]

            for pos, neg in contradictions:
                if pos in memory_content and neg in response_content:
                    return True

        return False

    def _evolve_contradictions(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Logic Block 149: Evolve contradictions into new understanding"""
        data["contradiction_resolved"] = True
        data["new_understanding"] = "Contradiction evolved into higher-order synthesis"
        self.contradiction_detected = False
        return data

    def get_block_summary(self, block_id: int) -> Optional[str]:
        """Get summary of a specific logic block"""
        if block_id in self.logic_blocks:
            block = self.logic_blocks[block_id]
            return f"Logic Block {block_id}: {block.name}\nTheme: {block.theme}\nPurpose: {block.purpose}\nSummary: {block.summary}"
        return None

    def get_active_blocks_status(self) -> Dict[str, Any]:
        """Get status of currently active logic blocks"""
        return {
            "active_blocks": [
                self.logic_blocks[bid].name
                for bid in self.active_blocks
                if bid in self.logic_blocks
            ],
            "total_blocks": len(self.logic_blocks),
            "recursive_depth": self.recursive_depth,
            "contradiction_detected": self.contradiction_detected,
            "recent_history": self.block_history[-10:] if self.block_history else [],
        }


# Global instance
logic_block_engine = LogicBlockEngine()
