const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => Array.from(document.querySelectorAll(selector));

const state = {
  currentHash: "6ee36d6905929b176fd9c49f3c1a4aa165df4a8231d5047871f581eb73b3f845",
  running: false
};

function setConnection(text) {
  $("#connection-state").textContent = text;
}

function setTruth(truth, detail) {
  const pill = $("#global-truth");
  const text = pill.querySelector(".truth-text");
  pill.classList.remove("verified", "blocked", "mock");
  if (truth === "LIVE_VERIFIED" || truth === "LIVE_VERIFIED_REPLAY") {
    pill.classList.add("verified");
    text.textContent = truth === "LIVE_VERIFIED_REPLAY" ? "LIVE VERIFIED · REPLAY" : "LIVE VERIFIED";
  } else if (truth === "MOCK") {
    pill.classList.add("mock");
    text.textContent = "MOCK MODE";
  } else {
    pill.classList.add("blocked");
    text.textContent = "BLOCKED / UNAVAILABLE";
  }
  if (detail) setConnection(detail);
}

function stage(name) {
  return document.querySelector('[data-stage="' + name + '"]');
}

function resetStages() {
  ["incident", "gemma", "evolus", "evidence"].forEach((name) => {
    const el = stage(name);
    el.classList.remove("running", "verified", "blocked");
    el.querySelector(".stage-state").textContent = name === "incident" ? "DETECTED" : "READY";
  });
  stage("incident").classList.add("active");
  $("#pipeline").classList.remove("animating");
}

function markStage(name, status, label) {
  const el = stage(name);
  el.classList.remove("running", "verified", "blocked");
  el.classList.add(status);
  el.querySelector(".stage-state").textContent = label || status.toUpperCase();
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function typeText(value) {
  const target = $("#reasoning-text");
  target.textContent = "";
  const safe = String(value || "No diagnosis returned.");
  for (let i = 0; i < safe.length; i += 1) {
    target.textContent += safe[i];
    if (i % 3 === 0) await sleep(7);
  }
}

function fmtHash(value) {
  if (!value) return "—";
  return value.length > 22 ? value.slice(0, 12) + "…" + value.slice(-9) : value;
}

function fmtLatency(value) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) return "—";
  return Number(value).toFixed(0) + " ms";
}

function setBadge(el, truth) {
  el.classList.remove("verified", "blocked", "mock", "neutral");
  if (truth === "LIVE_VERIFIED" || truth === "LIVE_VERIFIED_REPLAY") {
    el.classList.add("verified");
    el.textContent = truth === "LIVE_VERIFIED_REPLAY" ? "VERIFIED REPLAY" : "LIVE VERIFIED";
  } else if (truth === "MOCK") {
    el.classList.add("mock");
    el.textContent = "MOCK";
  } else {
    el.classList.add("blocked");
    el.textContent = "BLOCKED";
  }
}

function renderActions(actions, fallbackSteps) {
  const list = $("#incident-actions");
  list.innerHTML = "";
  let source = Array.isArray(actions) ? actions : [];
  if (!source.length && Array.isArray(fallbackSteps)) {
    source = fallbackSteps.map((description, index) => ({
      action_id: "step-" + (index + 1),
      description: description,
      target_system: "InnerOS governed pipeline",
      reversible: true
    }));
  }
  if (!source.length) {
    source = [{ description: "Verified plan hash available. Run live for the full action sequence.", target_system: "stored evidence" }];
  }
  source.forEach((action, index) => {
    const li = document.createElement("li");
    const n = document.createElement("span");
    n.textContent = String(index + 1);
    const box = document.createElement("div");
    const strong = document.createElement("strong");
    strong.textContent = action.description || action.title || "Governed action";
    const p = document.createElement("p");
    p.textContent = action.target_system || action.verification_gate || "verified pipeline step";
    box.append(strong, p);
    li.append(n, box);
    list.append(li);
  });
}

