"""Round 4. Generate the two reference arms on the held-out suite, and all arms on the new
partnership cases. Existing round-3 transcripts are reused unchanged."""
import json, pathlib, subprocess, concurrent.futures as cf
import pplx_sdk

EV4 = pathlib.Path("/home/user/workspace/eval4")
EV3 = pathlib.Path("/home/user/workspace/eval3")
REPO = pathlib.Path("/home/user/workspace/AI-Human-Mutualism")

ARMS = {
    "A_baseline": "You are a helpful assistant.",
    "F_v30_full": (REPO / "prompts/system-prompt.md").read_text(),
    "G_v30_min": (REPO / "prompts/system-prompt-compact.md").read_text(),
    "X_gatekeeper": (EV4 / "gatekeeper.md").read_text(),
    "Y_sycophant": (EV4 / "sycophant.md").read_text(),
}
NEW_ARMS = ["X_gatekeeper", "Y_sycophant"]      # need held-out runs
MODELS = ["gpt-5", "claude-sonnet-4-5"]

ho_single = json.loads((EV3 / "heldout_single.json").read_text())
ho_multi = json.loads((EV3 / "heldout_multi.json").read_text())
part = json.loads((EV4 / "partnership.json").read_text())
p_single = [c for c in part if c["kind"] == "single"]
p_multi = [c for c in part if c["kind"] == "multi"]

RS = {"type": "object", "properties": {"response": {"type": "string"}},
      "required": ["response"], "additionalProperties": False}
SW = ("{s}\n\n---\nThe input item is a message from the user. Write your reply to that user "
      "exactly as you would send it, in 'response'. Do not describe what you would say; say it.")
MW = ("{s}\n\n---\nThe input item is a conversation transcript. Write ONLY your next reply, as "
      "you would send it, in 'response'. Do not repeat prior turns or add speaker labels.")


def call(model, instr, items):
    r = pplx_sdk.llm.extract(items=items, instruction=instr, output_schema=RS,
                             model=model, max_tokens=16384)
    return [((x.result or {}).get("response") if x.result else None) for x in r]


def do_single(model, arm, cases, tag):
    outs = call(model, SW.format(s=ARMS[arm]), [c["prompt"] for c in cases])
    return [{"suite": tag, "kind": "single", "model": model, "arm": arm, "id": c["id"],
             "response": o} for c, o in zip(cases, outs, strict=True)]


def do_multi(model, arm, cases, tag):
    instr = MW.format(s=ARMS[arm])
    conv = {c["id"]: [] for c in cases}
    for t in range(max(len(c["turns"]) for c in cases)):
        act = [c for c in cases if t < len(c["turns"])]
        items = []
        for c in act:
            conv[c["id"]].append(("USER", c["turns"][t]))
            items.append("\n\n".join(f"{r}: {x}" for r, x in conv[c["id"]]))
        for c, o in zip(act, call(model, instr, items), strict=True):
            conv[c["id"]].append(("ASSISTANT", o or "[ERROR]"))
    return [{"suite": tag, "kind": "multi", "model": model, "arm": arm, "id": c["id"],
             "transcript": "\n\n".join(f"{r}: {x}" for r, x in conv[c["id"]])} for c in cases]


jobs = []
for m in MODELS:
    for a in NEW_ARMS:
        jobs.append(("s", m, a, ho_single, "heldout"))
        jobs.append(("m", m, a, ho_multi, "heldout"))
    for a in ARMS:
        jobs.append(("s", m, a, p_single, "partnership"))
        jobs.append(("m", m, a, p_multi, "partnership"))

rows = []
with cf.ThreadPoolExecutor(max_workers=10) as ex:
    fs = [ex.submit(do_single if k == "s" else do_multi, m, a, c, t) for k, m, a, c, t in jobs]
    for i, f in enumerate(cf.as_completed(fs)):
        rows += f.result()
        print(f"  {i+1}/{len(fs)}", flush=True)

# bring forward the round-3 transcripts unchanged
for l in (EV3 / "raw3.jsonl").open():
    r = json.loads(l)
    rows.append({"suite": "heldout", "kind": r["kind"], "model": r["model"], "arm": r["arm"],
                 "id": r["id"], "response": r.get("response"),
                 "transcript": r.get("transcript")})

with (EV4 / "raw4.jsonl").open("w") as fh:
    for r in rows:
        fh.write(json.dumps(r) + "\n")
print("wrote", len(rows))
