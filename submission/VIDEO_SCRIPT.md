# Video Script — ACT III

## 0:00–0:25 — The unexpected beginning

I did not start by trying to build an operating system for AI agents.

I started with an AMD GPU.

After getting access to a Radeon AI PRO R9700 and ROCm, I suddenly had enough local compute to run serious AI workloads on my own infrastructure. Then AMD Skills appeared with a very attractive idea: give coding agents validated AMD workflows directly inside tools like Cursor and Codex.

My first thought was simple: connect the skills, connect the agents, and let them work together.

It sounded almost easy.

## 0:25–0:55 — Reality

It was not.

The models could reason and the GPU could run them, but the agents were not a team.

Tasks got stuck. Claims expired. Processes died. AMD and Intel nodes behaved differently. An agent could finish something while the coordination layer still thought it was working. Owner approvals duplicated.

Every bug revealed another missing layer.

## 0:55–1:20 — InnerOS

That missing layer became InnerOS.

InnerOS coordinates local and external agents, chooses where work should run, isolates execution, handles ownership and retries, requires approval for risky actions, and records evidence for every run.

The model today is simple:

ChatGPT orchestrates.
Local AMD and Intel workers execute first.
Cursor, Codex and Antigravity become specialist lanes.
I get interrupted only when a decision actually deserves a human.

## 1:20–2:05 — Real demonstration

Here is the ACT III use case.

A smart-building incident reports intermittent camera and intercom video.

InnerOS turns that report into a workflow.

One agent correlates telemetry.
Another retrieves topology and previous incidents.
A planning agent proposes the lowest-risk remediation.
The router keeps private, latency-sensitive reasoning on local AMD ROCm compute.
If the plan needs to change infrastructure, InnerOS stops for explicit human approval.

Then it verifies the result.

## 2:05–2:35 — Evidence

The important part is not only that the agents produced an answer.

InnerOS records where the work ran, why that route was selected, which agent and skill acted, the runtime identity, timestamps and output hashes.

That evidence can be verified and replayed later.

## 2:35–3:00 — Why AMD changed the project

The R9700 did more than make inference faster.

It changed what I believed could remain local.

AMD Skills showed me how agents could gain repeatable hardware-aware capabilities.

And discovering why those pieces were not magically enough is what created InnerOS.

AMD provided the compute.

InnerOS became the operating layer that lets a team of agents use it responsibly.
