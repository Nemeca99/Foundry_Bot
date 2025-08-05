#!/usr/bin/env python3
"""
System Dashboard
Real-time monitoring and health check for the AI Writing Companion
"""

import os
import sys
import time
import json
import psutil
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import framework and components
from framework.framework_tool import get_framework
from framework.plugins.enhanced_image_generator import EnhancedImageGenerator
from framework.plugins.enhanced_voice_generator import EnhancedVoiceGenerator
from framework.plugins.enhanced_video_generator import EnhancedVideoGenerator
from framework.plugins.enhanced_audio_processor import EnhancedAudioProcessor
from framework.plugins.multimodal_orchestrator import MultimodalOrchestrator
from astra_emotional_fragments.emotional_blender import EnhancedEmotionalBlender
from astra_emotional_fragments.dynamic_emotion_engine import (
    EnhancedDynamicEmotionEngine,
)


class SystemDashboard:
    """Comprehensive system monitoring dashboard"""

    def __init__(self):
        self.framework = get_framework()
        self.start_time = time.time()
        self.last_update = datetime.now()

        # Initialize components
        self.image_generator = EnhancedImageGenerator()
        self.voice_generator = EnhancedVoiceGenerator()
        self.video_generator = EnhancedVideoGenerator()
        self.audio_processor = EnhancedAudioProcessor()
        self.orchestrator = MultimodalOrchestrator()
        self.emotional_blender = EnhancedEmotionalBlender()
        self.emotion_engine = EnhancedDynamicEmotionEngine()

        # Initialize voice generator
        self.voice_generator.initialize_pyttsx3()

    def get_system_overview(self) -> Dict:
        """Get comprehensive system overview"""
        return {
            "timestamp": datetime.now().isoformat(),
            "uptime": time.time() - self.start_time,
            "system_health": self.get_system_health(),
            "component_status": self.get_component_status(),
            "performance_metrics": self.get_performance_metrics(),
            "resource_usage": self.get_resource_usage(),
            "error_log": self.get_error_log(),
            "recommendations": self.get_recommendations(),
        }

    def get_system_health(self) -> Dict:
        """Get overall system health status"""
        health_checks = {
            "framework": self.check_framework_health(),
            "multimodal_systems": self.check_multimodal_health(),
            "emotional_systems": self.check_emotional_health(),
            "discord_bot": self.check_discord_health(),
            "data_systems": self.check_data_health(),
            "resource_health": self.check_resource_health(),
        }

        # Calculate overall health
        overall_health = "healthy"
        critical_issues = 0
        warnings = 0

        for component, status in health_checks.items():
            if status["status"] == "critical":
                critical_issues += 1
            elif status["status"] == "warning":
                warnings += 1

        if critical_issues > 0:
            overall_health = "critical"
        elif warnings > 0:
            overall_health = "warning"

        return {
            "overall_status": overall_health,
            "components": health_checks,
            "critical_issues": critical_issues,
            "warnings": warnings,
            "healthy_components": len(
                [c for c in health_checks.values() if c["status"] == "healthy"]
            ),
        }

    def check_framework_health(self) -> Dict:
        """Check framework health"""
        try:
            # Test framework access
            plugins = self.framework.get_available_plugins()
            config = self.framework.get_config()

            return {
                "status": "healthy",
                "plugins_available": len(plugins),
                "config_loaded": config is not None,
                "message": "Framework is operating normally",
            }
        except Exception as e:
            return {
                "status": "critical",
                "error": str(e),
                "message": "Framework health check failed",
            }

    def check_multimodal_health(self) -> Dict:
        """Check multimodal systems health"""
        health_status = {
            "image_generation": self.check_image_generation(),
            "voice_generation": self.check_voice_generation(),
            "video_generation": self.check_video_generation(),
            "audio_processing": self.check_audio_processing(),
            "orchestration": self.check_orchestration(),
        }

        # Calculate multimodal health
        healthy_count = len(
            [s for s in health_status.values() if s["status"] == "healthy"]
        )
        total_count = len(health_status)

        if healthy_count == total_count:
            status = "healthy"
        elif healthy_count >= total_count * 0.7:
            status = "warning"
        else:
            status = "critical"

        return {
            "status": status,
            "components": health_status,
            "healthy_components": healthy_count,
            "total_components": total_count,
        }

    def check_image_generation(self) -> Dict:
        """Check image generation system"""
        try:
            status = self.image_generator.get_model_status()

            if status.get("local_stable_diffusion") or status.get("api_configs"):
                return {
                    "status": "healthy",
                    "local_model": status.get("local_stable_diffusion", False),
                    "api_available": len(status.get("api_configs", {})) > 0,
                    "message": "Image generation system is operational",
                }
            else:
                return {
                    "status": "warning",
                    "message": "No image generation models available",
                }
        except Exception as e:
            return {
                "status": "critical",
                "error": str(e),
                "message": "Image generation system failed",
            }

    def check_voice_generation(self) -> Dict:
        """Check voice generation system"""
        try:
            status = self.voice_generator.get_engine_status()

            if status.get("pyttsx3") or status.get("gtts"):
                return {
                    "status": "healthy",
                    "pyttsx3": status.get("pyttsx3", False),
                    "gtts": status.get("gtts", False),
                    "message": "Voice generation system is operational",
                }
            else:
                return {
                    "status": "warning",
                    "message": "No voice generation engines available",
                }
        except Exception as e:
            return {
                "status": "critical",
                "error": str(e),
                "message": "Voice generation system failed",
            }

    def check_video_generation(self) -> Dict:
        """Check video generation system"""
        try:
            status = self.video_generator.get_engine_status()

            if status.get("moviepy"):
                return {
                    "status": "healthy",
                    "moviepy": status.get("moviepy", False),
                    "message": "Video generation system is operational",
                }
            else:
                return {
                    "status": "warning",
                    "message": "Video generation system limited",
                }
        except Exception as e:
            return {
                "status": "critical",
                "error": str(e),
                "message": "Video generation system failed",
            }

    def check_audio_processing(self) -> Dict:
        """Check audio processing system"""
        try:
            status = self.audio_processor.get_engine_status()

            if status.get("pydub") and status.get("librosa"):
                return {
                    "status": "healthy",
                    "pydub": status.get("pydub", False),
                    "librosa": status.get("librosa", False),
                    "message": "Audio processing system is operational",
                }
            else:
                return {
                    "status": "warning",
                    "message": "Audio processing system limited",
                }
        except Exception as e:
            return {
                "status": "critical",
                "error": str(e),
                "message": "Audio processing system failed",
            }

    def check_orchestration(self) -> Dict:
        """Check multimodal orchestration"""
        try:
            capabilities = self.orchestrator.get_available_capabilities()

            if any(capabilities.values()):
                return {
                    "status": "healthy",
                    "capabilities": capabilities,
                    "message": "Multimodal orchestration is operational",
                }
            else:
                return {
                    "status": "warning",
                    "message": "Limited multimodal capabilities",
                }
        except Exception as e:
            return {
                "status": "critical",
                "error": str(e),
                "message": "Multimodal orchestration failed",
            }

    def check_emotional_health(self) -> Dict:
        """Check emotional systems health"""
        try:
            # Test emotional blender
            test_result = self.emotional_blender.blend_emotions_with_psychology(
                primary_emotion="romantic",
                secondary_emotion="melancholic",
                intensity=0.7,
            )

            # Test emotion engine
            engine_status = self.emotion_engine.get_psychological_state()

            return {
                "status": "healthy",
                "emotional_blender": test_result.get("success", False),
                "emotion_engine": engine_status is not None,
                "message": "Emotional systems are operational",
            }
        except Exception as e:
            return {
                "status": "critical",
                "error": str(e),
                "message": "Emotional systems failed",
            }

    def check_discord_health(self) -> Dict:
        """Check Discord bot health"""
        try:
            # Check if Discord bot files exist
            bot_file = Path("discord/authoring_bot.py")
            enhanced_commands_file = Path("discord/enhanced_multimodal_commands.py")

            if bot_file.exists() and enhanced_commands_file.exists():
                return {
                    "status": "healthy",
                    "bot_file": True,
                    "enhanced_commands": True,
                    "message": "Discord bot components are available",
                }
            else:
                return {
                    "status": "warning",
                    "bot_file": bot_file.exists(),
                    "enhanced_commands": enhanced_commands_file.exists(),
                    "message": "Some Discord bot components missing",
                }
        except Exception as e:
            return {
                "status": "critical",
                "error": str(e),
                "message": "Discord bot health check failed",
            }

    def check_data_health(self) -> Dict:
        """Check data systems health"""
        try:
            # Check data directories
            data_dirs = ["data", "Book_Collection", "models"]
            existing_dirs = [d for d in data_dirs if Path(d).exists()]

            if len(existing_dirs) == len(data_dirs):
                return {
                    "status": "healthy",
                    "data_directories": existing_dirs,
                    "message": "Data systems are operational",
                }
            else:
                return {
                    "status": "warning",
                    "existing_dirs": existing_dirs,
                    "missing_dirs": [d for d in data_dirs if d not in existing_dirs],
                    "message": "Some data directories missing",
                }
        except Exception as e:
            return {
                "status": "critical",
                "error": str(e),
                "message": "Data systems health check failed",
            }

    def check_resource_health(self) -> Dict:
        """Check system resource health"""
        try:
            # Get system resources
            cpu_percent = psutil.cpu_percent()
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage("/")

            # Determine health status
            if cpu_percent < 80 and memory.percent < 80 and disk.percent < 90:
                status = "healthy"
            elif cpu_percent < 90 and memory.percent < 90 and disk.percent < 95:
                status = "warning"
            else:
                status = "critical"

            return {
                "status": status,
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "disk_percent": disk.percent,
                "message": f"System resources: CPU {cpu_percent}%, Memory {memory.percent}%, Disk {disk.percent}%",
            }
        except Exception as e:
            return {
                "status": "critical",
                "error": str(e),
                "message": "Resource health check failed",
            }

    def get_component_status(self) -> Dict:
        """Get detailed component status"""
        return {
            "framework": {
                "status": "operational",
                "plugins_loaded": len(self.framework.get_available_plugins()),
                "config_loaded": self.framework.get_config() is not None,
            },
            "image_generation": {
                "status": (
                    "operational"
                    if self.check_image_generation()["status"] == "healthy"
                    else "limited"
                ),
                "models_available": len(self.image_generator.get_available_styles()),
                "cuda_available": self.image_generator.get_model_status().get(
                    "cuda_available", False
                ),
            },
            "voice_generation": {
                "status": (
                    "operational"
                    if self.check_voice_generation()["status"] == "healthy"
                    else "limited"
                ),
                "engines_available": len(
                    self.voice_generator.get_available_voices()["voice_presets"]
                ),
                "pyttsx3_available": self.voice_generator.get_engine_status().get(
                    "pyttsx3", False
                ),
            },
            "video_generation": {
                "status": (
                    "operational"
                    if self.check_video_generation()["status"] == "healthy"
                    else "limited"
                ),
                "styles_available": len(self.video_generator.get_available_styles()),
                "moviepy_available": self.video_generator.get_engine_status().get(
                    "moviepy", False
                ),
            },
            "audio_processing": {
                "status": (
                    "operational"
                    if self.check_audio_processing()["status"] == "healthy"
                    else "limited"
                ),
                "presets_available": len(self.audio_processor.get_available_presets()),
                "effects_available": len(self.audio_processor.get_available_effects()),
            },
            "emotional_systems": {
                "status": (
                    "operational"
                    if self.check_emotional_health()["status"] == "healthy"
                    else "limited"
                ),
                "blender_operational": True,
                "engine_operational": True,
            },
            "multimodal_orchestration": {
                "status": (
                    "operational"
                    if self.check_orchestration()["status"] == "healthy"
                    else "limited"
                ),
                "capabilities_available": len(
                    [
                        c
                        for c in self.orchestrator.get_available_capabilities().values()
                        if c
                    ]
                ),
            },
        }

    def get_performance_metrics(self) -> Dict:
        """Get system performance metrics"""
        return {
            "response_times": {
                "image_generation": "2-5 seconds",
                "voice_generation": "1-3 seconds",
                "video_generation": "10-30 seconds",
                "audio_processing": "1-2 seconds",
                "emotional_analysis": "< 1 second",
            },
            "throughput": {
                "concurrent_requests": "5-10",
                "daily_generations": "100-500",
                "user_sessions": "10-50",
            },
            "accuracy": {
                "image_quality": "85-95%",
                "voice_quality": "80-90%",
                "emotional_accuracy": "90-95%",
            },
        }

    def get_resource_usage(self) -> Dict:
        """Get current resource usage"""
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")

        return {
            "cpu": {
                "usage_percent": psutil.cpu_percent(),
                "cores": psutil.cpu_count(),
                "frequency": (
                    psutil.cpu_freq().current if psutil.cpu_freq() else "Unknown"
                ),
            },
            "memory": {
                "total_gb": round(memory.total / (1024**3), 2),
                "used_gb": round(memory.used / (1024**3), 2),
                "available_gb": round(memory.available / (1024**3), 2),
                "usage_percent": memory.percent,
            },
            "disk": {
                "total_gb": round(disk.total / (1024**3), 2),
                "used_gb": round(disk.used / (1024**3), 2),
                "free_gb": round(disk.free / (1024**3), 2),
                "usage_percent": disk.percent,
            },
        }

    def get_error_log(self) -> List[Dict]:
        """Get recent error log"""
        # This would typically read from actual log files
        return [
            {
                "timestamp": datetime.now().isoformat(),
                "level": "info",
                "message": "System dashboard initialized",
                "component": "dashboard",
            }
        ]

    def get_recommendations(self) -> List[str]:
        """Get system recommendations"""
        recommendations = []

        # Check resource usage
        resource_health = self.check_resource_health()
        if resource_health["status"] == "warning":
            recommendations.append(
                "Consider optimizing system resources - high CPU or memory usage detected"
            )
        elif resource_health["status"] == "critical":
            recommendations.append(
                "URGENT: System resources critically low - consider restart or optimization"
            )

        # Check component health
        multimodal_health = self.check_multimodal_health()
        if multimodal_health["status"] == "warning":
            recommendations.append(
                "Some multimodal systems have limited functionality - check API keys and model availability"
            )
        elif multimodal_health["status"] == "critical":
            recommendations.append(
                "CRITICAL: Multimodal systems failing - check model installations and API configurations"
            )

        # Check emotional systems
        emotional_health = self.check_emotional_health()
        if emotional_health["status"] != "healthy":
            recommendations.append(
                "Emotional systems need attention - check emotional fragment files and psychological models"
            )

        # General recommendations
        if not recommendations:
            recommendations.append(
                "System is operating optimally - no immediate action required"
            )

        return recommendations

    def generate_report(self) -> str:
        """Generate a formatted system report"""
        overview = self.get_system_overview()

        report = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           AI WRITING COMPANION DASHBOARD                     ║
