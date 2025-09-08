"""Tests for my_whisper package."""

import pytest

from my_whisper.whisper_transcriber import WhisperTranscriber


class TestWhisperTranscriber:
    """Test cases for WhisperTranscriber class."""

    def test_init(self) -> None:
        """Test transcriber initialization."""
        transcriber = WhisperTranscriber(model="tiny")
        assert transcriber.model_name == "tiny"
        assert transcriber.model is not None

    def test_transcribe_file_not_found(self) -> None:
        """Test transcribe with non-existent file."""
        transcriber = WhisperTranscriber(model="tiny")

        with pytest.raises(FileNotFoundError):
            transcriber.transcribe("non_existent_file.wav")

    # Note: Integration tests with actual audio files would require test audio files
    # and would be slower, so they're not included in basic unit tests
