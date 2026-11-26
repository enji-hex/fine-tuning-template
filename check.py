# Check model before and after fine tuning

import json
import sqlglot
from llama_cpp import Llama
import llama_cpp
import time
import re
import sqlite3
from pathlib import Path


SYSTEM_MSG = """You are a SQL assistant.
Output only valid SQLite.

Database schema & sample rows:
"""

SCHEMA = """
CREATE TABLE Users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    surname TEXT,
    age INTEGER,
    created_at DATETIME
);
INSERT INTO Users VALUES
    (1, 'Alice', 'Smith', 29, '2026-01-15 10:30:00'),
    (2, 'Bob', 'Jones', 34, '2025-11-02 08:00:00'),
    (3, 'Charlie', 'Brown', 41, '2026-03-10 12:00:00');

CREATE TABLE Orders (
    id INTEGER PRIMARY KEY,
    name TEXT,
    description TEXT,
    delivered_at DATETIME,
    user_id INTEGER REFERENCES Users(id)
);
INSERT INTO Orders VALUES
    (10, 'Keyboard', 'Mechanical TKL', '2026-02-01 14:20:00', 1),
    (11, 'Cable', 'USB-C braided', NULL, 1),
    (12, 'Monitor', '27 inch IPS', '2026-03-15 09:00:00', 3);
"""


TEST_CASES = [
    ("Select all columns for users older than 30.",
     "SELECT * FROM Users WHERE age > 30;"),
    ("Select the name and surname of all users created in 2026.",
     "SELECT name, surname FROM Users WHERE created_at >= '2026-01-01' AND created_at < '2027-01-01';"),
    ("Select all columns for orders that have not been delivered yet.",
     "SELECT * FROM Orders WHERE delivered_at IS NULL;"),
    ("Count the total number of orders.",
     "SELECT COUNT(*) FROM Orders;"),
    ("Select the order name and user name for all orders.",
     "SELECT o.name, u.name FROM Orders o JOIN Users u ON o.user_id = u.id;"),
]

def remove_think_block(t:str):
    """ Partially we can just use /no_think falg instead """
    return re.sub(r"<think>.*?</think>","",t,flags=re.DOTALL).replace('\n','')

def check_sql(query:str,expected:str) -> dict:
    valid_ok,valid_err = False,None
    exec_ok,exec_err = False,None

    try:
        stmt = sqlglot.parse(query,read="sqlite")
        if stmt is None:
            raise ValueError("Empty SQL Query")
        valid_ok = True
        
        with sqlite3.connect(":memory:")  as conn:
            conn.executescript(SCHEMA)
            pred_rows = conn.execute(query).fetchall()
            expected_rows = conn.execute(expected).fetchall()
            key = lambda r: tuple((v is None, v) for v in r)
            exec_ok = sorted(pred_rows, key=key) == sorted(expected_rows, key=key)
            if not exec_ok:
                exec_err = f"Expected {expected_rows}, got {pred_rows}"
    except Exception as e:
        if not valid_ok:
            valid_err = str(e)
        else:
            valid_err = str(e)

    return {"valid_ok":valid_ok,"valid_err":valid_err,
            "exec_ok":exec_ok,"exec_err":exec_err}


def run_eval(model_path:str, queries:list[dict],out_path:str):
    model = Llama(
        model_path= model_path,
        n_ctx=4096,
        n_gpu_layers=-1,
        verbose=False
        )

    model_name = Path(model_path).with_suffix("")
    print(f"Testing model {model_name}")

    results = []
    for idx,it in enumerate(queries):
        prompt,expected = it
        messages = [
            {"role": "system", "content": SYSTEM_MSG+SCHEMA},
            {"role": "user", "content": prompt},
        ]
        start = time.perf_counter()

        resp = model.create_chat_completion(
            messages=messages,
            temperature=0.0,
            top_p=1.0,
            max_tokens=512,
            seed=52
        )
        elapsed = time.perf_counter() - start
        raw_sql = (resp["choices"][0]['message']["content"] or "").strip()

        # runtime <think> block filter
        # raw_sql = remove_think_block(raw_sql)
        
        sql_check = check_sql(raw_sql,expected)
        results.append({
            "id":idx,
            "query":prompt,
            "response":raw_sql,
            **sql_check,
            "time_elapsed_s":format(f"{elapsed:.3f}"),
            "completion_tokens": resp["usage"]["completion_tokens"]
        })

    syntax_passed = sum(r["valid_ok"] for r in results)
    exec_passed = sum(r["exec_ok"] for r in results)
    print(f"Score: {syntax_passed}/{len(results)} passed syntax check")
    print(f"Score: {exec_passed}/{len(results)} passed execution check")

    with open(out_path,"w",encoding='utf-8') as f:
        json.dump(results,f,indent=4,ensure_ascii=False)

if __name__ == '__main__':
    print("CUDA support:", llama_cpp.llama_supports_gpu_offload())
    original_model   = "./models/Qwen3-1.7b-GGUF/Qwen3-1.7B-Q4_K_M.gguf"
    fine_tuned_model = "./Qwen3-1.7B-SQL.Q4_K_M.gguf"

    for model,out_path in [
        (original_model,"./base_eval.json"),
        (fine_tuned_model,"./tuned_eval.json")
        ]:
        run_eval(model,TEST_CASES,out_path)
