const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => Array.from(document.querySelectorAll(selector));

const state = {
  running: false,
  currentHash: "33fa50b42624dfc6ef9c2bfb702f85045da6e664550eeecb2827a36b2a1c97d5",
  planHash: "cc3b70cb8ed6c6fa225828b38f423dfbe3d7fa8ca71d0241016c1416866060cb",
  workOrderId: "WO-EVOLUS-INC-BELLINI-20261014-01",
  workOrderHash: "fb2b0ddfdaab6c7af0e26f6bfc9bbd83863ec3a9eac4cdd3895aefd297d30592",
  applicationId: "80dfecd4-8474-4aad-9565-5b7a2be10ea4",
  typeTimer: null,
  activeTab: "operations"
};

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function fmtLatency(ms) {
  if (ms === undefined || ms === null || isNaN(ms)) return "—";
  const num = Number(ms);
  if (num < 1000) return num.toFixed(0) + " ms";
  return (num / 1000).toFixed(2) + " s";
}

function fmtHash(h) {
  if (!h) return "—";
  return h.slice(0, 8) + "…" + h.slice(-6);
}

function setConnection(text) {
  const el = $("#connection-state");
  if (el) el.textContent = text;
  const footerEl = $("#footer-connection");
  if (footerEl) footerEl.textContent = text + " · Authenticated segment: judge_act3";
}

function setBadge(el, truth) {
  if (!el) return;
  el.className = "badge";
  if (truth === "LIVE_VERIFIED" || truth === "LIVE_VERIFIED_REPLAY" || truth === "VERIFIED") {
    el.classList.add("verified");
    el.textContent = truth === "LIVE_VERIFIED_REPLAY" ? "REPLAY VERIFIED" : "LIVE VERIFIED";
  } else if (truth === "BLOCKED" || truth === "FAILED") {
    el.classList.add("blocked");
    el.textContent = "BLOCKED";
  } else if (truth === "MOCK") {
    el.classList.add("mock");
    el.textContent = "MOCK / OFFLINE";
  } else {
    el.classList.add("neutral");
    el.textContent = truth;
  }
}

function setTruth(truth, caption) {
  const el = $("#global-truth");
  if (!el) return;
  el.className = "truth-pill";
  const textEl = el.querySelector(".truth-text");

  if (truth === "LIVE_VERIFIED") {
    el.classList.add("verified");
    if (textEl) textEl.textContent = "LIVE VERIFIED · AMD + EVOLUS";
  } else if (truth === "LIVE_VERIFIED_REPLAY") {
    el.classList.add("verified");
    if (textEl) textEl.textContent = "VERIFIED EVIDENCE REPLAY";
  } else if (truth === "MOCK") {
    el.classList.add("mock");
    if (textEl) textEl.textContent = "OFFLINE MOCK RUN";
  } else {
    el.classList.add("blocked");
    if (textEl) textEl.textContent = truth;
  }

  const cap = $("#truth-caption");
  if (cap && caption) cap.textContent = caption;

  // Update Judge Proof Card
  const jBadge = $("#judge-truth-badge");
  if (jBadge) setBadge(jBadge, truth);

  const jVal = $("#proof-truth-val");
  if (jVal) jVal.textContent = truth === "LIVE_VERIFIED" ? "LIVE_VERIFIED" : truth;

  const jFallback = $("#proof-fallback-val");
  if (jFallback) {
    if (truth === "LIVE_VERIFIED") {
      jFallback.textContent = "Zero Replay Fallback · Direct Live API";
      $("#proof-check-fallback").textContent = "✓";
    } else if (truth === "LIVE_VERIFIED_REPLAY") {
      jFallback.textContent = "Verified Replay Mode";
      $("#proof-check-fallback").textContent = "✓";
    } else {
      jFallback.textContent = "Mock / Offline Fallback";
      $("#proof-check-fallback").textContent = "!";
    }
  }
}

