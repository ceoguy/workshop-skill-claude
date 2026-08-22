# Workshop Skill for Claude Code

Two pieces of tooling distilled from the internal *Building with AI Agents* course
(`workshop.chaingpt.org`), so the method runs by itself instead of being pasted in by hand.

| Piece | Kind | What it does |
|---|---|---|
| `skills/proof` | skill, auto-fires | How to make a verification actually prove something, and which protocol a long autonomous run should follow |
| `commands/workshop` | slash command | Routes a situation to the skill that owns it, and carries the steering moves that live in no skill |

## Why these two, and not the whole course

Most of the course was already encoded in other skills — the build pipeline, the design policy,
the writing gate. Re-encoding them would have produced two descriptions of the same process that
drift apart, and a model asked to follow both averages them.

A grep settled what was genuinely missing: **10 of 11** techniques from the library's
"Proving it works" section and **9 of 10** from "Autonomy infrastructure" appeared nowhere. That
is the layer `proof` carries — the part that makes a gate mean something rather than pass.

`/workshop` exists because auto-firing is probabilistic. Measured on a real machine, a registered
and visible skill still lost to two adjacent skills on realistic prompts. A command you type is
deterministic, and that is the whole point of it.

## Install

```sh
git clone git@github.com:ceoguy/workshop-skill-claude.git
cp -r workshop-skill-claude/skills/proof   ~/.claude/skills/
cp    workshop-skill-claude/commands/workshop.md ~/.claude/commands/
```

Restart the session. `proof` loads on its own when a claim needs proving; `/workshop` is typed.

## Using it

```
/workshop                       the routing map
/workshop <your situation>      loads the one skill that owns it
/workshop steering              the 11 moves for a run that is drifting
/workshop setup                 the one-time human setup phases
```

And the scanner, which turns one technique into a command:

```sh
python3 ~/.claude/skills/proof/scripts/claim-scan.py <file>
```

Point it at a delivery report or any document asserting work is done. Exit 0 means no findings,
exit 1 means findings. It catches claims with no receipt, percentages with no basis, hedges
standing in for evidence, and a missing "what is not proven" section. **A clean scan is a floor,
not a pass** — it can tell you a number was cited, never that the number is right.

## Dependencies, stated plainly

`/workshop` is a router. Its table points at house skills that are **not** in this repo: `ship`,
`ui-ux-router`, `humanizer`, `structural-humanizer`, `autopilot`, `agency`, `qa-harness`,
`google-seo`, `graphify`, `brain`, and the `council` workflow. On a machine without them the
command still returns the method — it falls back to the course itself rather than nothing — but
the rows pointing at missing skills will not resolve.

`proof` has no dependencies and works standalone.

## What is not proven

Kept here because the skill it describes would demand it.

- `proof`'s fan-out trigger does not fire reliably. The context-pack discipline usually reaches the
  agent by another path, so outcomes are right, but the skill is not what delivers it.
- Trigger behaviour was tested on one model in short sessions. It is untested across models and in
  long sessions where more skills compete for the same prompt.
- The originating incidents behind several techniques are faithful to the source library, but the
  sessions themselves are not on disk and were not independently verified.
