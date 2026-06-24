# Technical Notes: Reimplementing The Agent Evidence System

These notes are for someone who wants to understand and reimplement the hard technical parts of the event-agent research system: notebook rendering, notebooks as agent reasoning surfaces, notebooks as durable knowledge, prompt surfaces, telemetry, and report rendering.

The core lesson is that this system is not a prompt demo. It is an artifact-driven agent workflow. The agents matter, but the real reliability comes from the files they produce, the contracts those files obey, and the regression checks that prove the workflow still works after many turns.

## 1. The Main Technical Challenge

The difficult part is not getting an agent to write a plausible answer. The difficult part is making an agent system produce evidence that can be inspected later.

A single run needs to answer:

- What question was proposed?
- What alternatives were rejected?
- Why was one question selected?
- What prior memory was read?
- Was the question a statistical hypothesis, an EDA question, or a workflow task?
- Which dataset and unit of analysis were used?
- Which notebook was written and executed?
- What caveats apply?
- What did the report say?
- Can the whole process be replayed?

That means the implementation needs more than an LLM call. It needs structured candidate records, notebook artifacts, Markdown exports, telemetry events, prompt hashes, report HTML, and phase regression summaries.

## 2. Notebooks As Agent Reasoning Surfaces

The notebooks are not merely output reports. They are an agent reasoning surface. A turn notebook captures what the agents selected, what data was used, how the result was framed, what caveats apply, and what future agents can reuse.

The notebook should include:

- selected candidate
- candidate kind and semantic slot
- public question
- result summary
- formal hypothesis, when available
- experimental design
- statistical test output
- diagnostics
- caveats
- validation contract
- source notebook/cell references for follow-up questions

This makes the notebook a bridge between agent reasoning and deterministic execution. The agent can say, "This is the question we selected." The code can say, "This is the result and contract." The notebook puts both in one inspectable artifact.

The practical challenge is to avoid treating the notebook as prose only. A notebook should contain executable cells with structured payloads. If it only contains markdown narrative, future agents and tests cannot reliably inspect it.

## 3. Notebook Rendering And Execution

Use `nbformat` to build notebooks programmatically. Treat notebooks as structured JSON documents with markdown cells, code cells, metadata, outputs, and execution counts.

Two execution modes are useful:

- lightweight execution
- `nbclient` execution

Lightweight execution is useful for deterministic generated notebooks that only need simple Python evaluation. It can execute code cells in a controlled namespace, capture stdout, and store outputs. It is fast and avoids heavy kernel startup.

`nbclient` execution is closer to real Jupyter behavior. It should be used when notebook maturity matters, but it requires a working kernel environment and has more ways to fail.

Do not conflate execution levels:

| Status | Meaning |
| --- | --- |
| `scaffolded` | Notebook exists but code has not run. |
| `lightweight_executed` | Generated cells ran through the lightweight executor. |
| `nbclient_executed` | Notebook ran through a Jupyter kernel via `nbclient`. |
| `validated` | Notebook passed an explicit validation contract. |

The report evaluator should cap claims based on notebook status. A scaffolded notebook cannot support a validated finding. A lightweight-executed notebook is useful, but it is not the same as full notebook validation.

## 4. Notebook Validation Contracts

A generated notebook can drift away from the statistical runner if values are copied into multiple places. The fix is to embed a validation contract.

The runner creates a contract with the fields the notebook must expose. The notebook computes an observed contract from its visible payload and asserts equality.

Example:

```python
validation_contract = result_summary.get("notebook_validation_contract", {})
observed_contract = {
    "schema_version": validation_contract.get("schema_version"),
    "kind": selected_candidate.get("kind"),
    "metric": result_summary.get("metric"),
    "value": result_summary.get("value"),
    "claim_strength": result_summary.get("claim_strength"),
}
assert all(
    observed_contract.get(key) == validation_contract.get(key)
    for key in observed_contract
)
```

A stronger contract should also check:

- semantic slot
- statistical decision
- p-value fields
- adjusted decision
- design identifier
- data snapshot hashes
- source notebook references

This does not prove the analysis is correct. It proves the notebook did not silently diverge from the run payload.

## 5. Markdown Exports As Agent Knowledge