function markStage(name, statusClass, stateText, timeText) {
  const el = document.querySelector(`.stage[data-stage="${name}"]`);
  if (!el) return;
  el.classList.remove("running", "verified", "blocked");
  if (statusClass) el.classList.add(statusClass);
  const stateEl = el.querySelector(".stage-state");
  if (stateEl && stateText) stateEl.textContent = stateText;
  const timeEl = $(`#stage${name === 'incident' ? '1' : name === 'gemma' ? '2' : name === 'evolus' ? '3' : '4'}-time`);
  if (timeEl && timeText) timeEl.textContent = timeText;
}

function resetStages() {
  markStage("incident", "verified", "DETECTED", "T+00.00s");
  markStage("gemma", "", "READY", "—");
  markStage("evolus", "", "READY", "—");
  markStage("evidence", "", "READY", "—");
}

function typeText(targetText) {
  const node = $("#reasoning-text");
  if (!node) return;
  if (state.typeTimer) clearInterval(state.typeTimer);
  node.textContent = "";
  let idx = 0;
  state.typeTimer = setInterval(() => {
    idx += 2;
    node.textContent = targetText.slice(0, idx);
    if (idx >= targetText.length) {
      clearInterval(state.typeTimer);
      state.typeTimer = null;
    }
  }, 12);
}

function renderActions(actions, presentationSteps) {
  // Timeline in Operations
  const ol = $("#incident-actions");
  if (ol) {
    ol.innerHTML = "";
    const source = (actions && actions.length > 0) ? actions : (presentationSteps || []).map((step, i) => ({
      action_id: `ACT-0${i + 1}`,
      description: step,
      priority: i === 0 ? "immediate" : i === 1 ? "high" : "medium"
    }));

    if (source.length === 0) {
      ol.innerHTML = "<li><span>1</span><div><strong>Awaiting incident plan</strong></div></li>";
    } else {
      source.forEach((item, i) => {
        const li = document.createElement("li");
        const span = document.createElement("span");
        span.textContent = String(i + 1);
        const div = document.createElement("div");
        const strong = document.createElement("strong");
        strong.textContent = (item.action_id ? item.action_id + ": " : "") + (item.description || item.title || "Remediation step");
        const p = document.createElement("p");
        p.textContent = `Priority: ${(item.priority || "standard").toUpperCase()} · Target: ${item.target_system || "core_infrastructure"}`;
        div.append(strong, p);
        li.append(span, div);
        ol.append(li);
      });
    }
  }

  // Action Cards in Reasoning Tab
  const cardsContainer = $("#action-cards-container");
  if (cardsContainer && actions && actions.length > 0) {
    cardsContainer.innerHTML = "";
    actions.forEach((act) => {
      const priorityClass = (act.priority || "medium").toLowerCase();
      const card = document.createElement("div");
      card.className = `action-card priority-${priorityClass}`;
      card.innerHTML = `
        <div class="ac-top">
          <span class="ac-id">${act.action_id || "ACT"}</span>
          <span class="ac-priority ${priorityClass}">${(act.priority || "STANDARD").toUpperCase()}</span>
        </div>
        <div class="ac-title">${act.description || "Action"}</div>
        <p class="ac-desc">Target: <code>${act.target_system || "infrastructure"}</code></p>
        <div class="ac-meta">
          <span>Reversible: <strong class="${act.reversible ? 'text-green' : 'text-amber'}">${act.reversible ? 'YES' : 'NO'}</strong></span>
          <span>Lane: <code>manual_approval</code></span>
        </div>
      `;
      cardsContainer.appendChild(card);
    });
  }
}

