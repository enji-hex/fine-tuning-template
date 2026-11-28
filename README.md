
## rfc-finetuning-template

General template for fine tuning experiments.

Current future ideas is following:
| Tune Name                                          | Purpose                                                    | Status      |
| -------------------------------------------------- | ---------------------------------------------------------- | ----------- |
| [Text-to-SQL](./projects/qwen3-1.7b-sql/README.md) | SQL query generation from natural text.                    | DONE        |
| Telegraphic style thinking tunig                   | Cut extra tokens during thinking phase.                    | IN PROGRESS |
| In-turn code execution                             | Increase model ability to handle calculation-related tasks | IN PROGRESS |


**Backlog ideas**
- Text-to-MongoDB: Translate natural language descriptions into complex MongoDB queries (same deterministic verification pattern as Text-to-SQL).

#### Proposed project structure

```text
repo:
|- models   (local)
|- datasets (local)
|-project/project-N
        |- README.md        # Modelcard
        |- train.ipnb       # Cloud/Colab-ready fine-tuning & GGUF export pipeline
        |- check.py         # Deterministic evaluation & verification harness
        |- base_eval.json   # Default model evaluation metrics
        |- tune_eval.json   # Tuned model evaluation metrics
        |- model.gguf
        |- Modelfile
```

#### Proposed HF uploading system
```sh
cd ./project-N && hf push ..
```

**Reasons**:
- All experiments stays in one github repo, without model files
- HF repos contains ONLY flat ready to use sub-repo snaphots
- Ability to test new model agains several experiments
