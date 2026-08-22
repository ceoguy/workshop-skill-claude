---
name: proof
description: How to make a verification actually prove something, and which protocol a long autonomous run should follow. Load when a claim has to be trusted rather than believed: blind reproduction of a trusted output, held-out ground truth, byte-identical regression gates, fail-closed negative tests, proof-of-controls dossiers, eval hygiene and leakage self-tests, the DATA-DRIFTED third QA verdict, maiden runs, scoring a generative pipeline against a human baseline, and through-the-product evidence. Also load before any fan-out of subagents (the context pack), when rebuilding or porting something already trusted, when an agent is about to act outside its fence, and whenever work is about to be CALLED DONE and the evidence has to hold up. Triggers: "prove it", "how do we know", "can we trust this number", "is it actually done", "rebuild it from the spec", "does it fail closed", "ground truth", "accuracy", "leakage", "before we go live", "maiden run", "spawn subagents", "fan out", "run unattended", "overnight", "when should it stop". Composes with other skills, never replaces them: `ship` owns the gates and when to merge or deploy, `autopilot` owns the unattended harness, domain skills own their domain. This file only says what would make their checks mean something.
---

# Proof

`ship` owns the pipeline: plan, review, merge, deploy, QA, done-check. It says *that* a gate must pass. This skill is *how* you make a gate mean something, and how a run behaves when nobody is watching.

Mined from the sessions where the output had to be exactly right. Every technique below is here because a weaker version of it failed first.

## The one idea

A test that reads the answer from the same place it checks proves nothing. Every technique here is a way of getting a **second, independent** source of truth: a human's prior output, a held-out column, a frozen artifact, an adversary, the running system itself. If your verification has only one source, it is a restatement, not a proof.

---

## Part A — proving a claim

### Pick by what you are proving

| You need to trust | Reach for |
|---|---|
| A rebuild, port, or reimplementation | Blind reproduction |
| Anything that maps, classifies, or scores | Held-out ground truth |
| A refactor whose output is already trusted | Byte-identical regression gate |
| A credential- or permission-gated feature | Fail-closed negative test |
| A safety-critical control | Proof-of-controls dossier |
| An accuracy or eval number | Eval hygiene |
| A generative or creative pipeline | Score against the humans |
| A design or plan under high stakes | Counsel judged by execution |
| A generative output that could be faked by hand | Through-the-product evidence |
| A write path that has never fired for real | Pull maiden runs forward |
| A prod sweep whose data moved under it | The third QA verdict (DATA-DRIFTED) |

### Blind reproduction
The strongest validation move there is. Make the system rebuild something a trusted human already produced, with a no-peeking fence, then diff on the same inputs.

> Rebuild the {endpoint / export / parser} from the spec alone, without looking at the current implementation. No peeking at the existing code. Then we diff your version against production on the same inputs.

### Held-out ground truth (anti-tautology)
Derive the answer from first principles, then compare against a reference column the deriving code never saw. This caught a real tautology that plan-audit loops had missed. Add an out-of-sample case to every check.

### Byte-identical regression gate
When refactoring a pipeline whose output is already trusted, the gate is not "tests pass". It is *the frozen known-good artifact reproduces byte-identically*. Git-diff-empty on the untouched path, SHA-pinned inputs, and a freeze check wired into the verify command.

### Fail-closed negative test
Prove the feature fails **closed** with the exact expected status, and ship that test as a first-class prod gate. Pre-decide both branches before you run it: confirmed → record the evidence and let ship's remaining gates run; not confirmed → STOP, fix the gating, redeploy, re-verify. This test is evidence for a gate, not a substitute for one; `CLOSED`/`DELIVERED` still require ship's QA and done-check.

### Proof-of-controls dossier
For safety-critical systems, "the control exists and tests pass" is not done. Script an adversarial attempt to defeat **each** control (double-post it, tamper the audit chain two ways, silence the approver, self-mint authorization) and compile a control-by-control table with real evidence. A control that fails to prove is a real gap, not a flaky test.

### Eval hygiene
Pre-registered scoring, a sealed future blind month, SHA-pinned label sets, provenance on every corpus entry, and a runnable leakage self-test whose expected result is null (empty training data must produce zero precedent hits). Standing rule: if ground truth may have leaked into training, flag it LOUDLY and quarantine.

> A perfect score is a leak signal, not a win.

### Score against the humans
For creative pipelines: export the team's actually-shipped output as the benchmark corpus, score generated output against it on named numeric bars, and when a metric misses, **fix the generator and regenerate** rather than hand-patching the output. Exit when the pipeline consistently beats the human baseline, with honest per-iteration scorecards.

### Through-the-product evidence
When QAing anything generative, forbid hand-crafted proof: it must be created **through the system, not by you directly**. One specimen per output type into a reviewable catalogue, so readiness cannot be faked by the agent's own writing skill.

### Counsel judged by execution
For high-stakes designs, reviewers must **re-perform** the plan's claims: live API probes, byte comparisons, re-deriving hashes from the engine code. Not read-review them. Distinguish material findings from non-material notes (fold the latter in as hygiene). Re-performance is the requirement here; the round structure is ship's and this technique raises the bar of its **council gate**, which re-convenes on findings and stops after three rounds without unanimity by handing the founder the split verdict. Do not confuse that with ship's prose branch (one bounded round plus one re-review), which is a different instrument.

### Two verdicts that stop a false pass

