#!/usr/bin/env python3
"""
Setup script for Python Soft Skill Enhancer

This script helps users set up the project environment and dependencies.
"""

import os
import sys
import subprocess
import platform

def print_colored(text, color_code):
    """Print colored text to terminal."""
    print(f"\033[{color_code}m{text}\033[0m")

def print_success(text):
    """Print success message in green."""
    print_colored(f"✅ {text}", "92")

def print_error(text):
    """Print error message in red."""
    print_colored(f"❌ {text}", "91")

def print_info(text):
    """Print info message in blue."""
    print_colored(f"ℹ️  {text}", "94")

def print_warning(text):
    """Print warning message in yellow."""
    print_colored(f"⚠️  {text}", "93")

def check_python_version():
    """Check if Python version is compatible."""
    print_info("Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print_error(f"Python 3.7 or higher is required. Current version: {version.major}.{version.minor}")
        return False
    
    print_success(f"Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def create_virtual_environment():
    """Create a virtual environment for the project."""
    print_info("Creating virtual environment...")
    
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print_success("Virtual environment created successfully")
        return True
    except subprocess.CalledProcessError:
        print_error("Failed to create virtual environment")
        return False

def get_activation_command():
    """Get the command to activate virtual environment based on OS."""
    if platform.system() == "Windows":
        return "venv\\Scripts\\activate"
    else:
        return "source venv/bin/activate"

def install_dependencies():
    """Install project dependencies."""
    print_info("Installing dependencies...")
    
    # Determine pip command based on OS
    if platform.system() == "Windows":
        pip_cmd = "venv\\Scripts\\pip"
    else:
        pip_cmd = "venv/bin/pip"
    
    try:
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
        print_success("Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print_error("Failed to install dependencies")
        print_info("You can try installing manually with: pip install -r requirements.txt")
        return False

def setup_environment_file():
    """Set up the environment file."""
    print_info("Setting up environment file...")
    
    if os.path.exists(".env"):
        print_warning(".env file already exists. Skipping creation.")
        return True
    
    if os.path.exists(".env.example"):
        try:
            # Copy .env.example to .env
            with open(".env.example", "r") as example_file:
                content = example_file.read()
            
            with open(".env", "w") as env_file:
                env_file.write(content)
            
            print_success(".env file created from .env.example")
            print_warning("Please edit .env file and add your Cohere API key!")
            return True
        except Exception as e:
            print_error(f"Failed to create .env file: {str(e)}")
            return False
    else:
        print_error(".env.example file not found")
        return False

def display_next_steps():
    """Display next steps for the user."""
    activation_cmd = get_activation_command()
    
    next_steps = f"""
🎉 Setup completed successfully!

Next steps:
1. Activate the virtual environment:
   {activation_cmd}

2. Set your Cohere API key in the .env file:
   - Open .env file in a text editor
   - Replace 'your_cohere_api_key_here' with your actual API key
   - Get your API key from: https://cohere.ai

3. Run the application:
   python main.py

4. (Optional) Test the installation:
   python -c "from soft_skill_enhancer import utils; print('✅ Installation successful!')"

📚 For more information, read the README.md file.
    """
    
    print_colored(next_steps, "96")

def main():
    """Main setup function."""
    print_colored("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║        🚀 PYTHON SOFT SKILL ENHANCER SETUP 🚀              ║
║                                                              ║
║     This script will help you set up the project            ║
║     environment and install all dependencies.               ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """, "96")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not os.path.exists("venv"):
        if not create_virtual_environment():
            print_error("Setup failed. Please create virtual environment manually.")
            sys.exit(1)
    else:
        print_info("Virtual environment already exists. Skipping creation.")
    
    # Install dependencies
    if not install_dependencies():
        print_error("Setup failed. Please install dependencies manually.")
        sys.exit(1)
    
    # Setup environment file
    setup_environment_file()
    
    # Display next steps
    display_next_steps()

if __name__ == "__main__":
    main()