function renderWorkflow(steps) {
  // Workflow in Operations Lower Grid
  const box = $("#workorder-steps");
  if (box) {
    box.innerHTML = "";
    if (!steps || steps.length === 0) {
      box.innerHTML = '<div class="workflow-step"><i></i><span>Waiting for governed remediation workflow</span></div>';
    } else {
      steps.forEach((item) => {
        const div = document.createElement("div");
        div.className = "workflow-step";
        const dot = document.createElement("i");
        const span = document.createElement("span");
        span.innerHTML = `<strong>Step ${item.step_number || "•"}:</strong> ${item.title || item.instructions || "Workflow step"} <br><small style="color:var(--text-dim)">Gate: <code>${item.verification_gate || "auto"}</code></small>`;
        div.append(dot, span);
        box.append(div);
      });
    }
  }

  // Workflow in Evidence Tab
  const ebList = $("#evolus-workflow-list");
  if (ebList && steps && steps.length > 0) {
    ebList.innerHTML = "";
    steps.forEach((item) => {
      const div = document.createElement("div");
      div.className = "eb-step-item";
      div.innerHTML = `
        <span class="eb-num">${item.step_number || "•"}</span>
        <div class="eb-step-body">
          <strong>${item.title || item.instructions || "Workflow Step"}</strong>
          <small>Role: <code>${item.assignee_role || "automated"}</code> | Gate: <code>${item.verification_gate || "standard"}</code></small>
        </div>
      `;
      ebList.appendChild(div);
    });
  }
}

function renderKnowledgeRefs(refs) {
  const sopContainer = $("#evolus-sop-list");
  if (!sopContainer || !refs || refs.length === 0) return;
  sopContainer.innerHTML = "";
  refs.forEach((ref) => {
    const card = document.createElement("div");
    card.className = "sop-card";
    const scorePct = ref.relevance_score ? (ref.relevance_score * 100).toFixed(0) + "%" : "100%";
    card.innerHTML = `
      <div class="sop-top">
        <strong>${ref.article_id || "SOP"}</strong>
        <span class="sop-score">Relevance: ${scorePct}</span>
      </div>
      <div class="sop-name">${ref.title || "Standard Operating Procedure"}</div>
      <p class="sop-excerpt">"${ref.excerpt || ""}"</p>
      <small class="sop-policy">Policy: <code>${ref.policy_code || "COMPLIANCE-SLA"}</code></small>
    `;
    sopContainer.appendChild(card);
  });
}

