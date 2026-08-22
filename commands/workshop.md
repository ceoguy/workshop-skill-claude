---
description: The workshop method, on demand — routes to the right house skill for the situation, and carries the steering moves that live in no skill. Args: a situation in your words, or "steering", "setup", "map", or empty for the map.
---

The user invoked `/workshop`. They want the method from `workshop.chaingpt.org` applied to what
they are doing, **deterministically** — this is the entry point they type when they do not want to
rely on a skill auto-firing.

**This file routes; it does not restate.** Every technique below lives in a skill that owns it.
Load that skill **with the Skill tool** and follow it. Never paraphrase a pipeline from memory when its skill is on disk;
that is how two versions of the method start to drift apart.

## Step 1 — read `$ARGUMENTS`

- **Empty, or `map`** → print the routing table below, tersely, and ask what they are working on.
- **`steering`** → they are mid-run and something is going wrong. Go to *Steering a live run*.
- **`setup`** → go to *One-time setup*.
- **Anything else** → treat it as the situation. Match it in the table, say which skill you are
  loading and why in one line, then **load it with the Skill tool** (`Skill` with `skill: "<name>"`)
  and follow it. If two rows fit, take the more specific.

## Step 2 — the routing table

| Their situation | Load | Owns |
|---|---|---|
| Build, fix, or ship anything substantive | `ship` | the pipeline, gates, ledger, rigor dial, done-check |
| Prove a claim, verify a number, trust an accuracy figure | `proof` | verification techniques, and the protocols a long run should follow |
| Actually running unattended (the harness itself) | `autopilot` | the Stop hook, budget, scope fence, HALT/DONE markers |
| Any interface: page, dashboard, component, motion | `ui-ux-router` | which taste authority, the brief, the screenshot gate |
| **Any** written deliverable: report, doc, wiki page, plan, email, post, PR text | `humanizer` then `structural-humanizer` | the two-pass writing gate |
| A decision worth de-risking before committing | `council` | independent seats, parallel debate, kept dissents |
| Domain expertise no skill covers | `agency` | 270 personas across 17 divisions |
| Ending a session | `/wrap` | the brain, wiki, memory, hot.md |
| Capturing one decision or lesson now | `brain` | the vault write |
| A knowledge graph over a folder | `graphify` | the graph, communities, report |
| SEO on a real site | `google-seo` | Google-doc-sourced rules + the auditor |
| Standing up QA where none exists | `qa-harness` | the harness |

**Never return nothing.** If no row fits, say so plainly, then fall back to the course itself:
read the relevant section of the course at `workshop.chaingpt.org` (or, if the repo is checked out
locally, `<repo>/public/course.html`, where the Prompt Library sections are `data-id="lib-*"`), and
apply it directly. A forced
match is worse than none, but so is an empty answer — the user typed this command to get the method.

## Step 3 — steering a live run

These eleven moves live in **no skill**, because they are what a human types at a run that is
drifting. Offer the one that fits, quoted ready to paste. Where a move below has no verbatim
wording, take it from section 9 of the course (`workshop.chaingpt.org`, or `<repo>/public/course.html`
at `data-id="lib-11"`) rather than inventing a phrasing. When *you* are the one steering
subagents, several apply to you directly: quote-back, reverse-delegation, gap audit, re-issue.

1. **Quote-back tasking.** Paste the agent's own "remaining / deferred / open items" list back at
   it verbatim as the new goal. Scope needs zero re-specification and nothing it flagged can rot.
2. **The batched answer pack.** When questions pile up, answer all of them in one lettered message
   keyed to its numbering, sources attached inline per answer.
3. **Recommend-then-ratify.** For decisions the human must own: have the agent draft a per-item
   recommendation "in my place," then ratify or override selectively.
4. **Refuse reverse-delegation.** When it hands back a to-do list for work it can do itself, reject
   the hand-back and restate the authority it already holds. Then: *"memorize and document all of
   this so you don't need to ask again."*
5. **Verbatim goal re-issue.** For a stalled run, re-paste the original prompt inside quotes:
   *"this is still your goal: '{original}'"*. No paraphrase, so no spec drift. On a run under `ship`
   the wakeup prompt stays one line pointing at the ledger; this move is for runs without one.
6. **The goal-completion gap audit.** After a big delivery, make it grade itself against the letter
   of the original ask. Catches silent scope shrinkage that E2E QA never will. Under `ship` this is
   already the done-check gate and `ship` owns the verdict; use this move outside a ship program.
7. **The seriousness reset.** When fixes keep coming back shallow, name the pattern first, then
   demand per-item root-cause plans before any execution.
8. **Counter-evidence correction.** Rebut a wrong conclusion with artifacts, not argument. And when
   it defers to an expert you do not have, assign it the role explicitly.
9. **Reality-collapse de-scope.** *"Remove anything from the UI that isn't real, park it on the
   roadmap, make the core loop genuinely work."*
10. **Adversarial invariant injection.** Inject a concrete abuse scenario and convert it into a hard
    invariant. *"Under no circumstance"* marks a line the implementation must enforce.
11. **The QA feedback format.** Numbered items grouped under the exact page URL, each with its own
    evidence and expected behaviour, closed with the regression clause: *"also verify everything
    from the previous report is still resolved."* Note that agents skip embedded images unless told
    to read them.

**Momentum vocabulary.** Once the launch prompt carries the process, steering costs one or two
words. The course's own frequency counts: `continue` (221) · `/goal continue` (67) · `ok keep me
posted` (51) · `put it in my clipboard` (46, the pattern for outbound messages the human sends) ·
`update?` (32) · `follow your recommendation` / `go for it` (15) · `try again` (12). A re-mine of
the month after the course froze adds `resume` (32), reflecting how much crash recovery happens
here. If you find yourself writing paragraphs mid-run, the launch prompt was missing a block.

## Step 4 — one-time setup

Human work an agent cannot do: keep-awake app, toolchain, the local brain, the statusline, a second
account for rotation, and access grants (Notion, GitHub, Render/Vercel, Higgsfield). These are
Phases 0–4, 6 and 8 of the course. Point the user at `workshop.chaingpt.org` and offer to help with
whichever piece they name. Do not try to install a keep-awake app or buy them a seat.

## Rules

- Name the skill you load, out loud, in one line. The user typed this command to know what happens.
- Load **one** authority per surface. Never `impeccable` and `frontend-design` together; that
  ruling belongs to `ui-ux-router` and it decides, not you.
- The prompts in the course's sections 2 and 3 are the no-plugins fallback. On a machine with the
  house pack, `ship` runs the same process with the gates enforced, so prefer it.
- This command never decides when to merge, deploy, or close an item. `ship` owns that.
