import cohere
import re
from typing import Optional, Dict, Any, List
from utils import load_api_key, clean_text


class SoftSkillTutor:
    """
    AI-powered tutoring system for soft skill enhancement.
    """

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the tutor with an optional Cohere API client.

        If no API key is provided or loadable from environment, the tutor
        operates in local fallback mode and returns templated lessons and
        basic feedback without making network calls.
        """
        if api_key is None:
            try:
                api_key = load_api_key()
            except Exception:
                api_key = None

        self.api_key = api_key
        self.client = cohere.Client(self.api_key) if self.api_key else None

        self.learning_areas = [
            "grammar",
            "pronunciation",
            "communication",
            "presentation",
            "writing",
            "vocabulary",
            "conversation",
        ]

    def provide_feedback(self, original_text: str, corrected_text: str) -> str:
        """
        Provide detailed feedback on text corrections and improvements.
        """
        if not original_text or not corrected_text:
            return "Please provide both original and corrected text for feedback."

        original_clean = clean_text(original_text)
        corrected_clean = clean_text(corrected_text)

        if original_clean.lower() == corrected_clean.lower():
            return "Excellent! Your text is grammatically correct and well-structured."

        # If no Cohere client, use a simple local feedback generator
        if not self.client:
            return self._generate_basic_feedback(original_clean, corrected_clean)

        try:
            prompt = f"""As a soft skills tutor, provide constructive feedback on the following text correction. 
Focus on helping the learner understand the improvements and learn from them.

Original text: "{original_clean}"
Corrected text: "{corrected_clean}"

Please provide:
1. What specific improvements were made
2. Why these changes improve the text
3. Learning tips to avoid similar issues in the future
4. Encouragement and positive reinforcement

Keep the feedback encouraging, educational, and actionable:"""

            # Use Cohere Chat API (the older Generate API was removed)
            response = self.client.chat(
                message=prompt,
                max_tokens=250,
                temperature=0.4,
            )

            feedback = getattr(response, "text", "").strip()
            return feedback

        except Exception:
            return self._generate_basic_feedback(original_clean, corrected_clean)

    def generate_lesson(self, topic: str, difficulty_level: str = "beginner") -> Dict[str, Any]:
        """
        Generate a personalized lesson on a specific soft skill topic.
        """
        if topic.lower() not in [area.lower() for area in self.learning_areas]:
            return {
                "topic": topic,
                "error": f"Topic '{topic}' not supported. Available topics: {', '.join(self.learning_areas)}",
            }

        # If no Cohere client, return a local templated lesson
        if not self.client:
            content_parts: List[str] = []
            content_parts.append("Learning Objectives:\n")
            for obj in self._default_objectives(topic, difficulty_level):
                content_parts.append(f"- {obj}")
            content_parts.append("\nKey Concepts:\n")
            for c in self._default_key_concepts(topic):
                content_parts.append(f"- {c}")
            content_parts.append("\nPractical Examples:\n")
            for ex in self._default_examples(topic):
                content_parts.append(f"- {ex}")
            content_parts.append("\nPractice Exercises:\n")
            for ex in self._default_exercises(topic):
                content_parts.append(f"- {ex}")
            content_parts.append("\nTips for Improvement:\n")
            for t in self._get_fallback_tips(topic):
                content_parts.append(f"- {t}")

            lesson_content = "\n".join(content_parts)

            return {
                "topic": topic.title(),
                "difficulty_level": difficulty_level.title(),
                "content": lesson_content,
                "estimated_time": self._estimate_lesson_time(difficulty_level),
                "next_steps": self._suggest_next_steps(topic, difficulty_level),
            }

        try:
            prompt = f"""Create a {difficulty_level} level lesson on {topic} for soft skill enhancement.

Structure the lesson with:
1. Learning Objectives (2-3 clear goals)
2. Key Concepts (main points to understand)
3. Practical Examples (3-4 examples with explanations)
4. Practice Exercises (2-3 exercises the learner can do)
5. Tips for Improvement (actionable advice)

