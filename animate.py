import json
import sys
import json, math, random, struct, sys, time, wave,os

START_TIME = time.monotonic()
KEYSTROKE_TIMESTAMPS: list[float] = []


RED="\033[1;31m"
YL="\033[1;33m"
GRN="\033[1;32m"
BL="\033[1;36m"
RST="\033[0m"
MUTED="\033[90m"
IT="\033[3m"

def stream_text(text: str, delay: float = 0.015) -> None:
    text = text.replace('\n',' ')
    if len(text)>90: text = text[:90]+'...'
    
    for ch in text:
        if ch != " ":
            KEYSTROKE_TIMESTAMPS.append(time.monotonic() - START_TIME)
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def run_test(title:str,fname:str) -> str:
    os.system("clear")
    stream_text(f"{BL}Model Under Test:{RST} {IT}{title}{RST}",delay=0.02)

    with open(fname, "r", encoding="utf-8") as f:
        report = json.load(f)

    for i, item in enumerate(report, 1):
        print(f"\n{BL}[{i}] PROMPT:{RST} {item['query']}")
        sys.stdout.write(f"{YL}SQL:{RST} ")
        stream_text(item["response"], delay=0.02)

        status = f"{GRN}PASS (exec_ok){RST}" if item["exec_ok"] \
            else f"{RED}FAIL{RST}"
        print(f"{MUTED}SQLite Check ->{RST} {status}")
        time.sleep(0.6)

    passed = sum(1 for i in report if i["exec_ok"])
    return f"{YL}{IT}{title:<20}{RST} passed: {passed}/{len(report)}{RST}\n"

if __name__ == '__main__':
    base = run_test("Qwen3-1.7b-GGUF","base_eval.json")
    time.sleep(1)
    tune = run_test("Qwen3-1.7b-SQL-GGUF","tuned_eval.json")
    time.sleep(1)
    print('\n')
    stream_text(base,delay=0.02)
    stream_text(tune,delay=0.02)
    time.sleep(3)