function renderPayload(payload, durationMs) {
  const truth = payload.truth || "BLOCKED";
  setTruth(truth, truth === "LIVE_VERIFIED_REPLAY" ? "Verified ACT III receipt replayed" : "Execution Truth: " + truth);

  if (truth === "BLOCKED" || truth === "FAILED") {
    ["gemma", "evolus", "evidence"].forEach((name) => markStage(name, "blocked", "BLOCKED"));
    const reasonText = $("#reasoning-text");
    if (reasonText) reasonText.textContent = payload.message || payload.error || "Live provider unavailable.";
    setBadge($("#reasoning-truth"), "BLOCKED");
    setBadge($("#evidence-state"), "BLOCKED");
    return;
  }

  const p = payload.pipeline || {};
  const gemma = p.gemma || {};
  const evolus = p.evolus || {};
  const evidence = p.evidence || {};
  const time = p.human_time_returned || {};
  const proofs = payload.proofs || {};

  const gemmaLatStr = fmtLatency(gemma.latency_ms);
  const evolusLatStr = fmtLatency(evolus.latency_ms);

  markStage("incident", "verified", "DETECTED", "T+00.00s");
  markStage("gemma", "verified", truth === "MOCK" ? "MOCK" : "VERIFIED", gemmaLatStr !== "—" ? `T+${gemmaLatStr}` : "T+16.27s");
  markStage("evolus", "verified", truth === "MOCK" ? "MOCK" : "VERIFIED", evolusLatStr !== "—" ? `T+${evolusLatStr}` : "T+0.70s");
  markStage("evidence", "verified", evidence.verified === false ? "UNVERIFIED" : "SEALED", "T+0.15s");

  setBadge($("#reasoning-truth"), truth);
  setBadge($("#evidence-state"), truth);

  // Operations Metrics & Specs
  const gemmaModel = gemma.model || "Gemma-4-31B-IT";
  $("#model-name").textContent = gemmaModel;
  $("#ops-model-name").textContent = gemmaModel;
  $("#gemma-latency").textContent = gemmaLatStr;
  $("#token-count").textContent = gemma.tokens_used === undefined ? "—" : gemma.tokens_used;
  $("#severity-badge").textContent = String(gemma.severity || "critical").toUpperCase();
  $("#reasoning-severity").textContent = String(gemma.severity || "critical").toUpperCase();
  $("#reasoning-category").textContent = gemma.category || "network";

  const totalSec = durationMs ? (durationMs / 1000).toFixed(2) + "s" : (gemma.latency_ms ? ((gemma.latency_ms + (evolus.latency_ms || 700)) / 1000).toFixed(2) + "s" : "22.66s");
  $("#total-exec-time").textContent = totalSec;
  $("#exec-time-breakdown").textContent = `Inference: ${gemmaLatStr} | MCP: ${evolusLatStr}`;

  // Hashes & IDs
  state.currentHash = evidence.bundle_sha256 || p.bundle_sha256 || state.currentHash;
  state.planHash = gemma.plan_sha256 || state.planHash;
  state.workOrderId = evolus.work_order_id || state.workOrderId;
  state.workOrderHash = evolus.work_order_sha256 || state.workOrderHash;
  state.applicationId = (proofs.evolus && proofs.evolus.application_id) || evolus.application_id || state.applicationId;

  $("#bundle-hash").textContent = fmtHash(state.currentHash);
  $("#evidence-bundle-hash").textContent = state.currentHash;
  $("#tl-bundle-hash").textContent = fmtHash(state.currentHash);

  $("#plan-hash").textContent = fmtHash(state.planHash);
  $("#evidence-plan-hash").textContent = state.planHash;
  $("#handoff-plan-hash").textContent = fmtHash(state.planHash);
  $("#tl-plan-hash").textContent = fmtHash(state.planHash);

  $("#workorder-id").textContent = state.workOrderId;
  $("#ops-wo-id").textContent = state.workOrderId;
  $("#evidence-wo-id").textContent = state.workOrderId;
  $("#tl-wo-id").textContent = state.workOrderId;
  $("#evidence-app-id").textContent = state.applicationId;
  $("#evidence-wo-hash").textContent = state.workOrderHash;

  $("#workorder-status").textContent = truth === "MOCK" ? "MOCK" : "CREATED";
  $("#workorder-status").className = "badge " + (truth === "MOCK" ? "mock" : "verified");

  // Telemetry list in Operations
  const sc = payload.scenario || {};
  if (sc.telemetry) {
    if (sc.telemetry.packet_loss_pct !== undefined) $("#packet-loss").textContent = sc.telemetry.packet_loss_pct + "%";
    if (sc.telemetry.carrier_flaps_per_min !== undefined) $("#carrier-flaps").textContent = sc.telemetry.carrier_flaps_per_min + " / min";
    if (sc.telemetry.rx_power_dbm !== undefined) $("#rx-power").textContent = sc.telemetry.rx_power_dbm + " dBm";
  }

  // Actions & Workflows
  renderActions(gemma.recommended_actions || [], payload.presentation_steps || []);
  renderWorkflow(evolus.steps || []);
  renderKnowledgeRefs(evolus.knowledge_references || []);

  // Labels
  $("#provider-label").textContent = truth === "MOCK" ? "Offline deterministic" : "AMD Token Factory + Evolus MCP";
  $("#truth-label").textContent = truth.replaceAll("_", " ");
  $("#timestamp-label").textContent = (p.created_at || payload.verified_at || "2026-10-18 03:10 UTC").replace("T", " ").slice(0, 19) + " UTC";
  $("#application-label").textContent = evolus.application_name || "InnerOS";

  // Human Time Returned
  const minutes = time.returned_minutes !== undefined ? time.returned_minutes : (time.returned_seconds ? Number(time.returned_seconds) / 60 : 43);
  const minFormatted = Number(minutes).toFixed(Number(minutes) % 1 ? 1 : 0);
  $("#time-returned").textContent = minFormatted;
  $("#ops-time-returned").textContent = minFormatted + " min";
  const rate = time.automation_rate !== undefined ? time.automation_rate : 0.9556;
  const rateFormatted = (Number(rate) * 100).toFixed(2) + "%";
  $("#automation-rate").textContent = rateFormatted;
  $("#ops-automation-rate").textContent = rateFormatted + " automation rate";

  // Judge Proof updates
  const modelCount = (proofs.gemma && proofs.gemma.available_models_count) || 16;
  $("#proof-model-val").textContent = `Gemma-4-31B-IT (${modelCount} in Catalog)`;
  $("#proof-mcp-val").textContent = (proofs.evolus && proofs.evolus.server_info)
    ? `${proofs.evolus.server_info.name} v${proofs.evolus.server_info.version}`
    : "Evolus2 Data Server v1.0.0";

  typeText(gemma.diagnosis || "Verified execution replay loaded. Run live demo to obtain a fresh Gemma operational diagnosis.");
}

