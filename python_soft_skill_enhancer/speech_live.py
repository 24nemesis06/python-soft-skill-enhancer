"""Live recording helpers.

This module depends on third-party audio libraries (`sounddevice`, `soundfile`, `numpy`).
If they are not available, we provide a clear error message explaining how to install them.
"""

import tempfile
import time
from speech import SpeechAnalyzer
from utils import clean_text, validate_file_path
import grammar
import tutor

SOUND_MODULE_IMPORT_ERROR = None
sd = None
sf = None
try:
    import numpy as np
    import sounddevice as sd
    import soundfile as sf
except Exception as e:
    # Capture import-time error so the app can continue to run other features.
    SOUND_MODULE_IMPORT_ERROR = e


def _raise_missing_audio_lib():
    msg = (
        "Live recording requires additional audio packages which are not installed or failed to import.\n"
        "Please install them by running:\n\n"
        "    pip install -r requirements.txt\n\n"
        "If installation fails on Windows, you may need to install build tools or try:\n"
        "    pip install sounddevice soundfile numpy\n"
        "or use pipwin for PyAudio alternatives:\n"
        "    pip install pipwin; pipwin install pyaudio\n\n"
        "Original import error: {}"
    ).format(SOUND_MODULE_IMPORT_ERROR)
    raise RuntimeError(msg)


def record_audio(duration: int = 5, samplerate: int = 44100) -> str:
    """Record live audio from mic and save to a temporary WAV file.

    Raises a RuntimeError with actionable instructions if the audio libraries are missing.
    """
    if sd is None or sf is None:
        _raise_missing_audio_lib()

    print(f"\n🎙 Recording for {duration} seconds... Speak now!\n")
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='float32')
    sd.wait()
    print("✅ Recording complete.\n")

    temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    # Ensure data is in the shape (frames, channels) and write the WAV
    sf.write(temp_file.name, audio_data, samplerate)
    return temp_file.name


def analyze_live_speech(duration: int = 5):
    """Record live mic audio and analyze speech."""
    if sd is None or sf is None:
        _raise_missing_audio_lib()

    analyzer = SpeechAnalyzer()
    audio_path = record_audio(duration)
    print("🎧 Transcribing speech...")
    transcription = analyzer.analyze_speech(audio_path)
    print(f"\n🗣 Transcribed Text: {transcription}")

    # Pass the raw transcription through grammar correction to improve clarity/order
    try:
        corrected = grammar.correct_grammar(transcription)
    except Exception:
        # If grammar correction fails, fall back to raw transcription
        corrected = transcription

    # Provide tutor feedback for the correction (local or via API)
    try:
        feedback = tutor.provide_feedback(transcription, corrected)
    except Exception:
        feedback = "Feedback not available."

    # Return structured result so callers can display both original and corrected text
    return {
        "original": transcription,
        "corrected": corrected,
        "feedback": feedback,
        "audio_path": audio_path,
    }