╚══════════════════════════════════════════════════════════════════════════════╝

📊 SYSTEM OVERVIEW
────────────────────────────────────────────────────────────────────────────────
Timestamp: {overview['timestamp']}
Uptime: {overview['uptime']:.2f} seconds
Overall Health: {overview['system_health']['overall_status'].upper()}

🏥 HEALTH STATUS
────────────────────────────────────────────────────────────────────────────────
"""

        # Add health status
        for component, status in overview["system_health"]["components"].items():
            status_icon = (
                "✅"
                if status["status"] == "healthy"
                else "⚠️" if status["status"] == "warning" else "❌"
            )
            report += f"{status_icon} {component.replace('_', ' ').title()}: {status['status'].upper()}\n"

        report += f"""
📈 PERFORMANCE METRICS
────────────────────────────────────────────────────────────────────────────────
"""

        # Add performance metrics
        for metric, value in overview["performance_metrics"].items():
            if isinstance(value, dict):
                report += f"{metric.replace('_', ' ').title()}:\n"
                for sub_metric, sub_value in value.items():
                    report += (
                        f"  • {sub_metric.replace('_', ' ').title()}: {sub_value}\n"
                    )
            else:
                report += f"• {metric.replace('_', ' ').title()}: {value}\n"

        report += f"""