Raw `.ipynb` files are poor reading material for agents. They are verbose JSON. They include output structures, metadata, and cell wrappers. Agents need a compact, readable surface.

That is why every notebook should have a Markdown export.

Recommended pair:

```text
turn-07-semantic-msa.ipynb
turn-07-semantic-msa.md
```

The `.ipynb` file preserves execution metadata. The `.md` file becomes the agent-readable wiki surface.

This pattern lets the next turn read prior results without parsing notebook JSON. It also gives human reviewers something they can inspect in a normal diff or text viewer.

## 6. Notebook Knowledge Base

Markdown exports are useful, but the system also needs structured memory. The notebook knowledge base should extract facts from each turn into machine-readable JSON and readable Markdown.

Recommended artifacts:

```text
notebook-knowledge.json
notebook-knowledge.md
```

Each entry should include:

- notebook path
- markdown path
- selected candidate
- result summary
- notebook status
- validation metadata
- semantic slot
- hypothesis seeds
- source cells
- caveats

This is how notebooks become long-term agent knowledge. Later turns can use prior notebook cells to generate follow-up questions, avoid duplicates, carry forward null results, or request stronger designs.

The gotcha is memory noise. If every notebook dumps too much prose into the knowledge base, future turns become harder to steer. Keep the JSON structured and keep the Markdown summary compact.

## 7. Wiki Files

The wiki layer is a lightweight coordination mechanism. It should be append-oriented and readable.

Recommended files:

```text
SCHEMA.md
index.md
log.md
question-board.md
decision-records.md
caveats.md
semantic-map.md
findings.md
```

These files have different jobs:

- `SCHEMA.md` defines workspace conventions.
- `index.md` catalogs notebooks and exports.
- `log.md` records append-only activity.
- `question-board.md` records proposed and selected questions.
- `decision-records.md` records why choices were made.
- `caveats.md` keeps limitations visible.
- `semantic-map.md` links questions to data slots.
- `findings.md` summarizes durable results.

Do not rewrite history casually. Append new entries. If a finding is superseded, add a supersession note rather than deleting the older result.

## 8. Prompt Surfaces

Prompt files are useful, but they should not be the only place behavior lives.

A good split is:

- Markdown prompt/spec files define role, voice, responsibilities, prohibited behaviors, and claim boundaries.
- Code enforces candidate schemas, scoring, routing, notebook execution, telemetry, and report generation.

The agent roles used in the original workflow were:

- Spark: generate ideas.
- Skeptic: protect methodology and caveats.
- Mapper: connect questions to data, semantic slots, and memory.
- Moderator: rank and select.
- DataAgent: write notebooks and durable artifacts.

The mistake to avoid is putting enforceable contracts into prompt prose only. "Do not overclaim" is a useful prompt instruction, but the report evaluator should also enforce claim caps. "Do not route workflow tasks into statistical testing" is a useful instruction, but the classifier should enforce it.

## 9. Prompt Hashes And Provenance

Prompt drift is a real reproducibility problem. If role files change, run behavior may change even when code and data do not.

Store prompt hashes in every session:

```json
{
  "friend_prompt_hashes": {
    "Spark": "...",
    "Skeptic": "...",
    "Mapper": "...",
    "Moderator": "...",
    "DataAgent": "..."
  },
  "evidence_prompt_hashes": {}
}
```

Use SHA-256 over the prompt/spec file contents.

Reports should show whether:

- friend prompt hashes are present
- evidence prompt hashes are present
- all expected prompt specs loaded
- stale/default prompt warnings exist

This prevents silent fallback to default prompts.

## 10. Telemetry And Logging

Logging should be structured and replayable. A text log is not enough.

Each event should include:

- event id
- sequence number
- time offset
- event type
- turn number
- actor
- summary
- payload

Useful event types:

- `turn.started`
- `knowledge.read`
- `board.proposed`
- `board.ranked`
- `semantic.query`
- `hypothesis.classified`
- `question.submitted`
- `workflow.stage`
- `result.studied`
- `notebook.created`
- `wiki.updated`
- `knowledge.updated`
- `discussion.message`
- `memory.seeded`
- `turn.completed`

The important gotcha is to log rejected candidates, not only selected ones. Without the rejected board, a reviewer cannot understand the selection decision.

