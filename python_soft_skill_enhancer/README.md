# Python Soft Skill Enhancer

A comprehensive Python application designed to enhance soft skills through pronunciation detection, grammar correction, and interactive tutoring capabilities.

## Features

- **Grammar Correction**: AI-powered grammar checking and correction using Cohere API
- **Speech Analysis**: Pronunciation detection and analysis from audio files
- **Interactive Tutoring**: Personalized feedback and learning guidance
- **Real-time Feedback**: Instant corrections and suggestions
- **Progress Tracking**: Monitor your improvement over time

## Installation

### Prerequisites

- Python 3.7 or higher
- A Cohere API key (sign up at [cohere.ai](https://cohere.ai))

### Setup Instructions

1. **Clone or download the project**
   ```bash
   cd python_app
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

> Note on audio/recording dependencies
>
> - The live recording features depend on `sounddevice`, `soundfile`, and `numpy` (included in `requirements.txt`).
> - On Windows, if you see import errors for `sounddevice` or `soundfile`, try:
>   ```powershell
>   pip install sounddevice soundfile numpy
>   ```
>   If that fails due to native build requirements, install the Microsoft Visual C++ Build Tools or use `pipwin`:
>   ```powershell
>   pip install pipwin
>   pipwin install pyaudio
>   ```
> - On Linux/macOS, you may need PortAudio/libsndfile installed system-wide. Example on Debian/Ubuntu:
>   ```bash
>   sudo apt-get install libsndfile1 portaudio19-dev
>   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```bash
   echo "COHERE_API_KEY=your_api_key_here" > .env
   ```
   
   Or set the environment variable directly:
   ```bash
   export COHERE_API_KEY=your_api_key_here
   ```

## Usage

### Running the Application

```bash
python main.py
```

### Available Options

1. **Grammar Correction & Tutoring**
   - Enter any text to get grammar corrections
   - Receive detailed feedback on improvements
   - Learn from personalized tutoring suggestions

2. **Speech Analysis**
   - Upload audio files for pronunciation analysis
   - Get transcription and pronunciation feedback
   - Supported formats: WAV, FLAC, AIFF

3. **Interactive Menu**
   - Easy-to-use command-line interface
   - Color-coded feedback and results
   - Error handling with helpful messages

### Example Usage

```bash
$ python main.py

Select an option:
1. Grammar Correction and Tutoring
2. Speech Analysis for Mispronunciation Detection
3. Exit

Enter your choice (1-3): 1
Enter a sentence for grammar checking: I are going to the store

Corrected Sentence: I am going to the store
Feedback: Notice the subject-verb agreement correction. "I" requires "am" not "are".
```

## Project Structure

```
python_app/
├── README.md
├── requirements.txt
├── main.py
└── soft_skill_enhancer/
    ├── __init__.py
    ├── grammar.py      # Grammar correction functionality
    ├── speech.py       # Speech analysis and recognition
    ├── tutor.py        # Tutoring and feedback system
    └── utils.py        # Utility functions
```

## API Integration

This project uses the Cohere API for advanced natural language processing capabilities:

- **Grammar Correction**: Leverages Cohere's language models for accurate grammar checking
- **Tutoring Feedback**: Generates personalized learning suggestions
- **Error Analysis**: Provides detailed explanations of corrections

## Troubleshooting

### Common Issues

1. **Missing API Key**
   ```
   Error: COHERE_API_KEY is not set in environment variables.
   ```
   Solution: Ensure your API key is properly set in the environment or .env file

2. **Audio File Issues**
   ```
   Error: Speech recognition error: [Errno 2] No such file or directory
   ```
   Solution: Check that the audio file path is correct and the file exists

3. **Dependency Issues**
   ```
   ModuleNotFoundError: No module named 'cohere'
   ```
   Solution: Run `pip install -r requirements.txt` in your virtual environment

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
- Check the troubleshooting section above
- Review the error messages for specific guidance
- Ensure all dependencies are properly installed
