import speech_recognition as sr
import os
from typing import Dict, Any, Optional

from utils import clean_text, validate_file_path

class SpeechAnalyzer:
    """
    Speech analysis class for pronunciation detection and audio transcription.
    """
    
    def __init__(self):
        """Initialize the speech analyzer with recognizer."""
        self.recognizer = sr.Recognizer()
        # Adjust for ambient noise
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
    
    def analyze_speech(self, audio_path: str) -> str:
        """
        Analyze speech from an audio file and return transcription.
        
        Args:
            audio_path (str): Path to the audio file
            
        Returns:
            str: Transcribed text from the audio
            
        Raises:
            Exception: If file doesn't exist or speech recognition fails
        """
        if not validate_file_path(audio_path):
            raise Exception(f"Audio file not found: {audio_path}")
        
        try:
            with sr.AudioFile(audio_path) as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                # Record the audio data
                audio_data = self.recognizer.record(source)
            
            # Use Google Speech Recognition
            transcription = self.recognizer.recognize_google(audio_data)
            return clean_text(transcription)
            
        except sr.UnknownValueError:
            raise Exception("Could not understand the audio. Please ensure clear speech and good audio quality.")
        except sr.RequestError as e:
            raise Exception(f"Speech recognition service error: {str(e)}")
        except Exception as e:
            raise Exception(f"Speech analysis failed: {str(e)}")
    
    def analyze_pronunciation(self, audio_path: str, expected_text: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze pronunciation by comparing transcribed text with expected text.
        
        Args:
            audio_path (str): Path to the audio file
            expected_text (str, optional): Expected text for comparison
            
        Returns:
            Dict[str, Any]: Pronunciation analysis results
        """
        try:
            transcribed = self.analyze_speech(audio_path)
            
            if not expected_text:
                return {
                    "transcribed_text": transcribed,
                    "expected_text": None,
                    "pronunciation_score": None,
                    "analysis": "Transcription completed. Provide expected text for pronunciation analysis.",
                    "suggestions": ["Record again with clearer pronunciation", "Speak at a moderate pace"]
                }
            
            expected_clean = clean_text(expected_text.lower())
            transcribed_clean = transcribed.lower()
            
            # Simple similarity calculation
            similarity_score = self._calculate_similarity(expected_clean, transcribed_clean)
            
            return {
                "transcribed_text": transcribed,
                "expected_text": expected_text,
                "pronunciation_score": similarity_score,
                "analysis": self._generate_pronunciation_feedback(expected_clean, transcribed_clean, similarity_score),
                "suggestions": self._generate_pronunciation_suggestions(similarity_score)
            }
            
        except Exception as e:
            return {
                "transcribed_text": "",
                "expected_text": expected_text,
                "pronunciation_score": 0,
                "analysis": f"Analysis failed: {str(e)}",
                "suggestions": ["Check audio file format and quality", "Ensure clear speech"]
            }
    
    def _calculate_similarity(self, expected: str, transcribed: str) -> float:
        """
        Calculate similarity between expected and transcribed text.
        
        Args:
            expected (str): Expected text
            transcribed (str): Transcribed text
            
        Returns:
            float: Similarity score (0-100)
        """
        if not expected or not transcribed:
            return 0.0
        
        expected_words = expected.split()
        transcribed_words = transcribed.split()
        
        if not expected_words:
            return 0.0
        
        # Simple word-level matching
        matches = 0
        for word in expected_words:
            if word in transcribed_words:
                matches += 1
        
        similarity = (matches / len(expected_words)) * 100
        return round(similarity, 2)
    
    def _generate_pronunciation_feedback(self, expected: str, transcribed: str, score: float) -> str:
        """
        Generate feedback based on pronunciation analysis.
        
        Args:
            expected (str): Expected text
            transcribed (str): Transcribed text
            score (float): Similarity score
            
        Returns:
            str: Feedback message
        """
        if score >= 90:
            return "Excellent pronunciation! Your speech is very clear and accurate."
        elif score >= 75:
            return "Good pronunciation! Minor improvements could enhance clarity."
        elif score >= 50:
            return "Fair pronunciation. Focus on clearer articulation of words."
        else:
            return "Pronunciation needs improvement. Practice speaking slowly and clearly."
    
    def _generate_pronunciation_suggestions(self, score: float) -> list:
        """
        Generate suggestions based on pronunciation score.
        
        Args:
            score (float): Pronunciation score
            
        Returns:
            list: List of suggestions
        """
        if score >= 90:
            return ["Keep up the excellent work!", "Try more challenging texts"]
        elif score >= 75:
            return ["Focus on word endings", "Practice with tongue twisters"]
        elif score >= 50:
            return ["Speak more slowly", "Practice individual word pronunciation", "Record in a quiet environment"]
        else:
            return [
                "Practice basic pronunciation exercises",
                "Speak more slowly and clearly",
                "Focus on vowel sounds",
                "Use a mirror to watch mouth movements"
            ]
    
    def get_supported_formats(self) -> list:
        """
        Get list of supported audio formats.
        
        Returns:
            list: Supported audio file formats
        """
        return ['.wav', '.flac', '.aiff']
    
    def validate_audio_format(self, audio_path: str) -> bool:
        """
        Validate if the audio file format is supported.
        
        Args:
            audio_path (str): Path to audio file
            
        Returns:
            bool: True if format is supported
        """
        if not validate_file_path(audio_path):
            return False
        
        file_extension = os.path.splitext(audio_path)[1].lower()
        return file_extension in self.get_supported_formats()

def analyze_speech(audio_path: str) -> str:
    """
    Convenience function to analyze speech from audio file.
    
    Args:
        audio_path (str): Path to audio file
        
    Returns:
        str: Transcribed text
    """
    analyzer = SpeechAnalyzer()
    return analyzer.analyze_speech(audio_path)

def analyze_pronunciation(audio_path: str, expected_text: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function to analyze pronunciation.
    
    Args:
        audio_path (str): Path to audio file
        expected_text (str, optional): Expected text for comparison
        
    Returns:
        Dict[str, Any]: Pronunciation analysis results
    """
    analyzer = SpeechAnalyzer()
    return analyzer.analyze_pronunciation(audio_path, expected_text)