Another gotcha is workflow visibility. If the report is wrong, you need to know whether the failure came from candidate generation, classification, data access, statistical testing, notebook writing, or report rendering.

## 11. Playback Rendering

The playback UI is a static HTML view over telemetry. It should not need a server.

Implementation pattern:

1. Write `friends_loop_telemetry.json`.
2. Generate `ui/index.html`.
3. Embed or load the telemetry payload.
4. Render current event, board, workflow stage, discussion, result, and timeline.

If embedding JSON into HTML, escape dangerous sequences:

```python
payload = json.dumps(telemetry, ensure_ascii=False).replace("</", "<\\/")
```

This prevents embedded JSON from prematurely closing a script tag.

Test moved-log rendering. The UI should still work if someone copies `friends_loop_telemetry.json` away from the original run directory and rebuilds the playback HTML from that file.

## 12. Business Report Rendering

The business report is different from playback. Playback explains process. The business report explains evidence.

The business report should show:

- public question
- H0/H1 when available
- data/design
- statistical result
- interpretation
- caveats
- next action

Avoid internal handles in headlines. The report should not lead with `semantic_msa_batch_supported_positive`. It should lead with the public question.

Escape all public text before rendering HTML. Forum questions, candidate rationales, and caveats may contain characters that need HTML escaping.

## 13. Markdown-To-HTML Documentation Rendering

The project also needed browser-readable documentation versions. If you render Markdown to HTML, preserve:

- headings
- tables
- code fences
- inline code
- links
- ordered and unordered lists
- Mermaid blocks

The most common bug is treating headings inside fenced code blocks as real page headings. Track whether the parser is inside a code fence.

For Mermaid diagrams, a simple documentation page can use:

```html
<script type="module">
  import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
  mermaid.initialize({ startOnLoad: true, theme: "default" });
</script>
```

For production evidence reports, do not rely on external CDNs unless the report can still be understood without rendered diagrams.

## 14. Statistical Claim Boundaries

Notebook and report surfaces must preserve statistical caution.

A rejected null means the result rejected H0 under the recorded exploratory design. It does not prove causality.

Enforce this in multiple places:

- prompt instructions
- methodology cards
- result summaries
- notebook caveats
- report language
- evidence promotion logic
- report evaluator tests

The system should distinguish:

- exploratory association
- descriptive pattern
- validated finding
- publishable finding

Do not let a p-value alone promote a claim. Require design quality, diagnostics, notebook maturity, multiple-testing context, and caveats.

## 15. Multi-Turn Gotchas

Single-turn tests are not enough. Multi-turn runs expose different failures:

- repeated questions
- stale memory
- missing notebook exports
- workflow tasks routed as hypotheses
- report drift
- prompt hash omissions
- telemetry gaps
- evidence overpromotion
- duplicate semantic slots

Use a 20-turn regression after changes to candidate selection, prompts, notebooks, telemetry, reports, or memory.

A good 20-turn summary should check:

- requested turns
- completed workflows
- stopped early flag
- workflow-task statistical misroutes
- metadata coverage
- notebook status counts
- report files
- playback files
- prompt hash coverage
- caveat visibility

## 16. Reimplementation Checklist

For a clean reimplementation, build in this order:

1. Session JSON and run directory.
2. Static candidate board.
3. Candidate selection and rejected candidate record.
4. Notebook writer.
5. Markdown notebook export.
6. Wiki files.
7. Notebook knowledge JSON.
8. Telemetry events.
9. Playback HTML.
10. Business report HTML.
11. Hypothesis classifier.
12. Statistical test runner.
13. Prompt files and prompt hashes.
14. Report evaluator.
15. 20-turn regression summary.

The key is to keep every layer inspectable. If a future engineer can open the files and reconstruct what happened, the system is on solid ground.

## 17. Final Practical Advice

Treat notebooks as evidence objects, not decorations.

Treat Markdown exports as agent-readable memory, not secondary documentation.

Treat prompts as versioned inputs, not invisible configuration.

Treat telemetry as a product surface, not debug spam.

Treat reports as claim-governance tools, not marketing pages.

If those principles hold, the reimplementation will preserve the most important technical achievement of the original system: agents that generate ideas and evidence while leaving behind enough structure for humans and future agents to inspect, challenge, and improve the work.
