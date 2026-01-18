#!/usr/bin/env python3
"""
Python Soft Skill Enhancer - Main Application

Author: Somnath Sarkar (24nemesis06)
Version: 1.0.0
"""

import sys
import os
from colorama import init, Fore, Back, Style

# ✅ Proper package imports (works for both direct & -m runs)
import grammar, speech, speech_live, tutor, utils

# Initialize colorama
init(autoreset=True)


class SoftSkillEnhancerApp:
    """Main application class for the Soft Skill Enhancer."""

    def __init__(self):
        self.session_data = []
        self.running = True

    def display_banner(self):
        banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║           🎯 PYTHON SOFT SKILL ENHANCER 🎯                  ║
║                                                              ║
║     Enhance your communication skills with AI-powered       ║
║     grammar correction, speech analysis, and tutoring       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
        """
        print(banner)

    def display_main_menu(self):
        menu = f"""
{Fore.WHITE}{Back.BLUE} MAIN MENU {Style.RESET_ALL}

{Fore.GREEN}1.{Style.RESET_ALL} 📝 Grammar Correction & Analysis
{Fore.GREEN}2.{Style.RESET_ALL} 🎤 Speech Analysis & Pronunciation Check
{Fore.GREEN}3.{Style.RESET_ALL} 🎓 Interactive Tutoring & Lessons
{Fore.GREEN}4.{Style.RESET_ALL} 📊 Progress Assessment
{Fore.GREEN}5.{Style.RESET_ALL} ❓ Help & Information
{Fore.GREEN}6.{Style.RESET_ALL} 🚪 Exit

