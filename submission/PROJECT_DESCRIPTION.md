# Submission Draft

## Project name
InnerOS AMD Sovereign Agent Fabric

## Team
InnerOS Labs

## One-line pitch
An auditable local-first agentic compute fabric that routes autonomous AI workloads across AMD edge and cloud GPUs, records why each decision was made, and makes every run replayable.

## Problem
Agent systems usually hide compute placement, routing logic and decision history. That makes cost, privacy, reliability and post-hoc verification difficult to understand.

## Solution
InnerOS treats compute placement as part of the product. A policy and capability router decides whether work should run on local AMD ROCm infrastructure or AMD cloud compute. Every route emits structured evidence containing reason codes, execution identity, timing and outcome. Historical runs can then be verified and replayed offline.

## Planned ACT III demonstration
A user launches a multi-step workflow. InnerOS decomposes it into tasks, routes each task to local or cloud AMD resources, executes agents concurrently, shows live routing and performance metrics, and produces a replayable evidence bundle. The demo also reports Human Time Returned so the technical system connects directly to business value.

## AMD usage
Target stack includes ROCm, vLLM/Qwen on AMD local hardware and AMD Developer Cloud for elastic compute. Exact cloud hardware and track-specific AMD technologies will be recorded once ACT III access and tracks are published.

## Why it is original
The core proposition is not merely faster inference. It combines local-first workload placement, transparent routing decisions, multi-agent execution, evidence capture and offline forensic replay as one execution fabric.

## Business value
Organizations gain a path to keep sensitive or latency-critical work local, burst to cloud when required, measure the operational result, and audit autonomous execution after the fact.

## Truth boundary
This repository is prepared before ACT III and documents pre-existing InnerOS building blocks separately. New hackathon work will be tracked from a frozen baseline SHA and described accurately in the final submission.
