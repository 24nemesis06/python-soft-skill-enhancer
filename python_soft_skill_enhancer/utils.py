import os
from dotenv import load_dotenv

def load_api_key() -> str:
    """
    Load the Cohere API key from environment variables.
    
    Returns:
        str: The API key
        
    Raises:
        ValueError: If the API key is not found
    """
    # Load environment variables from .env file if it exists
    load_dotenv()
    
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError(
            "COHERE_API_KEY is not set in environment variables.\n"
            "Please set it using: export COHERE_API_KEY=your_api_key_here\n"
            "Or create a .env file with: COHERE_API_KEY=your_api_key_here"
        )
    return api_key

def validate_file_path(file_path: str) -> bool:
    """
    Validate if a file path exists and is accessible.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        bool: True if file exists and is accessible
    """
    return os.path.exists(file_path) and os.path.isfile(file_path)

def format_text_output(text: str, color_code: str = "") -> str:
    """
    Format text output with optional color coding.
    
    Args:
        text (str): Text to format
        color_code (str): ANSI color code
        
    Returns:
        str: Formatted text
    """
    if color_code:
        return f"{color_code}{text}\033[0m"
    return text

def clean_text(text: str) -> str:
    """
    Clean and normalize input text.
    
    Args:
        text (str): Input text
        
    Returns:
        str: Cleaned text
    """
    return text.strip().replace('\n', ' ').replace('\r', '')