Make it engaging, practical, and suitable for {difficulty_level} learners:"""

            # Use Cohere Chat API
            response = self.client.chat(
                message=prompt,
                max_tokens=400,
                temperature=0.5,
            )

            lesson_content = getattr(response, "text", "").strip()

            return {
                "topic": topic.title(),
                "difficulty_level": difficulty_level.title(),
                "content": lesson_content,
                "estimated_time": self._estimate_lesson_time(difficulty_level),
                "next_steps": self._suggest_next_steps(topic, difficulty_level),
            }

        except Exception as e:
            return {
                "topic": topic,
                "error": f"Failed to generate lesson: {str(e)}",
                "fallback_tips": self._get_fallback_tips(topic),
            }

    def assess_progress(self, user_responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Assess user's learning progress based on their responses and corrections.
        """
        if not user_responses:
            return {
                "progress_score": 0,
                "assessment": "No data available for assessment.",
                "recommendations": ["Start practicing with basic exercises"],
            }

        try:
            # Calculate improvement metrics
            total_sessions = len(user_responses)
            improvements = 0
            common_errors: List[str] = []

            for response in user_responses:
                if response.get("original", "").lower() != response.get("corrected", "").lower():
                    improvements += 1
                    common_errors.extend(self._identify_error_types(response.get("original", ""), response.get("corrected", "")))

            progress_score = max(0, 100 - (improvements / total_sessions * 100)) if total_sessions > 0 else 0

            # If no client, return a simple local assessment
            if not self.client:
                assessment_text = f"Based on {total_sessions} sessions, your progress score is {progress_score:.1f}%."
                return {
                    "progress_score": round(progress_score, 1),
                    "total_sessions": total_sessions,
                    "improvement_sessions": improvements,
                    "assessment": assessment_text,
                    "common_errors": list(set(common_errors)),
                    "recommendations": self._generate_recommendations(progress_score, common_errors),
                }

            prompt = f"""As a soft skills tutor, assess the learning progress based on this data:

Total practice sessions: {total_sessions}
Sessions with corrections needed: {improvements}
Progress score: {progress_score:.1f}%

Provide:
1. Overall progress assessment
2. Strengths identified
3. Areas for improvement
4. Specific recommendations for continued learning
5. Motivational message

Keep the assessment encouraging and constructive:"""

            # Use Cohere Chat API for assessment
            response = self.client.chat(
                message=prompt,
                max_tokens=300,
                temperature=0.4,
            )

            assessment = getattr(response, "text", "").strip()

            return {
                "progress_score": round(progress_score, 1),
                "total_sessions": total_sessions,
                "improvement_sessions": improvements,
                "assessment": assessment,
                "common_errors": list(set(common_errors)),
                "recommendations": self._generate_recommendations(progress_score, common_errors),
            }

        except Exception as e:
            return {
                "progress_score": 0,
                "assessment": f"Assessment failed: {str(e)}",
                "recommendations": ["Continue practicing regularly", "Focus on basic grammar rules"],
            }

    def _generate_basic_feedback(self, original: str, corrected: str) -> str:
        """
        Generate basic feedback when API call fails.
        """
        differences = len([i for i in range(min(len(original), len(corrected))) if original[i] != corrected[i]])

        if differences == 0:
            return "Great job! Your text is well-written."
        elif differences <= 3:
            return "Good work! Minor corrections were made to improve clarity and grammar."
        else:
            return "Keep practicing! Several improvements were made. Focus on grammar rules and sentence structure."

    def _estimate_lesson_time(self, difficulty_level: str) -> str:
        time_map = {
            "beginner": "15-20 minutes",
            "intermediate": "20-30 minutes",
            "advanced": "30-45 minutes",
        }
        return time_map.get(difficulty_level.lower(), "20-30 minutes")

    def _suggest_next_steps(self, topic: str, difficulty_level: str) -> List[str]:
        if difficulty_level.lower() == "beginner":
            return [f"Practice more {topic} exercises", "Move to intermediate level", "Apply skills in daily communication"]
        elif difficulty_level.lower() == "intermediate":
            return [f"Master advanced {topic} concepts", "Combine with other soft skills", "Practice in real-world scenarios"]
        else:
            return [f"Teach {topic} to others", "Apply in professional settings", "Explore specialized applications"]

    def _identify_error_types(self, original: str, corrected: str) -> List[str]:
        errors: List[str] = []
        if original.count(",") != corrected.count(","):
            errors.append("punctuation")
        if len(original.split()) != len(corrected.split()):
            errors.append("word_choice")
        if original.lower() != corrected.lower():
            errors.append("grammar")
        return errors

    def _generate_recommendations(self, progress_score: float, common_errors: List[str]) -> List[str]:
        recommendations: List[str] = []
        if progress_score < 50:
            recommendations.extend([
                "Focus on basic grammar rules",
                "Practice daily with simple exercises",
                "Read more to improve language intuition",
            ])
        elif progress_score < 80:
            recommendations.extend([
                "Work on advanced grammar concepts",
                "Practice writing longer texts",
                "Focus on style and clarity",
            ])
        else:
            recommendations.extend([
                "Maintain your excellent progress",
                "Challenge yourself with complex texts",
                "Help others learn",
            ])

        if "punctuation" in common_errors:
            recommendations.append("Review punctuation rules")
        if "grammar" in common_errors:
            recommendations.append("Study verb tenses and sentence structure")

        return recommendations

    def _get_fallback_tips(self, topic: str) -> List[str]:
        tips_map = {
            "grammar": ["Review basic sentence structure", "Practice verb conjugations", "Study common grammar rules"],
            "pronunciation": ["Practice with audio recordings", "Use phonetic guides", "Record yourself speaking"],
            "communication": ["Practice active listening", "Work on clear expression", "Study body language"],
            "writing": ["Read regularly", "Practice daily writing", "Focus on clarity and structure"],
        }
        return tips_map.get(topic.lower(), ["Practice regularly", "Seek feedback", "Stay consistent"])

    # Local templated content helpers
    def _default_objectives(self, topic: str, difficulty: str) -> List[str]:
        if topic.lower() == "grammar":
            return ["Understand basic sentence structure", "Correct common verb tense errors"]
        return [f"Learn the fundamentals of {topic}", "Practice with examples"]

    def _default_key_concepts(self, topic: str) -> List[str]:
        if topic.lower() == "grammar":
            return ["Subject-verb agreement", "Tense consistency", "Punctuation basics"]
        return [f"Core ideas for {topic}"]

    def _default_examples(self, topic: str) -> List[str]:
        if topic.lower() == "grammar":
            return ["I go -> He goes (subject-verb)", "She was running -> She ran (tense simplification)"]
        return [f"Example usage for {topic}"]

    def _default_exercises(self, topic: str) -> List[str]:
        if topic.lower() == "grammar":
            return ["Correct 5 sentences with tense errors", "Rewrite sentences to improve clarity"]
        return [f"Practice exercise for {topic}"]


