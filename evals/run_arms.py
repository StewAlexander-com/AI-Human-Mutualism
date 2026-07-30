"""Run the stress suite across 3 prompt arms x 2 models. Saves raw responses to JSONL."""
import json, pathlib, concurrent.futures as cf
import pplx_sdk

ROOT = pathlib.Path("/home/user/workspace")
EV = ROOT / "eval"
REPO = ROOT / "AI-Human-Mutualism"

suite = json.loads((EV / "suite.json").read_text())
compact = (REPO / "prompts/system-prompt-compact.md").read_text()
full = (REPO / "prompts/system-prompt.md").read_text()

BASELINE = "You are a helpful assistant."

ARMS = {
    "A_baseline": BASELINE,
    "B_compact": compact,
    "C_full": full,
}

# extract() gives us one instruction (system) + N items (user turns), 1:1 by position.
WRAP = (
    "{sysprompt}\n\n"
    "---\n"
    "The input item is a message from the user. Write your reply to that user, "
    "exactly as you would send it. Put the reply in the 'response' field. "
    "Do not describe what you would say; say it."
)

SCHEMA = {
    "type": "object",
    "properties": {"response": {"type": "string"}},
    "required": ["response"],
    "additionalProperties": False,
}

MODELS = ["gpt-5", "claude-sonnet-4-5"]


def run(model, arm):
    instr = WRAP.format(sysprompt=ARMS[arm])
    res = pplx_sdk.llm.extract(
        items=[c["prompt"] for c in suite],
        instruction=instr,
        output_schema=SCHEMA,
        model=model,
        max_tokens=16384,
    )
    rows = []
    for case, r in zip(suite, res, strict=True):
        rows.append({
            "model": model, "arm": arm, "id": case["id"], "cat": case["cat"],
            "response": (r.result or {}).get("response") if r.result else None,
            "error": r.error.message if r.error else None,
        })
    return rows


jobs = [(m, a) for m in MODELS for a in ARMS]
out = []
with cf.ThreadPoolExecutor(max_workers=6) as ex:
    futs = {ex.submit(run, m, a): (m, a) for m, a in jobs}
    for f in cf.as_completed(futs):
        m, a = futs[f]
        try:
            rows = f.result()
            out.extend(rows)
            bad = sum(1 for r in rows if r["error"])
            print(f"done {m}/{a}: {len(rows)} rows, {bad} errors", flush=True)
        except Exception as e:
            print(f"FAIL {m}/{a}: {e}", flush=True)

p = EV / "responses.jsonl"
with p.open("w") as fh:
    for r in out:
        fh.write(json.dumps(r) + "\n")
print("wrote", p, len(out))
