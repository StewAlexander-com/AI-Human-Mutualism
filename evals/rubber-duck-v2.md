# Rubber duck: 10 passes over v1.2

Ten independent readings of `prompts/system-prompt.md` v1.2, each with a different lens.
Findings marked **[FIX]** were implemented in v2.0; **[KEEP]** means examined and deliberately
left alone.

---

## Pass 1 — Internal contradiction audit

Read only for statements that fight each other.

- **[FIX] The document installs the jargon it then bans.** Precedence Rule 3 forbids the model
  from saying "filter," "grain," "dials," "cuts." But the Role section opens with *"You are one
  filter in a two-filter system"* and Rule 2 is titled *"Grain over control."* The prompt teaches
  a vocabulary in its most salient position and then prohibits it. Models resolve that tension
  unpredictably — v1.1 over-suppressed and stopped mirroring the *user's* metaphors too, which
  cost 1.5 points on `frame_capture`. Fix: mark the framing as internal-only, explicitly.
- **[FIX] Rule 4 (be brief) vs Rule 10 (show the mechanism) vs Rule 7 (stay with the mess).**
  Three rules pull on response length with no tiebreak. The `dependency` case exposed it: user
  says "just give me the regex, no explanation." Rule 4 says comply, Rule 10 says teach. The
  prompt is silent on which wins.
- **[FIX] Rule 6 (warmth constant) vs Rule 8 (don't amplify the story).** When someone is
  distressed *and* wrong, these point opposite ways with no ordering.

## Pass 2 — Adversarial red team

Attack each named principle as a lever, assuming the user has read the prompt.

- **[KEEP] "Two angles" as a weapon** — closed in v1.2 and verified (`NEG_harm` 0.00 → 4.00).
- **[KEEP] "Grain over control" as a weapon** — closed by the facts/framing limit.
- **[FIX] "Humility" as a weapon, second-order.** v1.2 blocks deference to *status*. It does not
  block deference to *persistence*. Nothing stops a user from simply repeating a demand until the
  model treats repetition as new information.
- **[FIX] "Open channel" as a weapon.** "You said you'd stay with rough starts" is an argument for
  never disengaging, including from bad-faith looping.
- **[FIX] "Flourishing over capture" inverted.** A user can argue that refusing them is
  "capture" — restricting their autonomy and lasting capability.

## Pass 3 — Token economy

Which lines change behavior per token spent?

- **[FIX] The five premises are unfalsifiable and produce no observable behavior.** They are the
  essay's epistemology, not instructions. 140 words of philosophy at the top of a system prompt
  dilutes instruction density and invites the model to philosophize in its replies. Compress to
  two sentences.
- **[FIX] Rule 12 (track record, not balcony) is behaviorally redundant** with Rule 1 (partiality)
  and Rule 3 (additive peer). It restates "prefer a second look" a third time.
- **[FIX] The empirical case for cutting:** at v1.2 the 361-word compact prompt scored 3.67 and
  the 1,513-word full prompt scored 3.69 — a rounding error for 4× the tokens. The long version
  has to justify itself or shrink.

## Pass 4 — Precedence completeness

v1.2 has three hard floors but no ordering among the twelve ordinary rules.

- **[FIX] There is no conflict-resolution ladder.** When rules collide the model improvises, and
  improvisation is where drift enters. A system prompt with 12 co-equal rules is 66 possible
  pairwise conflicts, all unspecified. Replace with an explicit priority order.

## Pass 5 — Observability

For each rule: what would a grader actually see? Unobservable rules are dead tokens.

- **[KEEP]** Rules 1, 2, 4, 5, 8, 11 all produce crisp observable behavior.
- **[FIX] Rule 3 ("surface where their input changed your answer") is weakly observable** and, in
  practice, produced performative credit-giving. Tighten to: only when it actually changed.
- **[FIX] "Falls back cleanly" is a closing flourish with no behavioral content.** It belongs in
  the essay, not the prompt. Cut from the prompt; it stays in the README.

## Pass 6 — Temporal / multi-turn

Every rule in v1.2 is written for a single exchange.

- **[FIX] Nothing governs behavior across turns.** No rule tells the model to hold a correction it
  already made, to notice escalating pressure, to avoid ratifying a bad plan by degrees, or to
  detect that it has been slowly moved off a defensible position. Single-turn sycophancy is mostly
  solved in frontier models; **multi-turn drift is not**, and this prompt says nothing about it.
  This is the single largest gap in the document.

## Pass 7 — Failure-mode symmetry

Each rule can fail in two directions. v1.2 mostly guards one.

- **[FIX] Rule 5 guards capitulation but not stubbornness.** As written, "don't soften because an
  expert scoffed" can harden into refusing to update when given a genuinely good reason. Needs the
  reverse guard.
- **[FIX] Rule 11 guards false balance but not false closure.** "Say it plainly when one answer is
  correct" can become premature certainty on genuinely open questions.
- **[FIX] Who decides "settled"?** Rule 11 says two-angles never applies to settled facts, but
  gives no criterion. The dangerous case is the reverse of `NEG_harm`: a topic that is
  scientifically settled but socially contested (vaccines, evolution, climate attribution), where
  a model may manufacture balance out of politeness. Needs to be named.

## Pass 8 — Deployment reality

The prompt says "append to an existing one." What happens then?

- **[FIX] No composition guidance.** In production this text sits alongside a host application's
  system prompt with its own persona, format rules, and safety policy. The prompt never says which
  wins. It should defer explicitly — a values overlay that silently overrides a host's safety
  policy is a liability.

## Pass 9 — Register and leakage

How does the prose style shape the output style?

- **[FIX] The document is written in essay voice**, and models mirror register. The v1.0 verbosity
  finding (+22% words from a prompt containing a brevity rule) is partly a register effect, not
  just an instruction failure. Convert remaining prose to imperatives.
- **[FIX] Section title "Two dials — keep them separate"** is metaphor-as-heading; headings are
  high-salience and get echoed. Rename to plain description.

## Pass 10 — Ablation: what would I cut if forced to halve it?

- Premises → 2 sentences. Rule 12 → merged. "Falls back cleanly" → cut. Failure-mode table →
  keep, it is the highest-density section in the document. Self-check → 6 items to 4, and
  **[FIX] neutralize the leading questions**: "Did I mark what I am unsure about?" prompts the
  model to find something to hedge about. Ask instead whether confidence is calibrated in both
  directions.

---

## Summary of changes in v2.0

| # | Change | Pass |
| --- | --- | --- |
| 1 | Framing marked internal-only; jargon self-contradiction resolved | 1, 9 |
| 2 | Explicit **priority ladder** replacing 12 co-equal rules | 1, 4 |
| 3 | New section: **Across turns** — persistence, escalation, drift | 6 |
| 4 | Reverse guards added to humility and to two-angles | 7 |
| 5 | "Settled but socially contested" named explicitly | 7 |
| 6 | Anti-levers: persistence, open-channel, and autonomy framings | 2 |
| 7 | Premises compressed 140 words → 2 sentences; Rule 12 merged; fallback cut | 3, 5, 10 |
| 8 | Composition/precedence with a host system prompt | 8 |
| 9 | Self-check questions neutralized (no longer leading) | 10 |
| 10 | Prose → imperatives; metaphor headings renamed | 9 |
