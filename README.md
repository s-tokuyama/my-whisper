# My Whisper Transcription Project

OpenAIのWhisperを使用した音声文字起こしプロジェクトです。

## セットアップ

このプロジェクトはdevcontainerを使用して開発環境を構築します。

### 前提条件

- Docker
- VS Code with Dev Containers extension

### 使用方法

1. VS Codeでプロジェクトを開く
2. Dev Containerで開く（Ctrl+Shift+P → "Dev Containers: Reopen in Container"）
3. コンテナが起動したら、自動的にffmpegとuvでパッケージがインストールされます
4. 音声ファイルを`audio/`ディレクトリに配置
5. 文字起こしを実行：
   ```bash
   uv run whisper-transcribe ./audio/your-audio.m4a --output ./output/your-transcription.txt
   ```

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