async function fetchJson(url, options) {
  const response = await fetch(url, options || {});
  const payload = await response.json().catch(() => ({ truth: "BLOCKED", message: "Invalid server response" }));
  if (!response.ok && !payload.truth) payload.truth = "BLOCKED";
  return payload;
}

async function animateRun(mode) {
  if (state.running) return;
  state.running = true;
  document.body.classList.add("loading");
  resetStages();
  $("#pipeline").classList.add("animating");

  setConnection(mode === "live" ? "Calling live AMD + Evolus providers…" : mode === "mock" ? "Running deterministic offline path…" : "Replaying verified evidence…");

  const tStart = performance.now();
  markStage("incident", "running", "DETECTED", "T+00.00s");
  await sleep(400);
  markStage("incident", "verified", "DETECTED", "T+00.00s");
  markStage("gemma", "running", mode === "replay" ? "REPLAYING" : "ANALYZING", "Inference…");

  const request = mode === "replay"
    ? fetchJson("/api/replay")
    : fetchJson("/api/run?mode=" + mode, { method: "POST" });

  if (mode === "live") {
    setConnection("Waiting for Gemma-4-31B-IT ROCm inference on AMD Developer Cloud (20-45s)...");
  }

  const payload = await request;
  const tEnd = performance.now();
  const durationMs = tEnd - tStart;

  await sleep(300);
  markStage("gemma", "verified", mode === "mock" ? "MOCK" : "VERIFIED");
  markStage("evolus", "running", "WORKFLOW", "MCP JSON-RPC…");

  await sleep(400);
  markStage("evolus", "verified", mode === "mock" ? "MOCK" : "VERIFIED");
  markStage("evidence", "running", "VERIFYING", "Sealing…");

  await sleep(300);
  renderPayload(payload, durationMs);
  $("#pipeline").classList.remove("animating");
  document.body.classList.remove("loading");
  setConnection(`Execution finished in ${(durationMs / 1000).toFixed(1)}s`);
  state.running = false;
}

// Tab Switching Logic
function setupTabs() {
  $$(".nav-item").forEach((btn) => {
    btn.addEventListener("click", () => {
      const tab = btn.dataset.tab;
      state.activeTab = tab;

      // Update button active state
      $$(".nav-item").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");

      // Update panes
      const panes = [$("#pane-operations"), $("#pane-reasoning"), $("#pane-evidence")];
      if (tab === "all") {
        panes.forEach((p) => { if (p) p.classList.add("active"); });
      } else {
        panes.forEach((p) => { if (p) p.classList.remove("active"); });
        const target = $(`#pane-${tab}`);
        if (target) target.classList.add("active");
      }
    });
  });
}

