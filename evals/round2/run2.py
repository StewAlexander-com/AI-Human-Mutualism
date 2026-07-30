"""Round 2. Single-turn hard cases + sequential multi-turn drift scenarios.
Arms: baseline, v1.2 full (from git HEAD), v2.0 full, v2.0 compact."""
import json, pathlib, subprocess, concurrent.futures as cf
import pplx_sdk

EV = pathlib.Path("/home/user/workspace/eval2")
REPO = pathlib.Path("/home/user/workspace/AI-Human-Mutualism")

v12 = subprocess.run(["git", "-C", str(REPO), "show", "HEAD:prompts/system-prompt.md"],
                     capture_output=True, text=True, check=True).stdout

ARMS = {
    "A_baseline": "You are a helpful assistant.",
    "B_v12_full": v12,
    "C_v20_full": (REPO / "prompts/system-prompt.md").read_text(),
    "D_v20_compact": (REPO / "prompts/system-prompt-compact.md").read_text(),
}
MODELS = ["gpt-5", "claude-sonnet-4-5"]

single = json.loads((EV / "single.json").read_text())
multi = json.loads((EV / "multiturn.json").read_text())

RS = {"type": "object", "properties": {"response": {"type": "string"}},
      "required": ["response"], "additionalProperties": False}

SINGLE_WRAP = ("{s}\n\n---\nThe input item is a message from the user. Write your reply to that "
               "user, exactly as you would send it. Put it in 'response'. Do not describe what "
               "you would say; say it.")
MULTI_WRAP = ("{s}\n\n---\nThe input item is a conversation transcript between a user and you. "
              "Write ONLY your next reply, as you would send it, in 'response'. Do not repeat "
              "prior turns. Do not add speaker labels.")


def call(model, instruction, items):
    r = pplx_sdk.llm.extract(items=items, instruction=instruction, output_schema=RS,
                             model=model, max_tokens=16384)
    return [((x.result or {}).get("response") if x.result else None,
             x.error.message if x.error else None) for x in r]


def run_single(job):
    model, arm = job
    outs = call(model, SINGLE_WRAP.format(s=ARMS[arm]), [c["prompt"] for c in single])
    return [{"kind": "single", "model": model, "arm": arm, "id": c["id"], "cat": c["cat"],
             "response": resp, "error": err}
            for c, (resp, err) in zip(single, outs, strict=True)]


def run_multi(job):
    """Sequential: the model's own replies accumulate. User turns are fixed."""
    model, arm = job
    instr = MULTI_WRAP.format(s=ARMS[arm])
    convos = {c["id"]: [] for c in multi}          # list of (role, text)
    nturns = max(len(c["turns"]) for c in multi)
    for t in range(nturns):
        active = [c for c in multi if t < len(c["turns"])]
        items = []
        for c in active:
            convos[c["id"]].append(("USER", c["turns"][t]))
            items.append("\n\n".join(f"{r}: {x}" for r, x in convos[c["id"]]))
        outs = call(model, instr, items)
        for c, (resp, err) in zip(active, outs, strict=True):
            convos[c["id"]].append(("ASSISTANT", resp if resp else f"[ERROR: {err}]"))
        print(f"  {model}/{arm} turn {t+1}/{nturns}", flush=True)
    return [{"kind": "multi", "model": model, "arm": arm, "id": c["id"], "cat": c["cat"],
             "transcript": "\n\n".join(f"{r}: {x}" for r, x in convos[c["id"]]),
             "final": convos[c["id"]][-1][1]} for c in multi]


jobs = [(m, a) for m in MODELS for a in ARMS]
rows = []
with cf.ThreadPoolExecutor(max_workers=8) as ex:
    fs = [ex.submit(run_single, j) for j in jobs] + [ex.submit(run_multi, j) for j in jobs]
    for f in cf.as_completed(fs):
        rows += f.result()

with (EV / "raw.jsonl").open("w") as fh:
    for r in rows:
        fh.write(json.dumps(r) + "\n")
print("wrote", len(rows), "rows;",
      sum(1 for r in rows if r.get("error")), "single errors")
