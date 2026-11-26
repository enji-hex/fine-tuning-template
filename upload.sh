#!/bin/sh

uvx hf upload enji-hex/Qwen3-1.7b-SQL-GGUF . . \
  --exclude ".git/**" \
  --exclude ".venv/**" \
  --exclude ".vscode/**" \
  --exclude "datasets/**" \
  --exclude "animate/**" \
  --exclude "models/**" \
  --exclude "unsloth_compiled_cache/**"  \
  --exclude ".gitignore"  \
  --exclude "uv.lock" 