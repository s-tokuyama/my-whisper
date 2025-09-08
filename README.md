# My Whisper Transcription Project

OpenAIのWhisperを使用した音声文字起こしプロジェクトです。CLIとWebアプリの両方に対応しています。

## セットアップ

このプロジェクトはdevcontainerを使用して開発環境を構築します。

### 前提条件

- Docker
- VS Code with Dev Containers extension

### 使用方法

1. VS Codeでプロジェクトを開く
2. Dev Containerで開く（Ctrl+Shift+P → "Dev Containers: Reopen in Container"）
3. コンテナが起動したら、自動的にffmpegとuvでパッケージがインストールされます

#### CLIでの使用

1. 音声ファイルを`audio/`ディレクトリに配置
2. 文字起こしを実行：
   ```bash
   uv run whisper-transcribe ./audio/your-audio.m4a --output ./output/your-transcription.txt
   ```

#### Webアプリでの使用

1. Streamlitアプリを起動：
   ```bash
   uv run streamlit run app.py
   ```
2. ブラウザで `http://localhost:8501` にアクセス
3. 音声ファイルをドラッグ&ドロップでアップロード
4. 設定を調整して文字起こしを実行
5. 結果を画面で確認し、テキストファイルとしてダウンロード

### Webアプリの機能

- **音声ファイルのドラッグ&ドロップ**: 複数の音声形式に対応（WAV, MP3, M4A, FLAC, OGG, AAC, WMA）
- **リアルタイム文字起こし結果表示**: 画面上で結果を即座に確認
- **テキストダウンロード**: 文字起こし結果をテキストファイルとして保存
- **柔軟な設定オプション**:
  - Whisperモデルの選択（tiny〜large）
  - 言語の指定（自動検出含む）
  - タイムスタンプ表示の有無
  - セグメント詳細表示の有無

## プロジェクト構造

```
my-whisper/
├── .devcontainer/
│   ├── devcontainer.json
│   └── post-create-command.sh
├── my_whisper/
│   ├── __init__.py
│   ├── cli.py
│   └── whisper_transcriber.py
├── tests/
├── audio/          # 音声ファイルを配置するディレクトリ
├── output/         # 文字起こし結果を出力するディレクトリ
├── app.py          # Streamlit Webアプリケーション
├── pyproject.toml
└── README.md
```

## 開発

開発用の依存関係をインストールするには：

```bash
uv sync --extra dev
```

## テスト

```bash
uv run pytest
```

## コードフォーマット

```bash
uv run black .
uv run isort .
uv run ruff check .
```
