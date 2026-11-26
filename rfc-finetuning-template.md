
title: rfc-finetuning-template

Proposed project structure

```
repo:
|- models   (local)
|- datasets (local)
|---project-N
    |- notebook.ipnb
    |- check.py
    |- results.json
    |- README.md
```

Proposed HF uploading system
```sh
cd ./project-N && hf push
```

Reasons:
- All experiments stays in one github repo, without model files
- HF repos contains ONLY flat ready to use sub-repo snaphots
- Ability to test new model agains several experiments