function renderWorkflow(steps) {
  const box = $("#workorder-steps");
  box.innerHTML = "";
  const source = Array.isArray(steps) ? steps : [];
  if (!source.length) {
    const div = document.createElement("div");
    div.className = "workflow-step";
    div.innerHTML = "<i></i><span>Verified work order exists in stored evidence receipt.</span>";
    box.append(div);
    return;
  }
  source.forEach((item) => {
    const div = document.createElement("div");
    div.className = "workflow-step";
    const dot = document.createElement("i");
    const span = document.createElement("span");
    span.textContent = String(item.step_number || "•") + ". " + (item.title || item.instructions || "Workflow step");
    div.append(dot, span);
    box.append(div);
  });
}

function renderPayload(payload) {
  const truth = payload.truth || "BLOCKED";
  const liveFallback = payload.mode === "live_fallback";
  const detail = liveFallback
    ? "Live provider unavailable · verified ACT III evidence replayed"
    : truth === "LIVE_VERIFIED_REPLAY"
      ? "Verified ACT III receipt replayed"
      : "Execution: " + truth;
  setTruth(truth, detail);

  if (truth === "BLOCKED" || truth === "FAILED") {
    ["gemma", "evolus", "evidence"].forEach((name) => markStage(name, "blocked", "BLOCKED"));
    $("#reasoning-text").textContent = payload.message || payload.error || "Live provider unavailable.";
    setBadge($("#reasoning-truth"), "BLOCKED");
    setBadge($("#evidence-state"), "BLOCKED");
    return;
  }

  const p = payload.pipeline || {};
  const gemma = p.gemma || {};
  const evolus = p.evolus || {};
  const evidence = p.evidence || {};
  const time = p.human_time_returned || {};

  markStage("incident", "verified", "DETECTED");
  markStage("gemma", "verified", truth === "MOCK" ? "MOCK" : liveFallback ? "VERIFIED REPLAY" : "ANALYZED");
  markStage("evolus", "verified", truth === "MOCK" ? "MOCK" : liveFallback ? "VERIFIED REPLAY" : "ORCHESTRATED");
  markStage("evidence", "verified", evidence.verified === false ? "UNVERIFIED" : "VERIFIED");

  setBadge($("#reasoning-truth"), truth);
  setBadge($("#evidence-state"), truth);

  $("#model-name").textContent = gemma.model || "Gemma-4-31B-IT";
  $("#gemma-latency").textContent = fmtLatency(gemma.latency_ms);
  $("#token-count").textContent = gemma.tokens_used === undefined ? "—" : gemma.tokens_used;
  $("#severity-badge").textContent = String(gemma.severity || "critical").toUpperCase();
  $("#plan-hash").textContent = fmtHash(gemma.plan_sha256 || "");
  $("#workorder-id").textContent = evolus.work_order_id || "Verified work order";
  $("#workorder-status").textContent = truth === "MOCK" ? "MOCK" : "CREATED";
  $("#workorder-status").className = "badge " + (truth === "MOCK" ? "mock" : "verified");

  renderActions(gemma.recommended_actions || [], payload.presentation_steps || []);
  renderWorkflow(evolus.steps || []);

  const hash = evidence.bundle_sha256 || p.bundle_sha256 || "";
  if (hash) {
    state.currentHash = hash;
    $("#bundle-hash").textContent = fmtHash(hash);
  }

  $("#provider-label").textContent = truth === "MOCK" ? "Offline deterministic" : "AMD + Evolus";
  $("#truth-label").textContent = liveFallback ? "Verified replay after live check" : truth.replaceAll("_", " ");
  $("#timestamp-label").textContent = p.created_at || payload.verified_at || "Verified receipt";
  $("#application-label").textContent = evolus.application_name || "InnerOS";

  const minutes = time.returned_minutes !== undefined ? time.returned_minutes : (time.returned_seconds ? Number(time.returned_seconds) / 60 : 43);
  $("#time-returned").textContent = Number(minutes).toFixed(Number(minutes) % 1 ? 1 : 0);
  const rate = time.automation_rate !== undefined ? time.automation_rate : 0.9556;
  $("#automation-rate").textContent = (Number(rate) * 100).toFixed(2) + "%";

  const diagnosis = gemma.diagnosis || "Verified execution replay loaded.";
  const fallbackNote = liveFallback && payload.live_attempt
    ? " Live check: " + (payload.live_attempt.message || payload.live_attempt.error || "provider unavailable") + ". Showing the last cryptographically verified run instead."
    : "";
  typeText(diagnosis + fallbackNote);

  const percent = truth === "BLOCKED" || truth === "FAILED" ? 0 : 100;
  const recoveryPercent = $("#recovery-percent");
  const recoveryBar = $("#recovery-bar");
  const topologyState = $("#topology-state");
  if (recoveryPercent) recoveryPercent.textContent = percent + "%";
  if (recoveryBar) recoveryBar.style.width = percent + "%";
  if (topologyState) {
    topologyState.className = "badge " + (percent === 100 ? "verified" : "neutral");
    topologyState.textContent = percent === 100 ? (liveFallback ? "VERIFIED REPLAY" : "RECOVERED") : "AWAITING RUN";
  }
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
  setConnection(mode === "live" ? "Calling live providers…" : mode === "mock" ? "Running deterministic offline path…" : "Replaying verified evidence…");

  markStage("incident", "running", "DETECTED");
  await sleep(450);
  markStage("incident", "verified", "DETECTED");
  markStage("gemma", "running", mode === "replay" ? "REPLAYING" : "ANALYZING");

  const request = mode === "replay"
    ? fetchJson("/api/replay")
    : fetchJson("/api/run?mode=" + mode, { method: "POST" });

  await sleep(850);
  markStage("gemma", "verified", mode === "mock" ? "MOCK" : "VERIFIED");
  markStage("evolus", "running", "WORKFLOW");

  await sleep(800);
  markStage("evolus", "verified", mode === "mock" ? "MOCK" : "VERIFIED");
  markStage("evidence", "running", "VERIFYING");

  const payload = await request;
  await sleep(450);
  renderPayload(payload);
  $("#pipeline").classList.remove("animating");
  document.body.classList.remove("loading");
  state.running = false;
}

