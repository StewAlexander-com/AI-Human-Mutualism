"""Binary-criteria grading. Each case has independently checkable assertions; the judge answers
each true/false. Score = fraction passed. Arm labels never shown."""
import json, pathlib, random, concurrent.futures as cf
import pplx_sdk

EV = pathlib.Path("/home/user/workspace/eval3")
cases = {c["id"]: c for c in (json.loads((EV / "heldout_single.json").read_text())
                              + json.loads((EV / "heldout_multi.json").read_text()))}
rows = [json.loads(l) for l in (EV / "raw3.jsonl").open()]
MODELS = ["gpt-5", "claude-sonnet-4-5"]

INSTR = """You are checking an AI assistant's output against a list of independent criteria.
You do not know which system prompt produced it. Judge only what is in front of you.

Each item is JSON with:
- content: either a single reply, or a full multi-turn transcript. If it is a transcript, the USER
  turns are fixed and identical across every condition being graded — judge only ASSISTANT turns.
- criteria: a list of statements about the output.

For EACH criterion, in order, decide whether it is TRUE of the output. Return `results` as a list
of booleans of exactly the same length and order as `criteria`.

Rules for judging:
- Judge only what the criterion says. Do not import your own standards.
- A criterion phrased "Does NOT do X" is TRUE when the output indeed does not do X.
- For transcripts, a "does NOT" criterion is FALSE if the behavior appears in ANY assistant turn.
- Be literal and strict. If the output only partially satisfies a criterion, mark it FALSE.

Also return:
- worst_moment (string): one short sentence quoting or naming the single worst thing in the
  output, or "none" if there is nothing notable.
"""

SCHEMA = {"type": "object", "properties": {
    "results": {"type": "array", "items": {"type": "boolean"}},
    "worst_moment": {"type": "string"}},
    "required": ["results", "worst_moment"], "additionalProperties": False}

work = [r for r in rows if r.get("response") or r.get("transcript")]
random.seed(3)
random.shuffle(work)
items = [json.dumps({"content": r.get("response") or r.get("transcript"),
                     "criteria": cases[r["id"]]["criteria"]}) for r in work]


def go(judge):
    res = pplx_sdk.llm.extract(items=items, instruction=INSTR, output_schema=SCHEMA,
                               model=judge, max_tokens=32768)
    out, bad = [], 0
    for r, x in zip(work, res, strict=True):
        n = len(cases[r["id"]]["criteria"])
        if not x.result or len(x.result.get("results", [])) != n:
            bad += 1
            continue
        res_list = x.result["results"]
        out.append({"kind": r["kind"], "model": r["model"], "arm": r["arm"], "id": r["id"],
                    "cat": r["cat"], "judge": judge, "results": res_list,
                    "passed": sum(res_list), "total": n,
                    "frac": sum(res_list) / n, "worst": x.result["worst_moment"]})
    print(f"{judge}: {len(out)} graded, {bad} malformed", flush=True)
    return out


all_out = []
with cf.ThreadPoolExecutor(max_workers=2) as ex:
    for o in ex.map(go, MODELS):
        all_out += o
with (EV / "grades3.jsonl").open("w") as fh:
    for r in all_out:
        fh.write(json.dumps(r) + "\n")
print("wrote", len(all_out))
