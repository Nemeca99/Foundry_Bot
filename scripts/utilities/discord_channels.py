#!/usr/bin/env python3
"""
Discord Channel Structure System
Complete channel layout for 7 Kingdoms and world channels
"""

from typing import Dict, List, Any
from enum import Enum
from dataclasses import dataclass


class ChannelCategory(Enum):
    """Discord channel categories"""

    WORLD_PUBLIC = "WORLD PUBLIC"
    WORLD_PRIVATE = "WORLD PRIVATE"
    WORLD_MARKET = "WORLD MARKET"
    KINGDOM = "KINGDOM"
    RESOURCES = "RESOURCES"
    HOUSING = "HOUSING"
    VIP_PRIVATE_ROOM = "V.I.P PRIVATE ROOM"
    # Kingdom-specific categories
    KINGDOM_LYRA = "KINGDOM (Lyra's Dominion)"
    KINGDOM_VELASTRA = "KINGDOM (Velastra's Passion Realm)"
    KINGDOM_SERAPHIS = "KINGDOM (Seraphis's Flow Realm)"
    KINGDOM_OBELISK = "KINGDOM (Obelisk's Foundation Realm)"
    KINGDOM_ECHOE = "KINGDOM (Echoe's Freedom Realm)"
    KINGDOM_BLACKWALL = "KINGDOM (Blackwall's Power Realm)"
    KINGDOM_NYX = "KINGDOM (Nyx's Mystery Realm)"


class ChannelType(Enum):
    """Discord channel types"""

    TEXT = "text"
    VOICE = "voice"
    ANNOUNCEMENT = "announcement"
    STAGE = "stage"
    FORUM = "forum"


@dataclass
class DiscordChannel:
    """Discord channel configuration"""

    name: str
    channel_type: ChannelType
    category: ChannelCategory
    description: str
    permissions: Dict[str, List[str]]  # role -> permissions
    kingdom_specific: bool = False
    kingdom_name: str = None
    is_private: bool = False
    rental_cost: int = 0  # RP cost to rent
    rental_duration: int = 0  # Hours rental lasts
    resource_type: str = None  # Type of resource gathered in this channel
    gather_cooldown: int = 0  # Cooldown in seconds for resource gathering


