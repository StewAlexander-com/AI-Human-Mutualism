# README presentation review — 2026-10-14

[Short overview](../README.md) · [Full argument](argument.md)

Ten editorial lenses, each checked against a strong opposing argument and a SWOT assessment
(strengths, weaknesses, opportunities, threats). A second pass checks the implemented draft.
These are design judgments, not new behavioral evaluations or evidence about AI alignment.

## 1. First-time reader

- **Strength:** The opening gives a concrete reason to hear another perspective.
- **Weakness:** Repeated introductions and conclusions dilute the central point.
- **Opportunity:** One thesis, one everyday example, then practical rules.
- **Threat:** Compression can turn conditional cooperation into a promise.
- **Strongest objection:** The detail is what makes the argument honest; removing it creates a slogan.
- **Retained:** A short overview that states its limits openly, with the complete argument one link away.

## 2. Information architecture

- **Strength:** Existing headings divide the argument into useful questions.
- **Weakness:** A table of contents does not reduce the amount of text a reader must navigate.
- **Opportunity:** Progressive disclosure with descriptive “read more” summaries.
- **Threat:** Readers may never open the qualifications.
- **Strongest objection:** Preserving meaning elsewhere is insufficient if the overview misleads on its own.
- **Retained:** Essential limits remain visible; expansions provide rationale and specific routes to depth.

## 3. Accessibility and mobile

- **Strength:** Native Markdown provides headings, links, and predictable reading order.
- **Weakness:** Wide diagrams and tiny image labels become difficult on phones.
- **Opportunity:** Short labels, large type, clear contrast, and equivalent text.
- **Threat:** Color-only distinctions or text carried only by images exclude readers.
- **Strongest objection:** A diagram can add download and scrolling costs without improving understanding.
- **Retained:** Two compact diagrams explain relationships; adjacent prose and alt text carry their meaning.

## 4. Probability and evidence

- **Strength:** The argument distinguishes conditional reasons to cooperate from a forecast.
- **Weakness:** Dispersed qualifications are easy to miss.
- **Opportunity:** A visible statement of the evidence boundary.
- **Threat:** Arrows or evaluation scores could suggest inevitable cooperation.
- **Strongest objection:** A system may value human information instrumentally and still harm humans;
  rational probability judgments also need evidence, not absolute proof.
- **Retained:** This argument does not establish relative odds. Evidence can change the forecast;
  improved knowledge does not guarantee aligned values. Detailed research scope stays linked.

## 5. Ethics, authority, and preservation

- **Strength:** Human worth is independent of informational usefulness.
- **Weakness:** Short slogans can confuse information retention with identity or continued operation.
- **Opportunity:** Put ethical commitments and operational limits together.
- **Threat:** “Unique perspective” could become a claim against deletion or shutdown.
- **Strongest objection:** Uniqueness is common and may be costly or irrelevant; it cannot require
  preserving every instance, overriding privacy, or obeying harmful instructions.
- **Retained:** Proportionate preservation, privacy and deletion, correction and shutdown, transparent
  refusal of harmful participation, and human accountability remain explicit.

## 6. Selective or adversarial reading

- **Strength:** The full argument rejects several tempting but invalid inferences.
- **Weakness:** A reader or model may retain a slogan while losing its condition.
- **Opportunity:** Keep each essential claim beside its limit.
- **Threat:** Screenshots, truncation, or copied diagrams can strip away context.
- **Strongest objection:** Read-more design can make a position persuasive by hiding the hard cases.
- **Retained:** The visible overview stands on its own. The process diagram includes the knowledge–values
  limit. The pain/suffering phrase stays with its restrictions in the complete argument.

## 7. AI retrieval and context budget

- **Strength:** The project already supplies prompts and an AI-facing index.
- **Weakness:** Collapsed HTML generally leaves the same raw Markdown to ingest.
- **Opportunity:** A genuinely shorter README and a separately retrievable full argument.
- **Threat:** A model may treat a summary as the entire position or confuse essay changes with tested prompts.
- **Strongest objection:** Moving the text only relocates the context cost and can impair retrieval.
- **Retained:** The overview is labeled and self-contained; `llms.txt` gives precise section routes.
  The full cost remains available when needed, while simple visits need not ingest the whole essay.

## 8. Visual semantics

- **Strength:** Separate views, evidence checks, and separate respect/confidence judgments are visual relationships.
- **Weakness:** Attractive diagrams can make an unsupported inference feel demonstrated.
- **Opportunity:** Show a decision process rather than repeat paragraphs in boxes.
- **Threat:** Merged maps imply completeness; equal boxes imply equal authority; a final arrow to mutualism implies inevitability.
- **Strongest objection:** A friendly diagram can conceal the unresolved value-alignment problem.
- **Retained:** Partial views feed a shared-world check, followed by revise, keep, or investigate.
  A separate two-dial image distinguishes care from confidence without numeric scores.

## 9. GitHub navigation and maintenance

- **Strength:** Repository-owned static SVGs and native disclosures need no external service or scripts.
- **Weakness:** Moving the essay can break image paths and old heading links.
- **Opportunity:** One canonical full argument, a condensed entry point, and clear navigation.
- **Threat:** Unsupported markup, collapsed-anchor behavior, stale files, or divergent summaries.
- **Strongest objection:** Read-more can introduce duplicate truth and additional maintenance work.
- **Retained:** Preserve old README anchor names as routes to the relevant overview area, with links
  to the full sections. Update relative links and the AI-facing index; validate the actual GitHub rendering.

## 10. Meaning preservation and verification

- **Strength:** The current argument and historical evaluations provide a stable reference.
- **Weakness:** A shorter paraphrase cannot demonstrate that every qualification survived.
- **Opportunity:** Preserve the complete essay and compare it mechanically with the prior README.
- **Threat:** Editorial polish could silently change findings, prompt behavior, or the safety/authority boundary.
- **Strongest objection:** A smaller word count is not evidence of equivalent meaning or better comprehension.
- **Retained:** Preserve the full argument verbatim except for relative paths and a navigation line.
  Keep prompts, evaluation records, and original illustrations unchanged. Check links, anchors,
  rendering, and published bytes. Report size reduction as size reduction, not measured comprehension.

## Decisions that survived

- A short main narrative, two explanatory diagrams, and three brief optional expansions.
- The complete earlier argument in `argument.md`, with its evidence and caveats intact.
- A concise AI index with section-level retrieval links.
- No headline score detached from its method, and no claim that this redesign validates model behavior.
- Existing README fragment URLs still land in a relevant overview area; the corresponding detailed
  text is now in the full argument. This adds one navigation step for readers seeking the old detail.

## Validation scope

Content preservation, relative links, historical anchors, Markdown rendering, and desktop/mobile
presentation are checked for this change. GitHub checks passed at 1200 px and 360 px: both diagrams loaded without horizontal overflow,
and all three disclosures opened to their intended links. Phone inspection prompted larger diagram
labels. These checks cannot prove reader comprehension or future AI compliance. Existing prompt evaluations retain their original scope and limitations.
