import cohere
from typing import Dict, Any
from utils import load_api_key, clean_text
from utils import clean_text, validate_file_path
class GrammarCorrector:
    """
    Grammar correction class using Cohere API for advanced language processing.
    """
    
    def __init__(self):
        """Initialize the grammar corrector with Cohere API client."""
        self.api_key = load_api_key()
        self.client = cohere.Client(self.api_key)
    
    def correct_grammar(self, text: str) -> str:
        """
        Correct grammar in the provided text using Cohere API.
        
        Args:
            text (str): Input text to be corrected
            
        Returns:
            str: Grammar-corrected text
            
        Raises:
            Exception: If API call fails or returns invalid response
        """
        if not text or not text.strip():
            return text
        
        cleaned_text = clean_text(text)
        
        try:
            prompt = f"""Please correct the grammar and improve the clarity of the following text. 
Only return the corrected version without any explanations or additional text:

Text to correct: "{cleaned_text}"

Corrected text:"""

            response = self.client.chat(
                message=prompt,
                max_tokens=150,
                temperature=0.2
            )
            
            corrected_text = response.text.strip()
            
            # Remove quotes if they were added by the model
            if corrected_text.startswith('"') and corrected_text.endswith('"'):
                corrected_text = corrected_text[1:-1]
            
            return corrected_text if corrected_text else cleaned_text
            
        except Exception as e:
            raise Exception(f"Grammar correction failed: {str(e)}")
    
    def analyze_grammar_errors(self, original: str, corrected: str) -> Dict[str, Any]:
        """
        Analyze the differences between original and corrected text.
        
        Args:
            original (str): Original text
            corrected (str): Corrected text
            
        Returns:
            Dict[str, Any]: Analysis of grammar errors and corrections
        """
        try:
            if original.strip() == corrected.strip():
                return {
                    "has_errors": False,
                    "error_count": 0,
                    "analysis": "No grammar errors detected.",
                    "improvements": []
                }
            
            prompt = f"""Analyze the grammar corrections made between these two texts and provide a brief explanation of the main errors that were fixed:

Original: "{original}"
Corrected: "{corrected}"

Please provide:
1. The main types of errors that were corrected
2. Brief explanation of why the corrections were made
3. Keep the response concise and educational

Analysis:"""

            response = self.client.chat(
                message=prompt,
                max_tokens=200,
                temperature=0.3
            )
            
            analysis = response.text.strip()
            
            return {
                "has_errors": True,
                "error_count": len([c for c in original if c != corrected[original.index(c)] if original.index(c) < len(corrected)]),
                "analysis": analysis,
                "improvements": self._extract_improvements(original, corrected)
            }
            
        except Exception as e:
            return {
                "has_errors": True,
                "error_count": 1,
                "analysis": f"Grammar analysis failed: {str(e)}",
                "improvements": ["Manual review recommended"]
            }
    
    def _extract_improvements(self, original: str, corrected: str) -> list:
        """
        Extract specific improvements made to the text.
        
        Args:
            original (str): Original text
            corrected (str): Corrected text
            
        Returns:
            list: List of improvements made
        """
        improvements = []
        
        # Simple word-level comparison
        original_words = original.split()
        corrected_words = corrected.split()
        
        if len(original_words) != len(corrected_words):
            improvements.append("Sentence structure improved")
        
        # Check for common improvements
        if original.lower() != corrected.lower():
            improvements.append("Grammar and clarity enhanced")
        
        if original.count(',') != corrected.count(','):
            improvements.append("Punctuation corrected")
        
        return improvements if improvements else ["Text refined for better clarity"]

def correct_grammar(text: str) -> str:
    """
    Convenience function to correct grammar in text.
    
    Args:
        text (str): Input text to be corrected
        
    Returns:
        str: Grammar-corrected text
    """
    corrector = GrammarCorrector()
    return corrector.correct_grammar(text)

def analyze_text(text: str) -> Dict[str, Any]:
    """
    Convenience function to analyze and correct text.
    
    Args:
        text (str): Input text to analyze
        
    Returns:
        Dict[str, Any]: Complete analysis including original, corrected, and error analysis
    """
    corrector = GrammarCorrector()
    corrected = corrector.correct_grammar(text)
    analysis = corrector.analyze_grammar_errors(text, corrected)
    
    return {
        "original": text,
        "corrected": corrected,
        "analysis": analysis
    }