**The third QA verdict.** Prod sweeps get three outcomes, not two: PASS, FINDINGS (fix, restart from scratch), and **DATA-DRIFTED**, meaning the underlying data went stale mid-sweep, so void the pass without counting it a failure, re-sync, re-sweep. And verify a deploy by grepping the actually-served content, never a local build hash.

**The overfitting guard.** Not every loop should run to unanimity. When further tightening starts producing false positives, stop and report the residual to the user by name. This is a reason to escalate, never a licence to declare yourself converged: the decision to accept a residual is the user's, and ship's loop caps and reporting rules govern how that stop is made.

### Pull maiden runs forward
Read the agent's own status language for "built, heavily tested, never fired live" and force that first real execution **now**, on a safe probe, instead of letting a write path's maiden run coincide with go-live day.

---

## Part B — running unattended

### The HALT protocol
Truly stuck after two honest attempts on the same sub-problem → write a HALT file with the reason and a proposed next step, and end the turn. About to do anything destructive or outside the scope fence (`rm -rf`, force push, credential rotation, external messages, or a deploy the run was **not** authorized to make) → HALT with the proposed action and the authorization needed. Ship's pipeline authorizes a deploy at its step 5, so do not HALT on that deploy **when the run's own scope fence permits deploys at all** — otherwise every program stalls asking for permission it holds. **The run's fence is the narrower authority and it wins.** An unattended run under `autopilot` carries its own `scope.md`, whose default is *"no git push, no deploys, no external sends, no destructive operations"*; under that fence a step-5 deploy is outside scope and HALTs like anything else. Ship authorizing a step does not widen a fence the founder drew. Keep a terse per-iteration journal: `iter 5 | did X | next Y`.

### The trust ladder
Agents that act externally (posting, sending, booking) graduate through stages: **shadow mode** (everything generated, nothing sent) → **one approval-gated supervised action** → **per-type autopilot** only after a trust period, with explicit NEVER_AUTO locks on high-stakes action types. The takeover moment is always human-gated.

**The ladder has a ceiling it may never climb past.** Outbound messages to humans are always founder-sent (draft them clipboard-ready), and purchases and credentials are FOUNDER ACTIONS. Those never graduate to autopilot at any rung. The ladder governs machine-facing actions, not the ones ship reserves for the founder.

### Event-driven, not schedule-driven
Mature loops convert from polling to watchers: a background monitor on prod logs, a drop-folder watcher, CI/deploy monitors. Scheduled wakeups demote to backstops. Every wakeup opens with the preemption clause: *if the owner sent new feedback in the meantime, address that FIRST.*

### Deploy shepherds
The minimal loop: a tiny single-purpose agent that polls one thing to an observable gate, then stops.

> Shepherd PR 47: check CI; when green, merge per approval; verify the deploy unpins the API-calls tile; then wrap.

### The scope-exhaustion stop
The right end state for an autonomous program is not "everything done" but **autonomously-buildable scope provably exhausted**: every surviving item labelled with the exact external gate blocking it (credential, legal counsel, owner data, cutover decision), prioritized P1/P2/P3, delivered as a final summary, and the loop explicitly forbidden from scheduling another wakeup.

### Scheduled routines as the backstop
`/schedule` creates a durable cron-style routine that fires whether or not a session is open, which is what carries a program across days. Write every routine stateless: it must assume no memory of prior runs, read the ledger first, and report only what changed. Watchers on real events still beat polling, so schedules are the backstop, not the primary signal.

### Watchdog and fallback deliverable
Long research or workflow runs get a hang detector (no journal writes for 10+ minutes = hung) and a pre-authorized fallback: kill it and synthesize the deliverable from the journal plus what was already gathered. **The report ships either way.**

### Parallel-agent coordination
Two agents on one repo: watch both branch heads for a git quiet streak (unchanged across two consecutive checks = done), then merge in a fresh integration worktree that touches neither agent's tree, build and test, and hand over the verified branch plus the push command. The human can short-circuit the wait at any time by saying they are done.

### The role-sharded audit swarm
Different from a council, which debates one plan. Shard a product audit **by lens**, one specialist per dimension (architecture, product, UI, UX, performance, devops, cost, business model), consolidate into a master report, put that report through ship's prose branch once, then execute it as the backlog.

### Never launch subagents blind
Subagents start with zero session history, so an ungrounded swarm hallucinates confidently. Before any fan-out, write a 150–400 word context pack (the goal, the decisions and constraints established so far, the facts that live only in this conversation) plus the exact file paths agents must read first, and thread both into every prompt with the anti-hallucination clause:

> Read these before answering; do not guess. Cite the file each fact came from. If a fact is not in your context or these files, output UNKNOWN, never invent.

A grounded swarm beats a bigger blind one.

---

## The scanner

A deterministic pre-check for any delivery report, `PROOF.md`, or document asserting work is done. It catches the grep-able slice: claims with no receipt, percentages with no basis, hedges standing in for evidence, and a missing honest ceiling.

```sh
python3 ~/.claude/skills/proof/scripts/claim-scan.py <file>
```

Exit 0 means no findings, exit 1 means findings. **A clean scan is a floor, not a pass** — it cannot tell you a cited number is correct, only that a number was cited. The judgment techniques above still apply.

## Where this sits

- **`ship`** owns the pipeline and its gates. When it says a gate must pass, this skill says what would make that gate mean something.
- **`qa-harness`** stands up the harness; this decides what the harness must prove.
- **`council`** runs the debate; *counsel judged by execution* above is what raises its bar for high stakes.

Do not restate the ship pipeline here, and do not let this skill decide when to merge or deploy. That is ship's job.
