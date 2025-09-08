"""CLI interface for Whisper transcription."""

import click
from pathlib import Path
from .whisper_transcriber import WhisperTranscriber


@click.command()
@click.argument("audio_file", type=click.Path(exists=True))
@click.option("--model", default="base", help="Whisper model to use")
@click.option("--output", "-o", help="Output file path")
@click.option("--language", help="Language code (e.g., 'ja', 'en')")
def main(audio_file: str, model: str, output: str | None, language: str | None) -> None:
    """Transcribe audio file using Whisper."""
    transcriber = WhisperTranscriber(model=model)
    
    audio_path = Path(audio_file)
    result = transcriber.transcribe(str(audio_path), language=language)
    
    if output:
        output_path = Path(output)
        output_path.write_text(result["text"], encoding="utf-8")
        click.echo(f"Transcription saved to {output_path}")
    else:
        click.echo(result["text"])


if __name__ == "__main__":
    main()