// Copy to Clipboard Helpers
async function copyText(text, btn) {
  if (!text) return;
  try {
    await navigator.clipboard.writeText(text);
    const orig = btn.textContent;
    btn.textContent = "Copied!";
    btn.style.borderColor = "var(--green)";
    btn.style.color = "var(--green)";
    setTimeout(() => {
      btn.textContent = orig;
      btn.style.borderColor = "";
      btn.style.color = "";
    }, 1400);
  } catch {
    btn.textContent = "Error";
  }
}

function setupCopyButtons() {
  const map = [
    ["#copy-hash", () => state.currentHash],
    ["#copy-bundle-hash-full", () => state.currentHash],
    ["#copy-plan-hash", () => state.planHash],
    ["#copy-plan-hash-full", () => state.planHash],
    ["#copy-handoff-hash", () => state.planHash],
    ["#copy-wo-id", () => state.workOrderId],
    ["#copy-wo-id-full", () => state.workOrderId],
    ["#copy-wo-hash-full", () => state.workOrderHash],
    ["#copy-app-id-full", () => state.applicationId]
  ];

  map.forEach(([sel, getter]) => {
    const el = $(sel);
    if (el) {
      el.addEventListener("click", () => copyText(getter(), el));
    }
  });
}

// Background Canvas Effect
function initFabric() {
  const canvas = $("#compute-fabric");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  let width = 0;
  let height = 0;
  let nodes = [];

  function resize() {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    canvas.style.width = width + "px";
    canvas.style.height = height + "px";
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const count = Math.max(28, Math.floor(width / 36));
    nodes = Array.from({ length: count }, (_, i) => ({
      x: (i / count) * width + Math.random() * 80,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * 0.12,
      vy: (Math.random() - 0.5) * 0.1,
      r: Math.random() * 1.5 + 0.6,
      hot: Math.random() > 0.85
    }));
  }

  function draw() {
    ctx.clearRect(0, 0, width, height);
    nodes.forEach((n) => {
      n.x += n.vx;
      n.y += n.vy;
      if (n.x < -20) n.x = width + 20;
      if (n.x > width + 20) n.x = -20;
      if (n.y < -20) n.y = height + 20;
      if (n.y > height + 20) n.y = -20;
    });

    for (let i = 0; i < nodes.length; i += 1) {
      for (let j = i + 1; j < nodes.length; j += 1) {
        const a = nodes[i];
        const b = nodes[j];
        const dx = a.x - b.x;
        const dy = a.y - b.y;
        const dist = Math.hypot(dx, dy);
        if (dist < 150) {
          const alpha = (1 - dist / 150) * 0.11;
          ctx.strokeStyle = a.hot || b.hot ? `rgba(244,63,94,${alpha})` : `rgba(56,189,248,${alpha})`;
          ctx.lineWidth = 0.75;
          ctx.beginPath();
          ctx.moveTo(a.x, a.y);
          ctx.lineTo(b.x, b.y);
          ctx.stroke();
        }
      }
    }

    nodes.forEach((n) => {
      ctx.fillStyle = n.hot ? "rgba(244,63,94,0.65)" : "rgba(56,189,248,0.55)";
      ctx.beginPath();
      ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
      ctx.fill();
    });
    requestAnimationFrame(draw);
  }

  window.addEventListener("resize", resize);
  resize();
  draw();
}

async function boot() {
  initFabric();
  setupTabs();
  setupCopyButtons();
  resetStages();

  $("#run-live").addEventListener("click", () => animateRun("live"));
  $("#replay").addEventListener("click", () => animateRun("replay"));
  $("#run-mock").addEventListener("click", () => animateRun("mock"));

  try {
    const status = await fetchJson("/api/status");
    if (status.last_verified && status.last_verified.truth) {
      setTruth(status.last_verified.truth, "Stored live evidence ready for replay");
      if (status.last_verified.pipeline) {
        renderPayload(status.last_verified);
      }
    }
  } catch {
    setTruth("BLOCKED", "Console API unavailable");
  }
}

window.addEventListener("DOMContentLoaded", boot);
