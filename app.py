"""Streamlit web application for Whisper transcription."""

import tempfile
from pathlib import Path
from typing import Any

import streamlit as st

from my_whisper.whisper_transcriber import WhisperTranscriber


def initialize_session_state() -> None:
    """Initialize session state variables."""
    if "transcriber" not in st.session_state:
        st.session_state.transcriber = None
    if "transcription_result" not in st.session_state:
        st.session_state.transcription_result = None
    if "audio_file" not in st.session_state:
        st.session_state.audio_file = None


def create_transcriber(model: str) -> WhisperTranscriber:
    """Create or get cached transcriber instance."""
    if (
        st.session_state.transcriber is None
        or st.session_state.transcriber.model_name != model
    ):
        with st.spinner(f"Loading Whisper model '{model}'..."):
            st.session_state.transcriber = WhisperTranscriber(model=model)
    return st.session_state.transcriber


def transcribe_audio(audio_file: Any, transcriber: WhisperTranscriber, language: str | None) -> dict[str, Any]:
    """Transcribe uploaded audio file."""
    # Save uploaded file to temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(audio_file.read())
        tmp_path = tmp_file.name

    try:
        # Transcribe the audio
        result = transcriber.transcribe(tmp_path, language=language)
        return result
    finally:
        # Clean up temporary file
        Path(tmp_path).unlink(missing_ok=True)


def main() -> None:
    """Main Streamlit application."""
    st.set_page_config(
        page_title="Whisper 文字起こしアプリ",
        page_icon="🎤",
        layout="wide"
    )

    initialize_session_state()

    # Header
    st.title("🎤 Whisper 文字起こしアプリ")
    st.markdown("音声ファイルをアップロードして、AIによる高精度な文字起こしを行います。")

    # Sidebar for options
    with st.sidebar:
        st.header("⚙️ 設定")

        # Model selection
        model_options = {
            "tiny": "Tiny (39MB) - 最速",
            "base": "Base (74MB) - バランス",
            "small": "Small (244MB) - 高精度",
            "medium": "Medium (769MB) - より高精度",
            "large": "Large (1550MB) - 最高精度"
        }

        selected_model = st.selectbox(
            "Whisperモデル",
            options=list(model_options.keys()),
            format_func=lambda x: model_options[x],
            index=1  # Default to "base"
        )

        # Language selection
        language_options = {
            "auto": "自動検出",
            "ja": "日本語",
            "en": "英語",
            "zh": "中国語",
            "ko": "韓国語",
            "es": "スペイン語",
            "fr": "フランス語",
            "de": "ドイツ語",
            "it": "イタリア語",
            "pt": "ポルトガル語",
            "ru": "ロシア語",
            "ar": "アラビア語"
        }

        selected_language = st.selectbox(
            "言語",
            options=list(language_options.keys()),
            format_func=lambda x: language_options[x],
            index=0  # Default to "auto"
        )

        language = None if selected_language == "auto" else selected_language

        # Additional options
        st.subheader("📋 追加オプション")
        show_timestamps = st.checkbox("タイムスタンプを表示", value=False)
        show_segments = st.checkbox("セグメント詳細を表示", value=False)

    # Main content area
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("📁 音声ファイルアップロード")

        # File uploader
        uploaded_file = st.file_uploader(
            "音声ファイルをドラッグ&ドロップまたはクリックして選択",
            type=["wav", "mp3", "m4a", "flac", "ogg", "aac", "wma"],
            help="対応形式: WAV, MP3, M4A, FLAC, OGG, AAC, WMA"
        )

        if uploaded_file is not None:
            st.success(f"ファイルがアップロードされました: {uploaded_file.name}")
            st.info(f"ファイルサイズ: {uploaded_file.size / 1024 / 1024:.2f} MB")

            # Transcribe button
            if st.button("🎯 文字起こしを開始", type="primary"):
                transcriber = create_transcriber(selected_model)

                with st.spinner("文字起こし中..."):
                    try:
                        result = transcribe_audio(
                            uploaded_file, transcriber, language)
                        st.session_state.transcription_result = result
                        st.session_state.audio_file = uploaded_file
                        st.success("文字起こしが完了しました！")
                    except (FileNotFoundError, ValueError, RuntimeError) as e:
                        st.error(f"エラーが発生しました: {str(e)}")
                    except Exception as e:
                        st.error(f"予期しないエラーが発生しました: {str(e)}")

    with col2:
        st.header("📝 文字起こし結果")

        if st.session_state.transcription_result is not None:
            result = st.session_state.transcription_result

            # Display detected language
            if result.get("language"):
                st.info(f"検出された言語: {result['language']}")

            # Display main text
            st.subheader("📄 テキスト")
            st.text_area(
                "文字起こし結果",
                value=result["text"],
                height=200,
                key="transcription_text"
            )

            # Download button
            st.download_button(
                label="💾 テキストをダウンロード",
                data=result["text"],
                file_name=f"transcription_{Path(st.session_state.audio_file.name).stem}.txt",
                mime="text/plain"
            )

            # Show segments if requested
            if show_segments and result.get("segments"):
                st.subheader("📊 セグメント詳細")
                for i, segment in enumerate(result["segments"]):
                    with st.expander(f"セグメント {i+1}"):
                        if show_timestamps:
                            st.write(
                                f"**時間:** {segment['start']:.2f}s - {segment['end']:.2f}s")
                        st.write(f"**テキスト:** {segment['text'].strip()}")

            # Show timestamps if requested
            if show_timestamps and result.get("segments"):
                st.subheader("⏰ タイムスタンプ付きテキスト")
                timestamped_text = ""
                for segment in result["segments"]:
                    timestamped_text += f"[{segment['start']:.2f}s] {segment['text'].strip()}\n"

                st.text_area(
                    "タイムスタンプ付きテキスト",
                    value=timestamped_text,
                    height=200,
                    key="timestamped_text"
                )

                # Download timestamped text
                st.download_button(
                    label="💾 タイムスタンプ付きテキストをダウンロード",
                    data=timestamped_text,
                    file_name=f"transcription_timestamped_{Path(st.session_state.audio_file.name).stem}.txt",
                    mime="text/plain"
                )
        else:
            st.info("音声ファイルをアップロードして文字起こしを開始してください。")

    # Footer
    st.markdown("---")
    st.markdown(
        "**Whisper 文字起こしアプリ** - OpenAI Whisperを使用した高精度音声認識"
    )


if __name__ == "__main__":
    main()
