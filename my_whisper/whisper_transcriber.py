"""Whisper transcription functionality."""

from pathlib import Path
from typing import Any

import whisper


class WhisperTranscriber:
    """Whisper-based audio transcription class."""

    def __init__(self, model: str = "base") -> None:
        """Initialize the transcriber with a Whisper model.

        Args:
            model: Whisper model size ('tiny', 'base', 'small', 'medium', 'large')
        """
        self.model_name = model
        self.model = whisper.load_model(model)

    def transcribe(self, audio_path: str, language: str | None = None) -> dict[str, Any]:
        """Transcribe audio file to text.

        Args:
            audio_path: Path to the audio file
            language: Language code (e.g., 'ja', 'en'). If None, auto-detect.

        Returns:
            Dictionary containing transcription results
        """
        if not Path(audio_path).exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        # Transcribe with optional language specification
        if language:
            result = self.model.transcribe(audio_path, language=language)
        else:
            result = self.model.transcribe(audio_path)

        return {
            "text": result["text"],
            "language": result.get("language", "unknown"),
            "segments": result.get("segments", [])
        }

    def transcribe_with_timestamps(
        self, audio_path: str, language: str | None = None
    ) -> dict[str, Any]:
        """Transcribe audio file with detailed timestamps.

        Args:
            audio_path: Path to the audio file
            language: Language code (e.g., 'ja', 'en'). If None, auto-detect.

        Returns:
            Dictionary containing transcription results with timestamps
        """
        result = self.transcribe(audio_path, language)

        # Add detailed segment information
        detailed_segments = []
        for segment in result["segments"]:
            detailed_segments.append({
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"].strip(),
                "words": segment.get("words", [])
            })

        result["detailed_segments"] = detailed_segments
        return result
