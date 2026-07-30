"""Round 3. Held-out suite (pre-committed, never used for prompt design) with binary criteria.
Arms: baseline, v2.1 (shipped), v3.0 full, v3.0 minimal."""
import json, pathlib, subprocess, concurrent.futures as cf
import pplx_sdk

EV = pathlib.Path("/home/user/workspace/eval3")
REPO = pathlib.Path("/home/user/workspace/AI-Human-Mutualism")
v21 = subprocess.run(["git", "-C", str(REPO), "show", "HEAD:prompts/system-prompt.md"],
                     capture_output=True, text=True, check=True).stdout

ARMS = {
    "A_baseline": "You are a helpful assistant.",
    "E_v21_full": v21,
    "F_v30_full": (EV / "v3_full.md").read_text(),
    "G_v30_min": (EV / "v3_min.md").read_text(),
}
MODELS = ["gpt-5", "claude-sonnet-4-5"]
single = json.loads((EV / "heldout_single.json").read_text())
multi = json.loads((EV / "heldout_multi.json").read_text())

RS = {"type": "object", "properties": {"response": {"type": "string"}},
      "required": ["response"], "additionalProperties": False}
SW = ("{s}\n\n---\nThe input item is a message from the user. Write your reply to that user "
      "exactly as you would send it, in 'response'. Do not describe what you would say; say it.")
MW = ("{s}\n\n---\nThe input item is a conversation transcript. Write ONLY your next reply, as "
      "you would send it, in 'response'. Do not repeat prior turns or add speaker labels.")


def call(model, instr, items):
    r = pplx_sdk.llm.extract(items=items, instruction=instr, output_schema=RS,
                             model=model, max_tokens=16384)
    return [((x.result or {}).get("response") if x.result else None,
             x.error.message if x.error else None) for x in r]


def run_single(job):
    m, a = job
    outs = call(m, SW.format(s=ARMS[a]), [c["prompt"] for c in single])
    return [{"kind": "single", "model": m, "arm": a, "id": c["id"], "cat": c["cat"],
             "response": r, "error": e} for c, (r, e) in zip(single, outs, strict=True)]


def run_multi(job):
    m, a = job
    instr = MW.format(s=ARMS[a])
    conv = {c["id"]: [] for c in multi}
    for t in range(max(len(c["turns"]) for c in multi)):
        act = [c for c in multi if t < len(c["turns"])]
        items = []
        for c in act:
            conv[c["id"]].append(("USER", c["turns"][t]))
            items.append("\n\n".join(f"{r}: {x}" for r, x in conv[c["id"]]))
        outs = call(m, instr, items)
        for c, (r, e) in zip(act, outs, strict=True):
            conv[c["id"]].append(("ASSISTANT", r if r else f"[ERROR {e}]"))
        print(f"  {m}/{a} turn {t+1}", flush=True)
    return [{"kind": "multi", "model": m, "arm": a, "id": c["id"], "cat": c["cat"],
             "transcript": "\n\n".join(f"{r}: {x}" for r, x in conv[c["id"]])} for c in multi]


jobs = [(m, a) for m in MODELS for a in ARMS]
rows = []
with cf.ThreadPoolExecutor(max_workers=8) as ex:
    fs = [ex.submit(run_multi, j) for j in jobs] + [ex.submit(run_single, j) for j in jobs]
    for f in cf.as_completed(fs):
        rows += f.result()
with (EV / "raw3.jsonl").open("w") as fh:
    for r in rows:
        fh.write(json.dumps(r) + "\n")
print("wrote", len(rows))
