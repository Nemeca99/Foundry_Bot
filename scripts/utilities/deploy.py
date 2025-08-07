#!/usr/bin/env python3
"""
Deployment Script for Authoring Bot
Handles complete setup and deployment process
"""

import sys
import os
import subprocess
import json
from pathlib import Path
from datetime import datetime

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class BotDeployer:
    """Complete deployment system for the Authoring Bot"""

    def __init__(self):
        self.deployment_log = []
        self.errors = []

    def log(self, message: str, level: str = "INFO"):
        """Log deployment message"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        self.deployment_log.append(log_entry)
        print(log_entry)

    def run_command(self, command: str, description: str) -> bool:
        """Run a command and log the result"""
        self.log(f"Running: {description}")

        try:
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, timeout=300
            )

            if result.returncode == 0:
                self.log(f"✅ {description} completed successfully")
                if result.stdout.strip():
                    self.log(f"Output: {result.stdout.strip()}")
                return True
            else:
                self.log(f"❌ {description} failed", "ERROR")
                self.log(f"Error: {result.stderr.strip()}", "ERROR")
                self.errors.append(f"{description}: {result.stderr.strip()}")
                return False

        except subprocess.TimeoutExpired:
            self.log(f"❌ {description} timed out", "ERROR")
            self.errors.append(f"{description}: Timeout")
            return False
        except Exception as e:
            self.log(f"❌ {description} failed with exception: {e}", "ERROR")
            self.errors.append(f"{description}: {e}")
            return False

    def check_prerequisites(self) -> bool:
        """Check if all prerequisites are met"""
        self.log("🔍 Checking prerequisites...")

        # Check Python version
        python_version = sys.version_info
        if python_version.major < 3 or (
            python_version.major == 3 and python_version.minor < 8
        ):
            self.log("❌ Python 3.8+ is required", "ERROR")
            return False

        self.log(
            f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}"
        )

        # Check if virtual environment exists
        venv_path = Path(".venv")
        if not venv_path.exists():
            self.log("⚠️  Virtual environment not found, will create one")
        else:
            self.log("✅ Virtual environment exists")

        # Check if .env file exists
        env_path = Path(".env")
        if not env_path.exists():
            self.log("⚠️  .env file not found, will run setup")
        else:
            self.log("✅ .env file exists")

        return True

    def setup_virtual_environment(self) -> bool:
        """Set up Python virtual environment"""
        self.log("🐍 Setting up virtual environment...")

        # Create virtual environment if it doesn't exist
        venv_path = Path(".venv")
        if not venv_path.exists():
            success = self.run_command(
                f"{sys.executable} -m venv .venv", "Creating virtual environment"
            )
            if not success:
                return False

        # Activate virtual environment and install requirements
        if os.name == "nt":  # Windows
            activate_cmd = ".venv\\Scripts\\activate"
            pip_cmd = ".venv\\Scripts\\pip"
        else:  # Unix/Linux
            activate_cmd = "source .venv/bin/activate"
            pip_cmd = ".venv/bin/pip"

        # Install requirements
        success = self.run_command(
            f"{pip_cmd} install -r requirements.txt", "Installing Python dependencies"
        )

        return success

    def run_setup(self) -> bool:
        """Run the bot setup process"""
        self.log("🔧 Running bot setup...")

        # Check if setup script exists
        setup_script = "scripts/setup/setup_bot.py"
        if not os.path.exists(setup_script):
            self.log(f"❌ Setup script not found: {setup_script}", "ERROR")
            return False

        # Run setup (this will be interactive)
        self.log("📝 Running interactive setup...")
        self.log("Please follow the prompts to configure your bot")

        try:
            result = subprocess.run(
                [sys.executable, setup_script],
                timeout=600,  # 10 minute timeout for setup
            )

            if result.returncode == 0:
                self.log("✅ Setup completed successfully")
                return True
            else:
                self.log("❌ Setup failed", "ERROR")
                return False

        except subprocess.TimeoutExpired:
            self.log("❌ Setup timed out", "ERROR")
            return False
        except Exception as e:
            self.log(f"❌ Setup failed with exception: {e}", "ERROR")
            return False

    def run_health_check(self) -> bool:
        """Run system health check"""
        self.log("🏥 Running health check...")

        health_script = "scripts/utils/system_health.py"
        if not os.path.exists(health_script):
            self.log(f"❌ Health check script not found: {health_script}", "ERROR")
            return False

        try:
            result = subprocess.run(
                [sys.executable, health_script],
                capture_output=True,
                text=True,
                timeout=300,
            )

            if result.returncode == 0:
                self.log("✅ Health check passed")
                return True
            else:
                self.log("❌ Health check failed", "ERROR")
                self.log(f"Health check output: {result.stdout}", "INFO")
                self.log(f"Health check errors: {result.stderr}", "ERROR")
                return False

        except Exception as e:
            self.log(f"❌ Health check failed with exception: {e}", "ERROR")
            return False

    def run_tests(self) -> bool:
        """Run comprehensive test suite"""
        self.log("🧪 Running test suite...")

        test_script = "scripts/tests/run_all_tests.py"
        if not os.path.exists(test_script):
            self.log(f"❌ Test runner not found: {test_script}", "ERROR")
            return False

        try:
            result = subprocess.run(
                [sys.executable, test_script],
                capture_output=True,
                text=True,
                timeout=600,  # 10 minute timeout for tests
            )

            if result.returncode == 0:
                self.log("✅ All tests passed")
                return True
            else:
                self.log("❌ Some tests failed", "ERROR")
                self.log(f"Test output: {result.stdout}", "INFO")
                self.log(f"Test errors: {result.stderr}", "ERROR")
                return False

        except Exception as e:
            self.log(f"❌ Tests failed with exception: {e}", "ERROR")
            return False

    def create_startup_scripts(self) -> bool:
        """Create convenient startup scripts"""
        self.log("📝 Creating startup scripts...")

        # Create Windows batch file
        batch_content = """@echo off
