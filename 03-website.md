# 03 — Website (Space 3: local console)

## Role **[DECIDED]**
A LOCAL web app that is (a) a **visualization of the project** (roadmap, knowledge graph, current
activity, checkpoints) and (b) **the human's channel to the orchestrator**. It talks to the
orchestrator only via the local bus + files — never by routing Claude.

## Comms **[DECIDED — see 05]**
- Hosts the **local HTTP loopback bus** (its own backend) for website→orchestrator messages.
- Reads `state.json` (and the knowledge base) to render live state.

## Launch **[DECIDED]**
The orchestrator's start command boots the website as a local background process.

## To close **[OPEN]**
- The screen list (candidate set: project dashboard, roadmap/todos, knowledge-graph viewer, checkpoint
  console, activity/agent log, handoff/restart prompt).
- The "contact the orchestrator" UX (how you send a message / answer / verdict).
- Whether it streams live agent activity or shows state snapshots.
- Stack **[DEFERRED]**.
