"""CLI interface for Whisper transcription."""

from pathlib import Path

import click

from .whisper_transcriber import WhisperTranscriber


@click.command()
@click.argument("audio_file", type=click.Path(exists=True))
@click.option("--model", default="base", help="Whisper model to use")
@click.option("--output", "-o", help="Output file path")
@click.option("--language", default="ja", help="Language code (e.g., 'ja', 'en')")
@click.option("--timestamps", "-t", is_flag=True, help="Include timestamps in output")
def main(audio_file: str, model: str, output: str | None, language: str | None, timestamps: bool) -> None:
    """Transcribe audio file using Whisper."""
    transcriber = WhisperTranscriber(model=model)

    audio_path = Path(audio_file)
    result = transcriber.transcribe(str(audio_path), language=language)

    # Prepare output text based on timestamps option
    if timestamps and result.get("segments"):
        output_text = ""
        for segment in result["segments"]:
            output_text += f"[{segment['start']:.2f}s] {segment['text'].strip()}\n"
    else:
        output_text = result["text"]

    if output:
        output_path = Path(output)
        output_path.write_text(output_text, encoding="utf-8")
        click.echo(f"Transcription saved to {output_path}")
    else:
        click.echo(output_text)


if __name__ == "__main__":
    main()  # type: ignore