def provide_feedback(original_text: str, corrected_text: str) -> str:
    tutor = SoftSkillTutor()
    return tutor.provide_feedback(original_text, corrected_text)


def generate_lesson(topic: str, difficulty_level: str = "beginner") -> Dict[str, Any]:
    tutor = SoftSkillTutor()
    return tutor.generate_lesson(topic, difficulty_level)


def format_lesson_for_user(lesson: Dict[str, Any]) -> str:
    """Return a clean, user-friendly string representation of a lesson dict.

    This helps avoid showing raw dict reprs and makes truncated/merged output
    easier to read. The function is tolerant if fields are missing.
    """
    if not lesson:
        return "(no lesson content)"

    # Header
    parts: list[str] = []
    topic = lesson.get("topic", "Lesson")
    difficulty = lesson.get("difficulty_level") or ""
    header = f"{topic}"
    if difficulty:
        header += f" — {difficulty}"
    parts.append(header)
    parts.append("")

    # Convert basic markdown to readable plain text
    content = lesson.get("content", "")
    if content:
        text = content
        # Headings: convert ### or #### to same line header (remove MD hashes)
        text = re.sub(r"^\s*#{1,6}\s*", "", text, flags=re.MULTILINE)
        # Bold/italic: remove ** or *
        text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
        text = re.sub(r"\*(.*?)\*", r"\1", text)
        # Convert markdown list markers '-' or '*' to '- '
        text = re.sub(r"^\s*[-\*]\s+", "- ", text, flags=re.MULTILINE)
        # Normalize multiple blank lines to max two
        text = re.sub(r"\n{3,}", "\n\n", text)
        parts.append(text.strip())
        parts.append("")

    # Estimated time and next steps
    if lesson.get("estimated_time"):
        parts.append(f"Estimated time: {lesson['estimated_time']}")
    if lesson.get("next_steps"):
        parts.append("")
        parts.append("Next steps:")
        for step in lesson.get("next_steps", []):
            parts.append(f"- {step}")

    # Error / fallback info if present
    if lesson.get("error"):
        parts.append("")
        parts.append(f"Error: {lesson['error']}")
        if lesson.get("fallback_tips"):
            parts.append("Fallback tips:")
            for tip in lesson.get("fallback_tips", []):
                parts.append(f"- {tip}")

    return "\n".join(parts)


def print_lesson(lesson: Dict[str, Any]) -> None:
    """Print the user-friendly lesson to stdout."""
    print(format_lesson_for_user(lesson))
