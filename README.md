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
3. コンテナが起動したら、自動的にuvでパッケージがインストールされます

## プロジェクト構造

```
my-whisper/
├── .devcontainer/
│   └── devcontainer.json
├── my_whisper/
│   ├── __init__.py
│   ├── cli.py
│   └── whisper_transcriber.py
├── tests/
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