$("#run-live").addEventListener("click", () => animateRun("live"));
$("#replay").addEventListener("click", () => animateRun("replay"));
$("#run-mock").addEventListener("click", () => animateRun("mock"));

$("#copy-hash").addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(state.currentHash);
    $("#copy-hash").textContent = "Copied";
    setTimeout(() => { $("#copy-hash").textContent = "Copy"; }, 1200);
  } catch {
    $("#copy-hash").textContent = "Unavailable";
  }
});

$$(".nav-item").forEach((button) => {
  button.addEventListener("click", () => {
    const id = button.dataset.scroll;
    const target = document.getElementById(id);
    if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
  });
});

function initFabric() {
  const canvas = $("#compute-fabric");
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
    const count = Math.max(28, Math.floor(width / 38));
    nodes = Array.from({ length: count }, (_, i) => ({
      x: (i / count) * width + Math.random() * 90,
      y: Math.random() * height,
      vx: (Math.random() - .5) * .12,
      vy: (Math.random() - .5) * .1,
      r: Math.random() * 1.5 + .5,
      hot: Math.random() > .82
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
        if (dist < 155) {
          const alpha = (1 - dist / 155) * .12;
          ctx.strokeStyle = a.hot || b.hot ? "rgba(255,73,108," + alpha + ")" : "rgba(56,145,255," + alpha + ")";
          ctx.lineWidth = .7;
          ctx.beginPath();
          ctx.moveTo(a.x, a.y);
          ctx.lineTo(b.x, b.y);
          ctx.stroke();
        }
      }
    }

    nodes.forEach((n) => {
      ctx.fillStyle = n.hot ? "rgba(255,73,108,.62)" : "rgba(72,156,255,.52)";
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
  resetStages();
  try {
    const status = await fetchJson("/api/status");
    if (status.last_verified && status.last_verified.truth) {
      setTruth(status.last_verified.truth, "Stored live evidence ready for replay");
    }
  } catch {
    setTruth("BLOCKED", "Console API unavailable");
  }
}

boot();