{Fore.YELLOW}Enter your choice (1-6):{Style.RESET_ALL} """
        return input(menu).strip()

    # === Grammar Menu ===
    def grammar_correction_menu(self):
        print(f"\n{Fore.WHITE}{Back.GREEN} GRAMMAR CORRECTION & ANALYSIS {Style.RESET_ALL}\n")

        while True:
            print(f"{Fore.CYAN}Options:{Style.RESET_ALL}")
            print("1. Correct a sentence")
            print("2. Analyze text in detail")
            print("3. Back to main menu")

            choice = input(f"\n{Fore.YELLOW}Choose an option (1-3):{Style.RESET_ALL} ").strip()

            if choice == "1":
                self.correct_sentence()
            elif choice == "2":
                self.analyze_text_detailed()
            elif choice == "3":
                break
            else:
                print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")

    def correct_sentence(self):
        print(f"\n{Fore.CYAN}Enter a sentence for grammar correction:{Style.RESET_ALL}")
        text = input("➤ ").strip()
        if not text:
            print(f"{Fore.RED}Please enter some text.{Style.RESET_ALL}")
            return

        try:
            print(f"\n{Fore.YELLOW}Processing...{Style.RESET_ALL}")
            corrected = grammar.correct_grammar(text)
            feedback = tutor.provide_feedback(text, corrected)

            print(f"\n{Fore.WHITE}{Back.BLUE} RESULTS {Style.RESET_ALL}")
            print(f"{Fore.CYAN}Original:{Style.RESET_ALL} {text}")
            print(f"{Fore.GREEN}Corrected:{Style.RESET_ALL} {corrected}")
            print(f"\n{Fore.MAGENTA}Feedback:{Style.RESET_ALL}")
            print(feedback)

            self.session_data.append({
                'type': 'grammar',
                'original': text,
                'corrected': corrected,
                'feedback': feedback
            })

        except Exception as e:
            print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")

        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

    def analyze_text_detailed(self):
        print(f"\n{Fore.CYAN}Enter text for detailed analysis:{Style.RESET_ALL}")
        text = input("➤ ").strip()
        if not text:
            print(f"{Fore.RED}Please enter some text.{Style.RESET_ALL}")
            return

        try:
            print(f"\n{Fore.YELLOW}Analyzing...{Style.RESET_ALL}")
            analysis = grammar.analyze_text(text)

            print(f"\n{Fore.WHITE}{Back.BLUE} DETAILED ANALYSIS {Style.RESET_ALL}")
            print(f"{Fore.CYAN}Original:{Style.RESET_ALL} {analysis['original']}")
            print(f"{Fore.GREEN}Corrected:{Style.RESET_ALL} {analysis['corrected']}")

            err = analysis['analysis']
            print(f"\n{Fore.MAGENTA}Analysis:{Style.RESET_ALL}")
            print(f"Has Errors: {err['has_errors']}")
            print(f"Error Count: {err['error_count']}")
            print(f"Details: {err['analysis']}")
            if err['improvements']:
                print(f"\n{Fore.CYAN}Improvements Made:{Style.RESET_ALL}")
                for imp in err['improvements']:
                    print(f"  • {imp}")

        except Exception as e:
            print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")

        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

    # === Speech Menu ===
    def speech_analysis_menu(self):
        print(f"\n{Fore.WHITE}{Back.GREEN} SPEECH ANALYSIS & PRONUNCIATION {Style.RESET_ALL}\n")

        while True:
            print(f"{Fore.CYAN}Options:{Style.RESET_ALL}")
            print("1. Transcribe audio file")
            print("2. Analyze pronunciation")
            print("3. Record & Analyze Live Speech")
            print("4. View supported formats")
            print("5. Back to main menu")

            choice = input(f"\n{Fore.YELLOW}Choose an option (1-5):{Style.RESET_ALL} ").strip()

            if choice == "1":
                self.transcribe_audio()
            elif choice == "2":
                self.analyze_pronunciation()
            elif choice == "3":
                self.record_and_analyze_live_speech()
            elif choice == "4":
                self.show_supported_formats()
            elif choice == "5":
                break
            else:
                print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")

    def transcribe_audio(self):
        print(f"\n{Fore.CYAN}Enter path to audio file:{Style.RESET_ALL}")
        path = input("➤ ").strip()
        if not path:
            print(f"{Fore.RED}Please enter a file path.{Style.RESET_ALL}")
            return

        try:
            print(f"\n{Fore.YELLOW}Transcribing...{Style.RESET_ALL}")
            text = speech.analyze_speech(path)
            print(f"\n{Fore.GREEN}Transcription:{Style.RESET_ALL} {text}")
        except Exception as e:
            print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

    def analyze_pronunciation(self):
        print(f"\n{Fore.CYAN}Enter path to audio file:{Style.RESET_ALL}")
        path = input("➤ ").strip()
        if not path:
            print(f"{Fore.RED}Please enter a file path.{Style.RESET_ALL}")
            return
        expected = input(f"{Fore.CYAN}Expected text (optional):{Style.RESET_ALL} ").strip() or None

        try:
            print(f"\n{Fore.YELLOW}Analyzing pronunciation...{Style.RESET_ALL}")
            result = speech.analyze_pronunciation(path, expected)
            print(f"\n{Fore.WHITE}{Back.BLUE} RESULT {Style.RESET_ALL}")
            print(result)
        except Exception as e:
            print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

    def record_and_analyze_live_speech(self):
        print(f"\n{Fore.CYAN}🎙 Get ready to record your speech!{Style.RESET_ALL}")
        try:
            duration = input(f"{Fore.YELLOW}Enter duration in seconds (default 5): {Style.RESET_ALL}").strip()
            duration = int(duration) if duration else 5
            result = speech_live.analyze_live_speech(duration)

            # `analyze_live_speech` now returns a dict with original, corrected, and feedback
            if isinstance(result, dict):
                original = result.get('original', '')
                corrected = result.get('corrected', original)
                feedback = result.get('feedback', '')

                print(f"\n{Fore.GREEN}✅ Original transcription:{Style.RESET_ALL} {original}")
                print(f"{Fore.GREEN}✅ Corrected:{Style.RESET_ALL} {corrected}")
                print(f"\n{Fore.MAGENTA}Feedback:{Style.RESET_ALL}\n{feedback}")

                # Save to session data for progress tracking
                self.session_data.append({
                    'type': 'live_speech',
                    'original': original,
                    'corrected': corrected,
                    'feedback': feedback,
                    'audio_path': result.get('audio_path')
                })
            else:
                # Fallback: older behavior where a plain string was returned
                print(f"\n{Fore.GREEN}✅ You said:{Style.RESET_ALL} {result}")
        except Exception as e:
            print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

    def show_supported_formats(self):
        analyzer = speech.SpeechAnalyzer()
        print(f"\n{Fore.WHITE}{Back.BLUE} SUPPORTED AUDIO FORMATS {Style.RESET_ALL}")
        for fmt in analyzer.get_supported_formats():
            print(f"• {fmt}")
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

    # === Tutoring Menu ===
    def tutoring_menu(self):
        print(f"\n{Fore.WHITE}{Back.GREEN} INTERACTIVE TUTORING & LESSONS {Style.RESET_ALL}\n")
        while True:
            print(f"{Fore.CYAN}Options:{Style.RESET_ALL}")
            print("1. Generate a lesson")
            print("2. Show learning topics")
            print("3. Back to main menu")
            choice = input(f"\n{Fore.YELLOW}Choose an option (1-3):{Style.RESET_ALL} ").strip()
            if choice == "1":
                self.generate_lesson()
            elif choice == "2":
                self.show_learning_topics()
            elif choice == "3":
                break
            else:
                print(f"{Fore.RED}Invalid choice. Try again.{Style.RESET_ALL}")

    def generate_lesson(self):
        topic = input(f"{Fore.YELLOW}Enter topic:{Style.RESET_ALL} ").strip()
        difficulty = input(f"{Fore.YELLOW}Enter difficulty (beginner/intermediate/advanced):{Style.RESET_ALL} ").strip() or "beginner"
        try:
            print(f"\n{Fore.YELLOW}Generating lesson...{Style.RESET_ALL}")
            lesson = tutor.generate_lesson(topic, difficulty)
            print(f"\n{Fore.WHITE}{Back.BLUE} LESSON {Style.RESET_ALL}")
            # Use pretty-printer if available
            try:
                if hasattr(tutor, 'print_lesson'):
                    tutor.print_lesson(lesson)
                else:
                    print(lesson)
            except Exception:
                # Fallback to raw print if formatting fails
                print(lesson)
        except Exception as e:
            print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

    def show_learning_topics(self):
        topics = ["grammar", "pronunciation", "communication", "presentation", "writing", "vocabulary", "conversation"]
        print(f"\n{Fore.WHITE}{Back.BLUE} AVAILABLE TOPICS {Style.RESET_ALL}")
        for t in topics:
            print(f"• {t.title()}")
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

    # === Progress & Help ===
    def progress_assessment(self):
        if not self.session_data:
            print(f"{Fore.YELLOW}No progress data yet.{Style.RESET_ALL}")
            input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")
            return
        try:
            print(f"\n{Fore.YELLOW}Assessing progress...{Style.RESET_ALL}")
            report = tutor.SoftSkillTutor().assess_progress(self.session_data)
            print(report)
        except Exception as e:
            print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

    def show_help(self):
        print(f"""
{Fore.WHITE}{Back.BLUE} HELP & INFORMATION {Style.RESET_ALL}

Use this app to enhance grammar, pronunciation, and communication.
Ensure .env has your Cohere API key before running.
        """)
        input(f"\n{Fore.YELLOW}Press Enter to continue...{Style.RESET_ALL}")

    def run(self):
        try:
            utils.load_api_key()
            self.display_banner()
            print(f"{Fore.GREEN}✅ API Key Loaded Successfully!{Style.RESET_ALL}")

            while self.running:
                choice = self.display_main_menu()
                if choice == "1":
                    self.grammar_correction_menu()
                elif choice == "2":
                    self.speech_analysis_menu()
                elif choice == "3":
                    self.tutoring_menu()
                elif choice == "4":
                    self.progress_assessment()
                elif choice == "5":
                    self.show_help()
                elif choice == "6":
                    print(f"\n{Fore.CYAN}Goodbye! Keep improving! 🚀{Style.RESET_ALL}")
                    self.running = False
                else:
                    print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Initialization error: {e}{Style.RESET_ALL}")
            sys.exit(1)


def main():
    """Entry point."""
    app = SoftSkillEnhancerApp()
    app.run()


if __name__ == "__main__":
    main()
