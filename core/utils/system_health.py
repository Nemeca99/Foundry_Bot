#!/usr/bin/env python3
"""
System Health Checker for Authoring Bot
Verifies all components are working properly
"""

import sys
import os
import json
import requests
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from config import Config
except ImportError:
    print("❌ Config not found. Please run setup first.")
    sys.exit(1)


class SystemHealthChecker:
    """Comprehensive system health checker"""

    def __init__(self):
        self.health_report = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "unknown",
            "components": {},
            "recommendations": [],
        }

    def check_config(self) -> Dict[str, Any]:
        """Check configuration validity"""
        print("🔧 Checking configuration...")

        try:
            errors = Config.validate()
            if errors:
                return {
                    "status": "error",
                    "message": f"Configuration errors: {errors}",
                    "details": {"errors": errors},
                }
            else:
                return {
                    "status": "healthy",
                    "message": "Configuration is valid",
                    "details": {
                        "discord_token": "✓ Set",
                        "lm_studio_url": Config.OLLAMA_BASE_URL,
                        "model_name": Config.OLLAMA_MODEL_NAME,
                        "timeout": Config.REQUEST_TIMEOUT,
                    },
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Configuration check failed: {e}",
                "details": {"error": str(e)},
            }

    def check_lm_studio_connection(self) -> Dict[str, Any]:
        """Check LM Studio connection"""
        print("🤖 Checking LM Studio connection...")

        try:
            # Test basic connection
            response = requests.get(f"{Config.OLLAMA_BASE_URL}/v1/models", timeout=10)

            if response.status_code == 200:
                models = response.json()
                model_found = any(
                    model.get("id", "").startswith(Config.OLLAMA_MODEL_NAME)
                    for model in models.get("data", [])
                )

                if model_found:
                    return {
                        "status": "healthy",
                        "message": "LM Studio is running and model is available",
                        "details": {
                            "url": Config.OLLAMA_BASE_URL,
                            "model": Config.OLLAMA_MODEL_NAME,
                            "available_models": len(models.get("data", [])),
                        },
                    }
                else:
                    return {
                        "status": "warning",
                        "message": "LM Studio is running but model not found",
                        "details": {
                            "url": Config.OLLAMA_BASE_URL,
                            "expected_model": Config.OLLAMA_MODEL_NAME,
                            "available_models": [
                                m.get("id") for m in models.get("data", [])
                            ],
                        },
                    }
            else:
                return {
                    "status": "error",
                    "message": f"LM Studio returned status {response.status_code}",
                    "details": {"status_code": response.status_code},
                }

        except requests.exceptions.ConnectionError:
            return {
                "status": "error",
                "message": "Cannot connect to LM Studio",
                "details": {"url": Config.OLLAMA_BASE_URL},
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"LM Studio check failed: {e}",
                "details": {"error": str(e)},
            }

    def check_discord_token(self) -> Dict[str, Any]:
        """Check Discord token validity"""
        print("📱 Checking Discord token...")

        try:
            import discord

            client = discord.Client(intents=discord.Intents.default())

            # Try to connect with the token
            response = requests.get(
                "https://discord.com/api/v10/users/@me",
                headers={"Authorization": f"Bot {Config.DISCORD_TOKEN}"},
                timeout=10,
            )

            if response.status_code == 200:
                bot_info = response.json()
                return {
                    "status": "healthy",
                    "message": "Discord token is valid",
                    "details": {
                        "bot_name": bot_info.get("username"),
                        "bot_id": bot_info.get("id"),
                        "application_id": bot_info.get("application_id"),
                    },
                }
            else:
                return {
                    "status": "error",
                    "message": f"Discord token validation failed: {response.status_code}",
                    "details": {"status_code": response.status_code},
                }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Discord token check failed: {e}",
                "details": {"error": str(e)},
            }

    def check_file_structure(self) -> Dict[str, Any]:
        """Check if all required files and folders exist"""
        print("📁 Checking file structure...")

        required_paths = [
            "config.py",
            "framework/framework_tool.py",
            "framework/plugins/",
            "discord/authoring_bot.py",
            "scripts/tests/",
            "scripts/tools/",
            "Book_Collection/",
            "data/",
            "models/",
        ]

        missing_paths = []
        existing_paths = []

        for path in required_paths:
            if os.path.exists(path):
                existing_paths.append(path)
            else:
                missing_paths.append(path)

        if missing_paths:
            return {
                "status": "warning",
                "message": f"Missing {len(missing_paths)} required paths",
                "details": {"missing": missing_paths, "existing": existing_paths},
            }
        else:
            return {
                "status": "healthy",
                "message": "All required paths exist",
                "details": {"paths": existing_paths},
            }

    def check_plugins(self) -> Dict[str, Any]:
        """Check if all plugins are loadable"""
        print("🔌 Checking plugins...")

        plugin_files = [
            "framework/plugins/text_generator.py",
            "framework/plugins/personality_engine.py",
            "framework/plugins/writing_assistant.py",
            "framework/plugins/personalization_engine.py",
            "framework/plugins/tool_manager.py",
            "framework/plugins/learning_engine.py",
            "framework/plugins/image_generator.py",
            "framework/plugins/video_generator.py",
            "framework/plugins/voice_generator.py",
        ]

        loadable_plugins = []
        failed_plugins = []

        for plugin_file in plugin_files:
            if os.path.exists(plugin_file):
                try:
                    # Try to import the plugin
                    spec = subprocess.run(
                        [
                            sys.executable,
                            "-c",
                            f"import sys; sys.path.insert(0, '{project_root}'); import {plugin_file.replace('/', '.').replace('.py', '')}",
                        ],
                        capture_output=True,
                        text=True,
                        timeout=30,
                    )

                    if spec.returncode == 0:
                        loadable_plugins.append(plugin_file)
                    else:
                        failed_plugins.append(
                            {"file": plugin_file, "error": spec.stderr}
                        )
                except Exception as e:
                    failed_plugins.append({"file": plugin_file, "error": str(e)})
            else:
                failed_plugins.append({"file": plugin_file, "error": "File not found"})

        if failed_plugins:
            return {
                "status": "warning",
                "message": f"{len(failed_plugins)} plugins failed to load",
                "details": {"loadable": loadable_plugins, "failed": failed_plugins},
            }
        else:
            return {
                "status": "healthy",
                "message": f"All {len(loadable_plugins)} plugins are loadable",
                "details": {"plugins": loadable_plugins},
            }

    def run_health_check(self):
        """Run comprehensive health check"""
        print("🏥 Starting System Health Check")
        print("=" * 50)

        # Run all checks
        checks = [
            ("Configuration", self.check_config),
            ("LM Studio Connection", self.check_lm_studio_connection),
            ("Discord Token", self.check_discord_token),
            ("File Structure", self.check_file_structure),
            ("Plugins", self.check_plugins),
        ]

        for check_name, check_func in checks:
            result = check_func()
            self.health_report["components"][check_name] = result

            status_icon = {"healthy": "✅", "warning": "⚠️", "error": "❌"}.get(
                result["status"], "❓"
            )

            print(f"{status_icon} {check_name}: {result['message']}")

        # Determine overall status
        statuses = [
            comp["status"] for comp in self.health_report["components"].values()
        ]
        if "error" in statuses:
            self.health_report["overall_status"] = "error"
        elif "warning" in statuses:
            self.health_report["overall_status"] = "warning"
        else:
            self.health_report["overall_status"] = "healthy"

        # Generate recommendations
        self._generate_recommendations()

        return self.health_report

    def _generate_recommendations(self):
        """Generate recommendations based on health check results"""
        recommendations = []

        for component_name, result in self.health_report["components"].items():
            if result["status"] == "error":
                if component_name == "Configuration":
                    recommendations.append(
                        "Run setup_bot.py to fix configuration issues"
                    )
                elif component_name == "LM Studio Connection":
                    recommendations.append(
                        "Start LM Studio and ensure the model is loaded"
                    )
                elif component_name == "Discord Token":
                    recommendations.append("Check your Discord token in the .env file")
                elif component_name == "File Structure":
                    recommendations.append(
                        "Run the main setup to create missing directories"
                    )
                elif component_name == "Plugins":
                    recommendations.append("Check plugin files for syntax errors")

            elif result["status"] == "warning":
                if component_name == "LM Studio Connection":
                    recommendations.append(
                        "Consider loading the correct model in LM Studio"
                    )
                elif component_name == "File Structure":
                    recommendations.append(
                        "Some optional paths are missing but not critical"
                    )
                elif component_name == "Plugins":
                    recommendations.append(
                        "Some plugins have issues but core functionality should work"
                    )

        self.health_report["recommendations"] = recommendations

    def save_report(self, filename: str = "scripts/utils/health_report.json"):
        """Save health report to file"""
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, "w") as f:
            json.dump(self.health_report, f, indent=2)

        print(f"\n📄 Health report saved to: {filename}")

    def print_summary(self):
        """Print health check summary"""
        print("\n" + "=" * 50)
        print("📊 HEALTH CHECK SUMMARY")
        print("=" * 50)

        status_icon = {"healthy": "✅", "warning": "⚠️", "error": "❌"}.get(
            self.health_report["overall_status"], "❓"
        )

        print(
            f"Overall Status: {status_icon} {self.health_report['overall_status'].upper()}"
        )

        if self.health_report["recommendations"]:
            print("\n💡 RECOMMENDATIONS:")
            for i, rec in enumerate(self.health_report["recommendations"], 1):
                print(f"  {i}. {rec}")

        if self.health_report["overall_status"] == "healthy":
            print("\n🎉 System is healthy and ready to use!")
        elif self.health_report["overall_status"] == "warning":
            print("\n⚠️  System has some issues but should work with limitations.")
        else:
            print("\n❌ System has critical issues that need to be resolved.")


def main():
    """Main health checker"""
    checker = SystemHealthChecker()
    report = checker.run_health_check()
    checker.save_report()
    checker.print_summary()

    return 0 if report["overall_status"] in ["healthy", "warning"] else 1


if __name__ == "__main__":
    sys.exit(main())