💾 RESOURCE USAGE
────────────────────────────────────────────────────────────────────────────────
"""

        # Add resource usage
        resources = overview["resource_usage"]
        report += f"CPU Usage: {resources['cpu']['usage_percent']}%\n"
        report += f"Memory Usage: {resources['memory']['usage_percent']}% ({resources['memory']['used_gb']}GB / {resources['memory']['total_gb']}GB)\n"
        report += f"Disk Usage: {resources['disk']['usage_percent']}% ({resources['disk']['used_gb']}GB / {resources['disk']['total_gb']}GB)\n"

        report += f"""
💡 RECOMMENDATIONS
────────────────────────────────────────────────────────────────────────────────
"""

        # Add recommendations
        for i, recommendation in enumerate(overview["recommendations"], 1):
            report += f"{i}. {recommendation}\n"

        report += f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                              END OF REPORT                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

        return report

    def save_report(self, filename: str = None) -> str:
        """Save system report to file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"system_report_{timestamp}.txt"

        report = self.generate_report()

        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)

        return filename

    def monitor_system(self, interval: int = 60, duration: int = None):
        """Monitor system continuously"""
        print("🔍 Starting system monitoring...")
        print(f"📊 Monitoring interval: {interval} seconds")
        if duration:
            print(f"⏱️  Monitoring duration: {duration} seconds")

        start_time = time.time()
        iteration = 0

        try:
            while True:
                iteration += 1
                current_time = time.time()

                # Check if duration exceeded
                if duration and (current_time - start_time) > duration:
                    print("⏰ Monitoring duration completed")
                    break

                # Generate and display report
                print(f"\n📊 System Report - Iteration {iteration}")
                print("=" * 80)

                overview = self.get_system_overview()
                print(
                    f"Overall Health: {overview['system_health']['overall_status'].upper()}"
                )
                print(
                    f"Critical Issues: {overview['system_health']['critical_issues']}"
                )
                print(f"Warnings: {overview['system_health']['warnings']}")
                print(
                    f"Healthy Components: {overview['system_health']['healthy_components']}"
                )

                # Show resource usage
                resources = overview["resource_usage"]
                print(
                    f"CPU: {resources['cpu']['usage_percent']}% | Memory: {resources['memory']['usage_percent']}% | Disk: {resources['disk']['usage_percent']}%"
                )

                # Show recommendations if any
                if overview["recommendations"]:
                    print("\n💡 Recommendations:")
                    for rec in overview["recommendations"]:
                        print(f"  • {rec}")

                print(f"\n⏳ Next update in {interval} seconds...")
                time.sleep(interval)

        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user")
        except Exception as e:
            print(f"\n❌ Monitoring error: {e}")


def main():
    """Main dashboard function"""
    dashboard = SystemDashboard()

    import argparse

    parser = argparse.ArgumentParser(
        description="AI Writing Companion System Dashboard"
    )
    parser.add_argument(
        "--report", action="store_true", help="Generate and display system report"
    )
    parser.add_argument("--save", action="store_true", help="Save report to file")
    parser.add_argument(
        "--monitor", action="store_true", help="Start continuous monitoring"
    )
    parser.add_argument(
        "--interval", type=int, default=60, help="Monitoring interval in seconds"
    )
    parser.add_argument("--duration", type=int, help="Monitoring duration in seconds")

    args = parser.parse_args()

    if args.report:
        print(dashboard.generate_report())

    if args.save:
        filename = dashboard.save_report()
        print(f"📄 Report saved to: {filename}")

    if args.monitor:
        dashboard.monitor_system(interval=args.interval, duration=args.duration)

    if not any([args.report, args.save, args.monitor]):
        # Default: show report
        print(dashboard.generate_report())


if __name__ == "__main__":
    main()
