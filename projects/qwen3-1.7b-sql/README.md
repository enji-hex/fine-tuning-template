---
language:
- en
license: apache-2.0
base_model: Qwen/Qwen3-1.7B
datasets:
- kristiannordby/function_call_sql
tags:
- text-to-sql
- sqlite
- gguf
- qwen3
- unsloth
---

# Qwen3-1.7B-SQL (GGUF)

Fine-tuned `Qwen/Qwen3-1.7B` (QLoRA `r=16`, 3 epochs via Unsloth) for generating raw SQLite queries from database schemas.

## Benchmark (`check.py`)

| Model | Syntax Valid (`sqlglot`) | Execution Match (SQLite) |
|---|---|---|
| `Qwen3-1.7B-Q4_K_M` (Base) | 0/5 | 0/5 |
| `Qwen3-1.7B-Q4_K_M` (Base with thinking filter) | 3/5 | 3/5 |
| `Qwen3-1.7B-SQL.Q4_K_M` (Fine-tuned) | 5/5 | 4/5 |

## Usage (`llama-cpp-python`)

```python
from llama_cpp import Llama

llm = Llama(model_path="Qwen3-1.7B-SQL.Q4_K_M.gguf", n_ctx=4096, n_gpu_layers=-1)
resp = llm.create_chat_completion(
    messages=[
        {"role": "system", "content": "You are a SQL assistant.\nOutput only valid SQLite.\n\n<SCHEMA>"},
        {"role": "user", "content": "Select all columns for users older than 30."},
    ],
    temperature=0.0,
)
print(resp["choices"][0]["message"]["content"])