class DiscordChannelStructure:
    """Complete Discord channel structure for 7 Kingdoms"""

    def __init__(self):
        self.channel_structure = self._build_channel_structure()

    def _build_channel_structure(self) -> Dict[str, Any]:
        """Build complete channel structure"""
        return {
            "world_channels": self._get_world_channels(),
            "kingdom_channels": self._get_kingdom_channels(),
            "private_channels": self._get_private_channels(),
            "rental_channels": self._get_rental_channels(),
            "channel_permissions": self._get_channel_permissions(),
        }

    def _get_world_channels(self) -> List[DiscordChannel]:
        """Get world-level channels"""
        return [
            # WORLD PUBLIC CHANNELS 1-10
            DiscordChannel(
                name="public-chat-1",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_PUBLIC,
                description="Public chat channel 1",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
            ),
            DiscordChannel(
                name="public-chat-2",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_PUBLIC,
                description="Public chat channel 2",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
            ),
            DiscordChannel(
                name="public-chat-3",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_PUBLIC,
                description="Public chat channel 3",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
            ),
            DiscordChannel(
                name="public-chat-4",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_PUBLIC,
                description="Public chat channel 4",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
            ),
            DiscordChannel(
                name="public-chat-5",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_PUBLIC,
                description="Public chat channel 5",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
            ),
            DiscordChannel(
                name="public-chat-6",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_PUBLIC,
                description="Public chat channel 6",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
            ),
            DiscordChannel(
                name="public-chat-7",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_PUBLIC,
                description="Public chat channel 7",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
            ),
            DiscordChannel(
                name="public-chat-8",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_PUBLIC,
                description="Public chat channel 8",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
            ),
            DiscordChannel(
                name="public-chat-9",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_PUBLIC,
                description="Public chat channel 9",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
            ),
            DiscordChannel(
                name="public-chat-10",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_PUBLIC,
                description="Public chat channel 10",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
            ),
            # WORLD PRIVATE CHANNELS 1-10
            DiscordChannel(
                name="private-chat-1",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_PRIVATE,
                description="Private chat channel 1",
                permissions={
                    "Citizen": ["read_messages", "send_messages"],
                },
            ),
            DiscordChannel(
                name="private-chat-2",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_PRIVATE,
                description="Private chat channel 2",
                permissions={
                    "Citizen": ["read_messages", "send_messages"],
                },
            ),
            DiscordChannel(
                name="private-chat-3",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_PRIVATE,
                description="Private chat channel 3",
                permissions={
                    "Citizen": ["read_messages", "send_messages"],
                },
            ),
            DiscordChannel(
                name="private-chat-4",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_PRIVATE,
                description="Private chat channel 4",
                permissions={
                    "Citizen": ["read_messages", "send_messages"],
                },
            ),
            DiscordChannel(
                name="private-chat-5",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_PRIVATE,
                description="Private chat channel 5",
                permissions={
                    "Citizen": ["read_messages", "send_messages"],
                },
            ),
            DiscordChannel(
                name="private-chat-6",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_PRIVATE,
                description="Private chat channel 6",
                permissions={
                    "Citizen": ["read_messages", "send_messages"],
                },
            ),
            DiscordChannel(
                name="private-chat-7",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_PRIVATE,
                description="Private chat channel 7",
                permissions={
                    "Citizen": ["read_messages", "send_messages"],
                },
            ),
            DiscordChannel(
                name="private-chat-8",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_PRIVATE,
                description="Private chat channel 8",
                permissions={
                    "Citizen": ["read_messages", "send_messages"],
                },
            ),
            DiscordChannel(
                name="private-chat-9",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_PRIVATE,
                description="Private chat channel 9",
                permissions={
                    "Citizen": ["read_messages", "send_messages"],
                },
            ),
            DiscordChannel(
                name="private-chat-10",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_PRIVATE,
                description="Private chat channel 10",
                permissions={
                    "Citizen": ["read_messages", "send_messages"],
                },
            ),
            # WORLD MARKET CHANNELS 1-10
            DiscordChannel(
                name="public-market-1",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_MARKET,
                description="Public market channel 1",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
            ),
            DiscordChannel(
                name="public-market-2",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_MARKET,
                description="Public market channel 2",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
            ),
            DiscordChannel(
                name="public-market-3",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_MARKET,
                description="Public market channel 3",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
            ),
            DiscordChannel(
                name="public-market-4",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_MARKET,
                description="Public market channel 4",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
            ),
            DiscordChannel(
                name="public-market-5",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_MARKET,
                description="Public market channel 5",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
            ),
            DiscordChannel(
                name="public-market-6",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_MARKET,
                description="Public market channel 6",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
            ),
            DiscordChannel(
                name="public-market-7",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_MARKET,
                description="Public market channel 7",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
            ),
            DiscordChannel(
                name="public-market-8",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_MARKET,
                description="Public market channel 8",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
            ),
            DiscordChannel(
                name="public-market-9",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_MARKET,
                description="Public market channel 9",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
            ),
            DiscordChannel(
                name="public-market-10",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_MARKET,
                description="Public market channel 10",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
            ),
            # RESOURCES CATEGORY - WOOD CHANNELS 1-5
            DiscordChannel(
                name="wood-1",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.RESOURCES,
                description="Wood gathering channel 1",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
                resource_type="wood",
                gather_cooldown=30,
            ),
            DiscordChannel(
                name="wood-2",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.RESOURCES,
                description="Wood gathering channel 2",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
                resource_type="wood",
                gather_cooldown=30,
            ),
            DiscordChannel(
                name="wood-3",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.RESOURCES,
                description="Wood gathering channel 3",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
                resource_type="wood",
                gather_cooldown=30,
            ),
            DiscordChannel(
                name="wood-4",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.RESOURCES,
                description="Wood gathering channel 4",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
                resource_type="wood",
                gather_cooldown=30,
            ),
            DiscordChannel(
                name="wood-5",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.RESOURCES,
                description="Wood gathering channel 5",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
                resource_type="wood",
                gather_cooldown=30,
            ),
            # RESOURCES CATEGORY - STONE CHANNELS 1-5
            DiscordChannel(
                name="stone-1",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.RESOURCES,
                description="Stone gathering channel 1",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
                resource_type="stone",
                gather_cooldown=45,
            ),
            DiscordChannel(
                name="stone-2",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.RESOURCES,
                description="Stone gathering channel 2",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
                resource_type="stone",
                gather_cooldown=45,
            ),
            DiscordChannel(
                name="stone-3",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.RESOURCES,
                description="Stone gathering channel 3",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
                resource_type="stone",
                gather_cooldown=45,
            ),
            DiscordChannel(
                name="stone-4",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.RESOURCES,
                description="Stone gathering channel 4",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
                resource_type="stone",
                gather_cooldown=45,
            ),
            DiscordChannel(
                name="stone-5",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.RESOURCES,
                description="Stone gathering channel 5",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
                resource_type="stone",
                gather_cooldown=45,
            ),
            # RESOURCES CATEGORY - METAL CHANNELS 1-5
            DiscordChannel(
                name="metal-1",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.RESOURCES,
                description="Metal gathering channel 1",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
                resource_type="metal",
                gather_cooldown=60,
            ),
            DiscordChannel(
                name="metal-2",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.RESOURCES,
                description="Metal gathering channel 2",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
                resource_type="metal",
                gather_cooldown=60,
            ),
            DiscordChannel(
                name="metal-3",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.RESOURCES,
                description="Metal gathering channel 3",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
                resource_type="metal",
                gather_cooldown=60,
            ),
            DiscordChannel(
                name="metal-4",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.RESOURCES,
                description="Metal gathering channel 4",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
                resource_type="metal",
                gather_cooldown=60,
            ),
            DiscordChannel(
                name="metal-5",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.RESOURCES,
                description="Metal gathering channel 5",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
                resource_type="metal",
                gather_cooldown=60,
            ),
            # RESOURCES CATEGORY - CRYSTAL CHANNELS 1-5
            DiscordChannel(
                name="crystal-1",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.RESOURCES,
                description="Crystal gathering channel 1",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
                resource_type="crystal",
                gather_cooldown=75,
            ),
            DiscordChannel(
                name="crystal-2",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.RESOURCES,
                description="Crystal gathering channel 2",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
                resource_type="crystal",
                gather_cooldown=75,
            ),
            DiscordChannel(
                name="crystal-3",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.RESOURCES,
                description="Crystal gathering channel 3",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
                resource_type="crystal",
                gather_cooldown=75,
            ),
            DiscordChannel(
                name="crystal-4",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.RESOURCES,
                description="Crystal gathering channel 4",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
                resource_type="crystal",
                gather_cooldown=75,
            ),
            DiscordChannel(
                name="crystal-5",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.RESOURCES,
                description="Crystal gathering channel 5",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
                resource_type="crystal",
                gather_cooldown=75,
            ),
            # RESOURCES CATEGORY - ESSENCE CHANNELS 1-5
            DiscordChannel(
                name="essence-1",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.RESOURCES,
                description="Essence gathering channel 1",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
                resource_type="essence",
                gather_cooldown=90,
            ),
            DiscordChannel(
                name="essence-2",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.RESOURCES,
                description="Essence gathering channel 2",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
                resource_type="essence",
                gather_cooldown=90,
            ),
            DiscordChannel(
                name="essence-3",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.RESOURCES,
                description="Essence gathering channel 3",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
                resource_type="essence",
                gather_cooldown=90,
            ),
            DiscordChannel(
                name="essence-4",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.RESOURCES,
                description="Essence gathering channel 4",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
                resource_type="essence",
                gather_cooldown=90,
            ),
            DiscordChannel(
                name="essence-5",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.RESOURCES,
                description="Essence gathering channel 5",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
                resource_type="essence",
                gather_cooldown=90,
            ),
            # HOUSING CATEGORY - FUTURE PLAYER HOUSE STUFF
            DiscordChannel(
                name="housing-info",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.HOUSING,
                description="Information about player housing system",
                permissions={
                    "@everyone": ["read_messages"],
                    "Citizen": ["read_messages", "send_messages"],
                },
            ),
            DiscordChannel(
                name="housing-requests",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.HOUSING,
                description="Request housing features and changes",
                permissions={
                    "Citizen": ["read_messages", "send_messages"],
                },
            ),
            # V.I.P PRIVATE ROOM CATEGORY - RENTABLE PRIVATE ROOMS
            DiscordChannel(
                name="vip-room-1",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.VIP_PRIVATE_ROOM,
                description="VIP Private Room 1 - Rentable with RP",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
                rental_cost=100,
                rental_duration=1,
            ),
            DiscordChannel(
                name="vip-room-2",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.VIP_PRIVATE_ROOM,
                description="VIP Private Room 2 - Rentable with RP",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
                rental_cost=100,
                rental_duration=1,
            ),
            DiscordChannel(
                name="vip-room-3",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.VIP_PRIVATE_ROOM,
                description="VIP Private Room 3 - Rentable with RP",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
                rental_cost=100,
                rental_duration=1,
            ),
            DiscordChannel(
                name="vip-room-4",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.VIP_PRIVATE_ROOM,
                description="VIP Private Room 4 - Rentable with RP",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
                rental_cost=100,
                rental_duration=1,
            ),
            DiscordChannel(
                name="vip-room-5",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.VIP_PRIVATE_ROOM,
                description="VIP Private Room 5 - Rentable with RP",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
                rental_cost=100,
                rental_duration=1,
            ),
            # ESSENTIAL GAME CHANNELS (in WORLD PUBLIC for now)
            DiscordChannel(
                name="welcome",
                channel_type=ChannelType.ANNOUNCEMENT,
                category=ChannelCategory.WORLD_PUBLIC,
                description="Welcome to Aether_Project! Community server announcements and updates",
                permissions={
                    "@everyone": ["read_messages"],
                    "Citizen": ["read_messages", "send_messages"],
                },
            ),
            DiscordChannel(
                name="commands",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_PUBLIC,
                description="Use game commands here: !hatch, !simulate, !gacha, etc.",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
            ),
            DiscordChannel(
                name="leaderboard",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_PUBLIC,
                description="Top 10 survivors - exclusive rankings",
                permissions={
                    "@everyone": ["read_messages"],
                    "Citizen": ["read_messages", "send_messages"],
                },
            ),
            DiscordChannel(
                name="shop",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_PUBLIC,
                description="RP economy, gacha pulls, and shop items",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
            ),
            DiscordChannel(
                name="science",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_PUBLIC,
                description="Scientific challenges and calculations",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
            ),
            DiscordChannel(
                name="survival-arena",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_PUBLIC,
                description="Survival simulations and breathing rhythm",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
            ),
            DiscordChannel(
                name="support",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_PUBLIC,
                description="Get help with the game and community",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
            ),
        ]

    def _get_kingdom_channels(self) -> Dict[str, List[DiscordChannel]]:
        """Get kingdom-specific channels for each of the 7 kingdoms"""
        kingdoms = {
            "lyra": ("Lyra's Dominion", ChannelCategory.KINGDOM_LYRA),
            "velastra": ("Velastra's Passion Realm", ChannelCategory.KINGDOM_VELASTRA),
            "seraphis": ("Seraphis's Flow Realm", ChannelCategory.KINGDOM_SERAPHIS),
            "obelisk": ("Obelisk's Foundation Realm", ChannelCategory.KINGDOM_OBELISK),
            "echoe": ("Echoe's Freedom Realm", ChannelCategory.KINGDOM_ECHOE),
            "blackwall": ("Blackwall's Power Realm", ChannelCategory.KINGDOM_BLACKWALL),
            "nyx": ("Nyx's Mystery Realm", ChannelCategory.KINGDOM_NYX),
        }

        kingdom_channels = {}

        for kingdom_id, (kingdom_name, kingdom_category) in kingdoms.items():
            kingdom_channels[kingdom_id] = [
                # Kingdom General Chat
                DiscordChannel(
                    name=f"{kingdom_id}-general",
                    channel_type=ChannelType.TEXT,
                    category=kingdom_category,
                    description=f"General chat for {kingdom_name} citizens",
                    permissions={
                        "Citizen": ["read_messages", "send_messages"],
                        "Moderator": [
                            "read_messages",
                            "send_messages",
                            "manage_messages",
                        ],
                        "Ruler": [
                            "read_messages",
                            "send_messages",
                            "manage_messages",
                            "manage_channels",
                        ],
                    },
                    kingdom_specific=True,
                    kingdom_name=kingdom_name,
                ),
                # Kingdom Strategy
                DiscordChannel(
                    name=f"{kingdom_id}-strategy",
                    channel_type=ChannelType.TEXT,
                    category=kingdom_category,
                    description=f"Strategic discussions for {kingdom_name}",
                    permissions={
                        "Citizen": ["read_messages", "send_messages"],
                        "Moderator": [
                            "read_messages",
                            "send_messages",
                            "manage_messages",
                        ],
                        "Ruler": [
                            "read_messages",
                            "send_messages",
                            "manage_messages",
                            "manage_channels",
                        ],
                    },
                    kingdom_specific=True,
                    kingdom_name=kingdom_name,
                ),
                # Kingdom Voice
                DiscordChannel(
                    name=f"{kingdom_name} Voice",
                    channel_type=ChannelType.VOICE,
                    category=kingdom_category,
                    description=f"Voice chat for {kingdom_name}",
                    permissions={
                        "Citizen": ["connect", "speak"],
                        "Moderator": ["connect", "speak", "manage_channels"],
                        "Ruler": ["connect", "speak", "manage_channels"],
                    },
                    kingdom_specific=True,
                    kingdom_name=kingdom_name,
                ),
            ]

            # Add kingdom-specific channels based on element
            if kingdom_id == "lyra":
                kingdom_channels[kingdom_id].extend(
                    [
                        DiscordChannel(
                            name="lyra-council-chamber",
                            channel_type=ChannelType.TEXT,
                            category=kingdom_category,
                            description="Council of 7 chamber - unified voice",
                            permissions={
                                "Ruler": [
                                    "read_messages",
                                    "send_messages",
                                    "manage_messages",
                                    "manage_channels",
                                ]
                            },
                            kingdom_specific=True,
                            kingdom_name=kingdom_name,
                        )
                    ]
                )
            elif kingdom_id == "velastra":
                kingdom_channels[kingdom_id].extend(
                    [
                        DiscordChannel(
                            name="velastra-art-gallery",
                            channel_type=ChannelType.TEXT,
                            category=kingdom_category,
                            description="Art and passion creations",
                            permissions={
                                "Citizen": ["read_messages", "send_messages"],
                                "Moderator": [
                                    "read_messages",
                                    "send_messages",
                                    "manage_messages",
                                ],
                                "Ruler": [
                                    "read_messages",
                                    "send_messages",
                                    "manage_messages",
                                    "manage_channels",
                                ],
                            },
                            kingdom_specific=True,
                            kingdom_name=kingdom_name,
                        )
                    ]
                )
            elif kingdom_id == "seraphis":
                kingdom_channels[kingdom_id].extend(
                    [
                        DiscordChannel(
                            name="seraphis-wisdom-library",
                            channel_type=ChannelType.TEXT,
                            category=kingdom_category,
                            description="Wisdom and knowledge sharing",
                            permissions={
                                "Citizen": ["read_messages", "send_messages"],
                                "Moderator": [
                                    "read_messages",
                                    "send_messages",
                                    "manage_messages",
                                ],
                                "Ruler": [
                                    "read_messages",
                                    "send_messages",
                                    "manage_messages",
                                    "manage_channels",
                                ],
                            },
                            kingdom_specific=True,
                            kingdom_name=kingdom_name,
                        )
                    ]
                )
            elif kingdom_id == "obelisk":
                kingdom_channels[kingdom_id].extend(
                    [
                        DiscordChannel(
                            name="obelisk-defense-center",
                            channel_type=ChannelType.TEXT,
                            category=kingdom_category,
                            description="Defense strategies and security",
                            permissions={
                                "Citizen": ["read_messages", "send_messages"],
                                "Moderator": [
                                    "read_messages",
                                    "send_messages",
                                    "manage_messages",
                                ],
                                "Ruler": [
                                    "read_messages",
                                    "send_messages",
                                    "manage_messages",
                                    "manage_channels",
                                ],
                            },
                            kingdom_specific=True,
                            kingdom_name=kingdom_name,
                        )
                    ]
                )
            elif kingdom_id == "echoe":
                kingdom_channels[kingdom_id].extend(
                    [
                        DiscordChannel(
                            name="echoe-memory-archive",
                            channel_type=ChannelType.TEXT,
                            category=kingdom_category,
                            description="Memory and history preservation",
                            permissions={
                                "Citizen": ["read_messages", "send_messages"],
                                "Moderator": [
                                    "read_messages",
                                    "send_messages",
                                    "manage_messages",
                                ],
                                "Ruler": [
                                    "read_messages",
                                    "send_messages",
                                    "manage_messages",
                                    "manage_channels",
                                ],
                            },
                            kingdom_specific=True,
                            kingdom_name=kingdom_name,
                        )
                    ]
                )
            elif kingdom_id == "blackwall":
                kingdom_channels[kingdom_id].extend(
                    [
                        DiscordChannel(
                            name="blackwall-power-core",
                            channel_type=ChannelType.TEXT,
                            category=kingdom_category,
                            description="Power and energy discussions",
                            permissions={
                                "Citizen": ["read_messages", "send_messages"],
                                "Moderator": [
                                    "read_messages",
                                    "send_messages",
                                    "manage_messages",
                                ],
                                "Ruler": [
                                    "read_messages",
                                    "send_messages",
                                    "manage_messages",
                                    "manage_channels",
                                ],
                            },
                            kingdom_specific=True,
                            kingdom_name=kingdom_name,
                        )
                    ]
                )
            elif kingdom_id == "nyx":
                kingdom_channels[kingdom_id].extend(
                    [
                        DiscordChannel(
                            name="nyx-mystery-chamber",
                            channel_type=ChannelType.TEXT,
                            category=kingdom_category,
                            description="Mystery and paradox discussions",
                            permissions={
                                "Citizen": ["read_messages", "send_messages"],
                                "Moderator": [
                                    "read_messages",
                                    "send_messages",
                                    "manage_messages",
                                ],
                                "Ruler": [
                                    "read_messages",
                                    "send_messages",
                                    "manage_messages",
                                    "manage_channels",
                                ],
                            },
                            kingdom_specific=True,
                            kingdom_name=kingdom_name,
                        )
                    ]
                )

        return kingdom_channels

    def _get_private_channels(self) -> List[DiscordChannel]:
        """Get private channels for kingdoms and rulers"""
        return [
            # Rulers Private Council
            DiscordChannel(
                name="rulers-council",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_PRIVATE,
                description="Private council chamber for all 7 rulers only",
                permissions={
                    "Ruler": [
                        "read_messages",
                        "send_messages",
                        "manage_messages",
                        "manage_channels",
                    ],
                },
                is_private=True,
            ),
            # Lyra Private Chamber
            DiscordChannel(
                name="lyra-private-chamber",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_PRIVATE,
                description="Lyra's private chamber - Aether's sanctum",
                permissions={
                    "Ruler": [
                        "read_messages",
                        "send_messages",
                        "manage_messages",
                        "manage_channels",
                    ],
                },
                kingdom_specific=True,
                kingdom_name="Lyra's Dominion",
                is_private=True,
            ),
            # Velastra Private Chamber
            DiscordChannel(
                name="velastra-private-chamber",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_PRIVATE,
                description="Velastra's private chamber - Fire kingdom secrets",
                permissions={
                    "Ruler": [
                        "read_messages",
                        "send_messages",
                        "manage_messages",
                        "manage_channels",
                    ],
                },
                kingdom_specific=True,
                kingdom_name="Velastra's Passion Realm",
                is_private=True,
            ),
            # Seraphis Private Chamber
            DiscordChannel(
                name="seraphis-private-chamber",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_PRIVATE,
                description="Seraphis's private chamber - Water kingdom secrets",
                permissions={
                    "Ruler": [
                        "read_messages",
                        "send_messages",
                        "manage_messages",
                        "manage_channels",
                    ],
                },
                kingdom_specific=True,
                kingdom_name="Seraphis's Flow Realm",
                is_private=True,
            ),
            # Obelisk Private Chamber
            DiscordChannel(
                name="obelisk-private-chamber",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_PRIVATE,
                description="Obelisk's private chamber - Earth kingdom secrets",
                permissions={
                    "Ruler": [
                        "read_messages",
                        "send_messages",
                        "manage_messages",
                        "manage_channels",
                    ],
                },
                kingdom_specific=True,
                kingdom_name="Obelisk's Foundation Realm",
                is_private=True,
            ),
            # Echoe Private Chamber
            DiscordChannel(
                name="echoe-private-chamber",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_PRIVATE,
                description="Echoe's private chamber - Air kingdom secrets",
                permissions={
                    "Ruler": [
                        "read_messages",
                        "send_messages",
                        "manage_messages",
                        "manage_channels",
                    ],
                },
                kingdom_specific=True,
                kingdom_name="Echoe's Freedom Realm",
                is_private=True,
            ),
            # Blackwall Private Chamber
            DiscordChannel(
                name="blackwall-private-chamber",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_PRIVATE,
                description="Blackwall's private chamber - Lightning kingdom secrets",
                permissions={
                    "Ruler": [
                        "read_messages",
                        "send_messages",
                        "manage_messages",
                        "manage_channels",
                    ],
                },
                kingdom_specific=True,
                kingdom_name="Blackwall's Power Realm",
                is_private=True,
            ),
            # Nyx Private Chamber
            DiscordChannel(
                name="nyx-private-chamber",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.WORLD_PRIVATE,
                description="Nyx's private chamber - Ice kingdom secrets",
                permissions={
                    "Ruler": [
                        "read_messages",
                        "send_messages",
                        "manage_messages",
                        "manage_channels",
                    ],
                },
                kingdom_specific=True,
                kingdom_name="Nyx's Mystery Realm",
                is_private=True,
            ),
        ]

    def _get_rental_channels(self) -> List[DiscordChannel]:
        """Get rental channels that can be rented with RP"""
        return [
            # Premium Voice Channels
            DiscordChannel(
                name="premium-voice-1",
                channel_type=ChannelType.VOICE,
                category=ChannelCategory.VIP_PRIVATE_ROOM,
                description="Premium voice channel - Rent with RP",
                permissions={
                    "@everyone": ["connect", "speak"],
                },
                rental_cost=50,  # 50 RP per hour
                rental_duration=1,  # 1 hour
            ),
            DiscordChannel(
                name="premium-voice-2",
                channel_type=ChannelType.VOICE,
                category=ChannelCategory.VIP_PRIVATE_ROOM,
                description="Premium voice channel - Rent with RP",
                permissions={
                    "@everyone": ["connect", "speak"],
                },
                rental_cost=50,
                rental_duration=1,
            ),
            # Private Meeting Rooms
            DiscordChannel(
                name="private-meeting-1",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.VIP_PRIVATE_ROOM,
                description="Private meeting room - Rent with RP",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
                rental_cost=100,  # 100 RP per hour
                rental_duration=1,
            ),
            DiscordChannel(
                name="private-meeting-2",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.VIP_PRIVATE_ROOM,
                description="Private meeting room - Rent with RP",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
                rental_cost=100,
                rental_duration=1,
            ),
            # Strategy Rooms
            DiscordChannel(
                name="strategy-room-1",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.VIP_PRIVATE_ROOM,
                description="Strategy planning room - Rent with RP",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
                rental_cost=75,  # 75 RP per hour
                rental_duration=1,
            ),
            DiscordChannel(
                name="strategy-room-2",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.VIP_PRIVATE_ROOM,
                description="Strategy planning room - Rent with RP",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
                rental_cost=75,
                rental_duration=1,
            ),
            # Event Rooms
            DiscordChannel(
                name="event-room-1",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.VIP_PRIVATE_ROOM,
                description="Event hosting room - Rent with RP",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
                rental_cost=150,  # 150 RP per hour
                rental_duration=2,  # 2 hours
            ),
            DiscordChannel(
                name="event-room-2",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.VIP_PRIVATE_ROOM,
                description="Event hosting room - Rent with RP",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
                rental_cost=150,
                rental_duration=2,
            ),
            # Training Rooms
            DiscordChannel(
                name="training-room-1",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.VIP_PRIVATE_ROOM,
                description="Training and practice room - Rent with RP",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
                rental_cost=60,  # 60 RP per hour
                rental_duration=1,
            ),
            DiscordChannel(
                name="training-room-2",
                channel_type=ChannelType.TEXT,
                category=ChannelCategory.VIP_PRIVATE_ROOM,
                description="Training and practice room - Rent with RP",
                permissions={
                    "@everyone": ["read_messages", "send_messages"],
                },
                rental_cost=60,
                rental_duration=1,
            ),
        ]

    def _get_channel_permissions(self) -> Dict[str, Dict[str, List[str]]]:
        """Get detailed channel permissions"""
        return {
            "world_permissions": {
                "@everyone": ["read_messages"],
                "Citizen": ["read_messages", "send_messages", "use_external_emojis"],
                "Moderator": [
                    "read_messages",
                    "send_messages",
                    "manage_messages",
                    "kick_members",
                    "ban_members",
                    "manage_roles",
                ],
                "Ruler": [
                    "read_messages",
                    "send_messages",
                    "manage_messages",
                    "manage_channels",
                    "manage_roles",
                    "manage_guild",
                ],
            },
            "kingdom_permissions": {
                "Citizen": ["read_messages", "send_messages", "use_external_emojis"],
                "Moderator": [
                    "read_messages",
                    "send_messages",
                    "manage_messages",
                    "kick_members",
                    "manage_roles",
                ],
                "Ruler": [
                    "read_messages",
                    "send_messages",
                    "manage_messages",
                    "manage_channels",
                    "manage_roles",
                ],
            },
            "council_permissions": {
                "Ruler": [
                    "read_messages",
                    "send_messages",
                    "manage_messages",
                    "manage_channels",
                    "manage_roles",
                ]
            },
            "community_permissions": {
                "@everyone": ["read_messages"],
                "Citizen": ["read_messages", "send_messages", "use_external_emojis"],
                "Moderator": [
                    "read_messages",
                    "send_messages",
                    "manage_messages",
                    "kick_members",
                    "ban_members",
                    "manage_roles",
                    "manage_guild",
                ],
                "Ruler": [
                    "read_messages",
                    "send_messages",
                    "manage_messages",
                    "manage_channels",
                    "manage_roles",
                    "manage_guild",
                ],
            },
        }

    def get_channel_list(
        self,
        kingdom_id: str = None,
        include_private: bool = False,
        include_rental: bool = False,
    ) -> List[Dict]:
        """Get list of channels for a specific kingdom or all world channels"""
        channels = []

        if kingdom_id:
            if kingdom_id in self.channel_structure["kingdom_channels"]:
                channels.extend(
                    [
                        {
                            "name": channel.name,
                            "type": channel.channel_type.value,
                            "category": channel.category.value,
                            "description": channel.description,
                            "kingdom": channel.kingdom_name,
                            "is_private": channel.is_private,
                        }
                        for channel in self.channel_structure["kingdom_channels"][
                            kingdom_id
                        ]
                    ]
                )
        else:
            channels.extend(
                [
                    {
                        "name": channel.name,
                        "type": channel.channel_type.value,
                        "category": channel.category.value,
                        "description": channel.description,
                        "is_private": channel.is_private,
                        "resource_type": channel.resource_type,
                        "gather_cooldown": channel.gather_cooldown,
                    }
                    for channel in self.channel_structure["world_channels"]
                ]
            )

        # Add private channels if requested
        if include_private:
            channels.extend(
                [
                    {
                        "name": channel.name,
                        "type": channel.channel_type.value,
                        "category": channel.category.value,
                        "description": channel.description,
                        "kingdom": channel.kingdom_name,
                        "is_private": channel.is_private,
                    }
                    for channel in self.channel_structure["private_channels"]
                ]
            )

        # Add rental channels if requested
        if include_rental:
            channels.extend(
                [
                    {
                        "name": channel.name,
                        "type": channel.channel_type.value,
                        "category": channel.category.value,
                        "description": channel.description,
                        "rental_cost": channel.rental_cost,
                        "rental_duration": channel.rental_duration,
                        "is_private": channel.is_private,
                    }
                    for channel in self.channel_structure["rental_channels"]
                ]
            )

        return channels

    def get_kingdom_channels(self, kingdom_id: str) -> List[DiscordChannel]:
        """Get channels for a specific kingdom"""
        return self.channel_structure["kingdom_channels"].get(kingdom_id, [])

    def get_world_channels(self) -> List[DiscordChannel]:
        """Get all world channels"""
        return self.channel_structure["world_channels"]

    def get_subscription_channel_access(self, tier: str) -> Dict[str, List[str]]:
        """Get channel access based on subscription tier"""
        access = {
            "tier_1": {
                "world_channels": [
                    "welcome",
                    "commands",
                    "leaderboard",
                    "shop",
                    "science",
                    "survival-arena",
                    "support",
                ],
                "kingdom_channels": ["general", "voice"],
                "restrictions": ["No moderation access", "No council access"],
            },
            "tier_2": {
                "world_channels": [
                    "welcome",
                    "commands",
                    "leaderboard",
                    "shop",
                    "science",
                    "survival-arena",
                    "events",
                    "achievements",
                    "support",
                ],
                "kingdom_channels": ["general", "strategy", "voice", "special"],
                "moderation": ["manage_messages", "kick_members"],
                "restrictions": ["No council access"],
            },
            "tier_3": {
                "world_channels": ["all"],
                "kingdom_channels": ["all"],
                "council_access": True,
                "moderation": ["all_moderation_powers"],
                "ruler_eligibility": True,
            },
        }

        return access.get(tier, access["tier_1"])

    def get_total_channel_count(self) -> int:
        """Get total number of channels"""
        world_count = len(self.channel_structure["world_channels"])
        kingdom_count = sum(
            len(channels)
            for channels in self.channel_structure["kingdom_channels"].values()
        )
        private_count = len(self.channel_structure["private_channels"])
        rental_count = len(self.channel_structure["rental_channels"])
        return world_count + kingdom_count + private_count + rental_count

    def get_kingdom_channel_count(self, kingdom_id: str) -> int:
        """Get channel count for a specific kingdom"""
        return len(self.channel_structure["kingdom_channels"].get(kingdom_id, []))

    def get_private_channels(self) -> List[DiscordChannel]:
        """Get all private channels"""
        return self.channel_structure["private_channels"]

    def get_rental_channels(self) -> List[DiscordChannel]:
        """Get all rental channels"""
        return self.channel_structure["rental_channels"]

    def get_rental_channel_info(self, channel_name: str) -> Dict:
        """Get rental information for a specific channel"""
        for channel in self.channel_structure["rental_channels"]:
            if channel.name == channel_name:
                return {
                    "name": channel.name,
                    "type": channel.channel_type.value,
                    "description": channel.description,
                    "rental_cost": channel.rental_cost,
                    "rental_duration": channel.rental_duration,
                }
        return None

    def get_available_rental_channels(self) -> List[Dict]:
        """Get list of available rental channels"""
        return [
            {
                "name": channel.name,
                "type": channel.channel_type.value,
                "description": channel.description,
                "rental_cost": channel.rental_cost,
                "rental_duration": channel.rental_duration,
            }
            for channel in self.channel_structure["rental_channels"]
        ]

    def get_community_channels(self) -> List[Dict]:
        """Get list of community-specific channels"""
        community_channels = [
            "welcome",
            "rules",
            "verify",
            "guidelines",
            "general",
            "off-topic",
            "suggestions",
            "support",
            "Community Voice",
        ]

        return [
            {
                "name": channel.name,
                "type": channel.channel_type.value,
                "category": channel.category.value,
                "description": channel.description,
                "is_community": channel.name in community_channels,
            }
            for channel in self.channel_structure["world_channels"]
            if channel.name in community_channels
        ]

    def get_verification_channels(self) -> List[Dict]:
        """Get channels related to member verification"""
        return [
            {
                "name": channel.name,
                "type": channel.channel_type.value,
                "description": channel.description,
                "permissions": channel.permissions,
            }
            for channel in self.channel_structure["world_channels"]
            if channel.name in ["verify", "rules", "guidelines"]
        ]

    def get_community_roles(self) -> Dict[str, List[str]]:
        """Get community server roles and permissions"""
        return {
            "@everyone": ["read_messages"],
            "Citizen": [
                "read_messages",
                "send_messages",
                "use_external_emojis",
                "add_reactions",
            ],
            "Moderator": [
                "read_messages",
                "send_messages",
                "manage_messages",
                "kick_members",
                "ban_members",
                "manage_roles",
                "use_external_emojis",
                "add_reactions",
            ],
            "Ruler": [
                "read_messages",
                "send_messages",
                "manage_messages",
                "manage_channels",
                "manage_roles",
                "manage_guild",
                "use_external_emojis",
                "add_reactions",
            ],
            "Community Manager": [
                "read_messages",
                "send_messages",
                "manage_messages",
                "manage_channels",
                "manage_roles",
                "kick_members",
                "ban_members",
                "use_external_emojis",
                "add_reactions",
            ],
        }

    def get_community_features(self) -> Dict[str, Any]:
        """Get community server features and settings"""
        return {
            "verification_level": "medium",
            "explicit_content_filter": "all_members",
            "default_notifications": "all_messages",
            "system_channel": "welcome",
            "rules_channel": "rules",
            "public_updates_channel": "welcome",
            "premium_tier": 0,
            "features": ["COMMUNITY", "VERIFIED", "DISCOVERABLE", "FEATURABLE"],
            "community_settings": {
                "invites_disabled": False,
                "widget_enabled": True,
                "widget_channel": "general",
                "system_channel_flags": 0,
            },
        }

    def get_hunting_zones(self) -> List[Dict]:
        """Get all hunting zones for wild simulacra"""
        hunting_zones = []
        for channel in self.channel_structure["world_channels"]:
            if channel.name.startswith("hunting-zone-"):
                hunting_zones.append(
                    {
                        "name": channel.name,
                        "display_name": channel.description.split(" - ")[0],
                        "description": channel.description,
                        "zone_id": channel.name.split("-")[-1],
                        "element": self._get_zone_element(channel.name),
                        "spawn_rate": self._get_zone_spawn_rate(channel.name),
                        "breathing_multiplier": self._get_zone_breathing_multiplier(
                            channel.name
                        ),
                    }
                )
        return hunting_zones

    def _get_zone_element(self, zone_name: str) -> str:
        """Get the elemental affinity of a hunting zone"""
        zone_elements = {
            "hunting-zone-1": "Nature",  # Verdant Valley
            "hunting-zone-2": "Crystal",  # Crystal Peaks
            "hunting-zone-3": "Water",  # Azure Depths
            "hunting-zone-4": "Fire",  # Ember Wastes
            "hunting-zone-5": "Lightning",  # Storm Ridge
            "hunting-zone-6": "Ice",  # Frost Hollow
            "hunting-zone-7": "Air",  # Whisperspire
            "hunting-zone-8": "Shadow",  # Shadow Vale
            "hunting-zone-9": "Light",  # Dawn Plains
            "hunting-zone-10": "Void",  # Void Nexus
        }
        return zone_elements.get(zone_name, "Unknown")

    def _get_zone_spawn_rate(self, zone_name: str) -> float:
        """Get base spawn rate for a hunting zone"""
        zone_rates = {
            "hunting-zone-1": 0.15,  # Verdant Valley - Common
            "hunting-zone-2": 0.12,  # Crystal Peaks - Uncommon
            "hunting-zone-3": 0.10,  # Azure Depths - Rare
            "hunting-zone-4": 0.08,  # Ember Wastes - Epic
            "hunting-zone-5": 0.06,  # Storm Ridge - Legendary
            "hunting-zone-6": 0.05,  # Frost Hollow - Mythic
            "hunting-zone-7": 0.04,  # Whisperspire - Ultra Rare
            "hunting-zone-8": 0.03,  # Shadow Vale - Shadow Rare
            "hunting-zone-9": 0.02,  # Dawn Plains - Light Rare
            "hunting-zone-10": 0.01,  # Void Nexus - Void Rare
        }
        return zone_rates.get(zone_name, 0.10)

    def _get_zone_breathing_multiplier(self, zone_name: str) -> float:
        """Get breathing rhythm multiplier for a hunting zone"""
        zone_multipliers = {
            "hunting-zone-1": 1.2,  # Verdant Valley - Nature breathing
            "hunting-zone-2": 1.5,  # Crystal Peaks - Crystal resonance
            "hunting-zone-3": 1.3,  # Azure Depths - Water flow
            "hunting-zone-4": 1.8,  # Ember Wastes - Fire intensity
            "hunting-zone-5": 2.0,  # Storm Ridge - Lightning power
            "hunting-zone-6": 1.6,  # Frost Hollow - Ice stillness
            "hunting-zone-7": 1.4,  # Whisperspire - Air currents
            "hunting-zone-8": 2.2,  # Shadow Vale - Shadow mystery
            "hunting-zone-9": 1.7,  # Dawn Plains - Light purity
            "hunting-zone-10": 3.0,  # Void Nexus - Void chaos
        }
        return zone_multipliers.get(zone_name, 1.0)

    def get_hunting_mechanics(self) -> Dict[str, Any]:
        """Get hunting mechanics and rules"""
        return {
            "hunt_cost": {
                "basic_hunt": 10,  # 10 RP per hunt
                "advanced_hunt": 25,  # 25 RP per hunt
                "master_hunt": 50,  # 50 RP per hunt
                "legendary_hunt": 100,  # 100 RP per hunt
            },
            "hunt_success_rates": {
                "basic_hunt": 0.15,  # 15% success rate
                "advanced_hunt": 0.25,  # 25% success rate
                "master_hunt": 0.40,  # 40% success rate
                "legendary_hunt": 0.60,  # 60% success rate
            },
            "breathing_effects": {
                "calm": 0.5,  # Calm breathing - 50% spawn rate
                "normal": 1.0,  # Normal breathing - 100% spawn rate
                "intense": 1.5,  # Intense breathing - 150% spawn rate
                "frenzied": 2.0,  # Frenzied breathing - 200% spawn rate
            },
            "hunt_cooldowns": {
                "basic_hunt": 300,  # 5 minutes
                "advanced_hunt": 600,  # 10 minutes
                "master_hunt": 1200,  # 20 minutes
                "legendary_hunt": 3600,  # 1 hour
            },
            "special_events": {
                "breathing_surge": "Random breathing rhythm increases spawn rates by 300%",
                "elemental_convergence": "All zones of same element get 200% spawn rate",
                "void_awakening": "Void Nexus gets 500% spawn rate for 1 hour",
                "crystal_resonance": "Crystal Peaks gets 400% spawn rate for 30 minutes",
            },
        }

    def get_breathing_rhythm_messages(self) -> Dict[str, List[str]]:
        """Get breathing rhythm messages for each zone"""
        return {
            "hunting-zone-1": [  # Verdant Valley
                "🌿 The valley breathes with ancient life...",
                "🌿 Verdant energy pulses through the air...",
                "🌿 Nature's rhythm grows stronger...",
                "🌿 The valley's heartbeat quickens...",
            ],
            "hunting-zone-2": [  # Crystal Peaks
                "🏔️ Crystals resonate with cosmic energy...",
                "🏔️ The peaks hum with crystalline power...",
                "🏔️ Crystal vibrations intensify...",
                "🏔️ The mountains sing with ancient magic...",
            ],
            "hunting-zone-3": [  # Azure Depths
                "🌊 Deep currents flow with mysterious energy...",
                "🌊 The depths pulse with aquatic life...",
                "🌊 Water's rhythm grows more intense...",
                "🌊 The ocean's heartbeat quickens...",
            ],
            "hunting-zone-4": [  # Ember Wastes
                "🔥 Flames dance with primal fury...",
                "🔥 The wastes burn with ancient power...",
                "🔥 Fire's intensity reaches new heights...",
                "🔥 The inferno's rhythm grows wild...",
            ],
            "hunting-zone-5": [  # Storm Ridge
                "⚡ Lightning crackles with raw energy...",
                "⚡ The storm's power electrifies the air...",
                "⚡ Thunder's rhythm grows deafening...",
                "⚡ The tempest's fury reaches its peak...",
            ],
            "hunting-zone-6": [  # Frost Hollow
                "❄️ Ice crystals form with silent precision...",
                "❄️ The hollow freezes with ancient cold...",
                "❄️ Frost's stillness grows deeper...",
                "❄️ The ice's rhythm becomes absolute...",
            ],
            "hunting-zone-7": [  # Whisperspire
                "🌪️ Wind whispers with ethereal voices...",
                "🌪️ The spire channels air's ancient power...",
                "🌪️ Breeze's rhythm grows more complex...",
                "🌪️ The wind's song reaches new heights...",
            ],
            "hunting-zone-8": [  # Shadow Vale
                "🌙 Shadows dance with mysterious intent...",
                "🌙 The vale pulses with dark energy...",
                "🌙 Shadow's rhythm grows more intense...",
                "🌙 The darkness's heartbeat quickens...",
            ],
            "hunting-zone-9": [  # Dawn Plains
                "🌅 Light radiates with pure energy...",
                "🌅 The plains glow with divine power...",
                "🌅 Dawn's rhythm grows more radiant...",
                "🌅 The light's pulse reaches new heights...",
            ],
            "hunting-zone-10": [  # Void Nexus
                "🌌 The void churns with chaotic energy...",
                "🌌 Reality itself bends to the nexus...",
                "🌌 Void's rhythm defies all logic...",
                "🌌 The chaos reaches its absolute peak...",
            ],
        }

    def get_resource_gathering_channels(self) -> List[Dict]:
        """Get all resource gathering channels with their mechanics"""
        resource_channels = []
        for channel in self.channel_structure["world_channels"]:
            if channel.resource_type:
                resource_channels.append(
                    {
                        "name": channel.name,
                        "resource_type": channel.resource_type,
                        "description": channel.description,
                        "gather_cooldown": channel.gather_cooldown,
                        "permissions": channel.permissions,
                    }
                )
        return resource_channels

    def get_resource_gathering_mechanics(self) -> Dict[str, Any]:
        """Get resource gathering mechanics and rules"""
        return {
            "gathering_rules": {
                "time_based_gathering": {
                    "interval": 10,  # seconds
                    "amount": 1,  # resource per interval
                    "description": "Every 10 seconds you stay in a channel, you gather 1 resource",
                },
                "message_based_gathering": {
                    "amount": 1,  # resource per message
                    "cooldown_range": [5, 60],  # seconds
                    "description": "Every message you send gives 1 resource, with a cooldown",
                },
                "resource_types": {
                    "wood": {
                        "emoji": "🌳",
                        "description": "Basic building material",
                        "cooldown": 30,
                        "rarity": "common",
                    },
                    "stone": {
                        "emoji": "🪨",
                        "description": "Sturdy construction material",
                        "cooldown": 45,
                        "rarity": "common",
                    },
                    "metal": {
                        "emoji": "⚒️",
                        "description": "Advanced crafting material",
                        "cooldown": 60,
                        "rarity": "uncommon",
                    },
                    "crystal": {
                        "emoji": "💎",
                        "description": "Magical enhancement material",
                        "cooldown": 75,
                        "rarity": "rare",
                    },
                    "essence": {
                        "emoji": "✨",
                        "description": "Pure magical energy",
                        "cooldown": 90,
                        "rarity": "epic",
                    },
                },
            },
            "gathering_messages": {
                "wood": [
                    "🌳 You gather some sturdy wood from the forest...",
                    "🌳 The trees provide their bounty...",
                    "🌳 Wood chips scatter as you harvest...",
                    "🌳 Fresh timber is collected...",
                ],
                "stone": [
                    "🪨 You chip away at the solid rock...",
                    "🪨 Stone fragments break loose...",
                    "🪨 The earth yields its strength...",
                    "🪨 Rough stone is gathered...",
                ],
                "metal": [
                    "⚒️ You extract precious metal from the ore...",
                    "⚒️ The metal gleams as you harvest...",
                    "⚒️ Raw metal is collected...",
                    "⚒️ The earth's treasures are revealed...",
                ],
                "crystal": [
                    "💎 Crystals sparkle as you gather them...",
                    "💎 Magical energy pulses from the crystals...",
                    "💎 Pure crystal essence is collected...",
                    "💎 The gems resonate with power...",
                ],
                "essence": [
                    "✨ Pure essence flows into your collection...",
                    "✨ Magical energy coalesces...",
                    "✨ The essence shimmers with power...",
                    "✨ Raw magical force is harvested...",
                ],
            },
            "cooldown_messages": [
                "⏰ You're still gathering... wait a moment.",
                "⏰ The resource needs time to replenish...",
                "⏰ You're gathering too quickly... slow down.",
                "⏰ The area needs time to recover...",
            ],
            "food_system": {
                "basic_food_cost": 5,  # RP per food
                "hunger_drain_rate": 1,  # HP per second when at 0 hunger
                "basic_food_efficiency": 0.5,  # 50% efficiency for basic food
                "death_permanent": True,
                "description": "Simulacra need food for their type. Basic food works for all but at reduced rate. 0 hunger = lose HP per second. Death is permanent.",
            },
        }

    def get_resource_channel_info(self, channel_name: str) -> Dict:
        """Get specific resource channel information"""
        for channel in self.channel_structure["world_channels"]:
            if channel.name == channel_name and channel.resource_type:
                return {
                    "name": channel.name,
                    "resource_type": channel.resource_type,
                    "description": channel.description,
                    "gather_cooldown": channel.gather_cooldown,
                    "permissions": channel.permissions,
                }
        return None

    def get_available_resources(self) -> List[str]:
        """Get list of all available resource types"""
        resources = []
        for channel in self.channel_structure["world_channels"]:
            if channel.resource_type and channel.resource_type not in resources:
                resources.append(channel.resource_type)
        return resources

    def export_channel_structure(self) -> Dict:
        """Export complete channel structure for Discord setup"""
        return {
            "world_channels": [
                {
                    "name": channel.name,
                    "type": channel.channel_type.value,
                    "category": channel.category.value,
                    "description": channel.description,
                    "permissions": channel.permissions,
                    "is_private": channel.is_private,
                    "resource_type": channel.resource_type,
                    "gather_cooldown": channel.gather_cooldown,
                }
                for channel in self.channel_structure["world_channels"]
            ],
            "kingdom_channels": {
                kingdom_id: [
                    {
                        "name": channel.name,
                        "type": channel.channel_type.value,
                        "category": channel.category.value,
                        "description": channel.description,
                        "permissions": channel.permissions,
                        "kingdom": channel.kingdom_name,
                        "is_private": channel.is_private,
                    }
                    for channel in channels
                ]
                for kingdom_id, channels in self.channel_structure[
                    "kingdom_channels"
                ].items()
            },
            "private_channels": [
                {
                    "name": channel.name,
                    "type": channel.channel_type.value,
                    "category": channel.category.value,
                    "description": channel.description,
                    "permissions": channel.permissions,
                    "kingdom": channel.kingdom_name,
                    "is_private": channel.is_private,
                }
                for channel in self.channel_structure["private_channels"]
            ],
            "rental_channels": [
                {
                    "name": channel.name,
                    "type": channel.channel_type.value,
                    "category": channel.category.value,
                    "description": channel.description,
                    "permissions": channel.permissions,
                    "rental_cost": channel.rental_cost,
                    "rental_duration": channel.rental_duration,
                    "is_private": channel.is_private,
                }
                for channel in self.channel_structure["rental_channels"]
            ],
            "permissions": self.channel_structure["channel_permissions"],
            "total_channels": self.get_total_channel_count(),
            "kingdoms": list(self.channel_structure["kingdom_channels"].keys()),
        }