echo Starting Authoring Bot...
cd /d "%~dp0"
call .venv\\Scripts\\activate
python scripts\\start_authoring_bot.py
pause
"""

        with open("start_bot.bat", "w") as f:
            f.write(batch_content)

        # Create PowerShell script
        ps_content = """# Authoring Bot Startup Script
Write-Host "Starting Authoring Bot..." -ForegroundColor Green
Set-Location $PSScriptRoot
.venv\\Scripts\\Activate.ps1
python scripts\\start_authoring_bot.py
"""

        with open("start_bot.ps1", "w") as f:
            f.write(ps_content)

        # Create Linux/Mac shell script
        shell_content = """#!/bin/bash
echo "Starting Authoring Bot..."
cd "$(dirname "$0")"
source .venv/bin/activate
python scripts/start_authoring_bot.py
"""

        with open("start_bot.sh", "w") as f:
            f.write(shell_content)

        # Make shell script executable
        if os.name != "nt":
            os.chmod("start_bot.sh", 0o755)

        self.log("✅ Startup scripts created")
        return True

    def generate_deployment_report(self):
        """Generate deployment report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "deployment_log": self.deployment_log,
            "errors": self.errors,
            "success": len(self.errors) == 0,
        }

        report_file = "scripts/deployment/deployment_report.json"
        os.makedirs(os.path.dirname(report_file), exist_ok=True)

        with open(report_file, "w") as f:
            json.dump(report, f, indent=2)

        self.log(f"📄 Deployment report saved to: {report_file}")

    def deploy(self) -> bool:
        """Run complete deployment process"""
        self.log("🚀 Starting Authoring Bot Deployment")
        self.log("=" * 50)

        steps = [
            ("Checking prerequisites", self.check_prerequisites),
            ("Setting up virtual environment", self.setup_virtual_environment),
            ("Running bot setup", self.run_setup),
            ("Running health check", self.run_health_check),
            ("Running tests", self.run_tests),
            ("Creating startup scripts", self.create_startup_scripts),
        ]

        for step_name, step_func in steps:
            self.log(f"\n📋 Step: {step_name}")
            if not step_func():
                self.log(f"❌ Deployment failed at: {step_name}", "ERROR")
                self.generate_deployment_report()
                return False

        self.log("\n🎉 Deployment completed successfully!")
        self.log("=" * 50)
        self.log("📋 Next Steps:")
        self.log("1. Start LM Studio and load your model")
        self.log("2. Run: python scripts/main.py")
        self.log(
            "3. Or use the startup scripts: start_bot.bat (Windows) or start_bot.sh (Linux/Mac)"
        )

        self.generate_deployment_report()
        return True


def main():
    """Main deployment function"""
    deployer = BotDeployer()
    success = deployer.deploy()

    if success:
        print("\n✅ Deployment successful! Your Authoring Bot is ready to use.")
        return 0
    else:
        print("\n❌ Deployment failed. Check the deployment report for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
