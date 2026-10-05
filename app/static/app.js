"use strict";
// ASA-Astro V1 thin slice UI. Renders only what the API returns; never builds HTML from data (textContent only).
const $ = (sel) => document.querySelector(sel);
const el = (tag, opts = {}, ...kids) => {
  const n = document.createElement(tag);
  if (opts.cls) n.className = opts.cls;
  if (opts.text !== undefined) n.textContent = String(opts.text);
  if (opts.href) n.href = opts.href;
  if (opts.attrs) for (const [k, v] of Object.entries(opts.attrs)) n.setAttribute(k, v);
  for (const k of kids) if (k) n.append(k);
  return n;
};
let current = null;
const status = (msg) => { $("#status").textContent = msg; };

async function api(path, init) {
  const r = await fetch(path, init);
  const body = await r.json().catch(() => ({ error: `HTTP ${r.status}` }));
  if (!r.ok) throw new Error(body.error || `HTTP ${r.status}`);
  return body;
}

function kv(dl, rows) {
  dl.replaceChildren();
  for (const [k, v] of rows) { dl.append(el("dt", { text: k }), el("dd", { text: v ?? "— (field absent)" })); }
}

function badge(label) { return el("span", { cls: `badge ${label}`, text: label }); }

function srcLink(runId, ref) {
  if (!ref || !runId) return null;
  const href = `/api/runs/${encodeURIComponent(runId)}/artifacts/${encodeURIComponent(ref.artifact)}`;
  return el("a", { cls: "src", href, text: `source: ${ref.artifact}#${ref.pointer || "/"}`,
    attrs: { "aria-label": `Open source field ${ref.pointer || "/"} in ${ref.artifact}` } });
}

function citedList(ul, items, runId, fmt) {
  ul.replaceChildren();
  if (!items.length) { ul.append(el("li", { text: "None recorded in this run." })); return; }
  for (const it of items) ul.append(fmt(it, runId));
}

async function loadPin() {
  try {
    const p = await api("/api/pin");
    kv($("#pin-dl"), [
      ["Pinned SHA", p.pinned_sha], ["Ref", p.pinned_ref], ["Pin file", p.pin_file], ["Pin kind", p.pin_kind],
      ["Declared status", p.pin_status_declared], ["Kernel (reported)", `${p.kernel_version_reported_by_kernel} — ${p.kernel_status_reported_by_kernel}`],
      ["Kernel (pin file declares)", p.pin_kernel_version_declared], ["Historical pin kept", p.historical_sha_preserved],
      ["Verification", `${p.verify_receipt && p.verify_receipt.status ? p.verify_receipt.status : "verified"} by ${p.verified_by}`],
    ]);
    markStage("pin", true);
  } catch (e) {
    kv($("#pin-dl"), [["Status", `NOT VERIFIED: ${e.message}`]]);
    markStage("pin", false);
  }
}

async function loadObjectives() {
  const o = await api("/api/objectives");
  const fill = (sel) => {
    if (!sel) return;
    sel.replaceChildren();
    for (const ob of o.objectives) {
      const opt = el("option", { text: `${ob.name} (${ob.slug})`, attrs: { value: ob.slug } });
      if (ob.slug === o.default) opt.selected = true;
      sel.append(opt);
    }
  };
  const sel = $("#objective");
  fill(sel);
  fill($("#upload-objective"));
  const describe = () => { const ob = o.objectives.find((x) => x.slug === sel.value); $("#objective-q").textContent = ob ? `${ob.question} — authority: ${ob.authority}` : ""; };
  sel.addEventListener("change", describe); describe();
}

function markStage(stage, ok) {
  const li = document.querySelector(`#stages li[data-stage="${stage}"]`);
  if (!li) return;
  li.classList.remove("done", "failed");
  if (ok === true) li.classList.add("done"); else if (ok === false) li.classList.add("failed");
}

function render(v) {
  current = v;
  const id = v.run_id;
  markStage("pin", !!v.pin.pinned_sha);
  markStage("snapshot", !!v.snapshot.summary.digest);
  markStage("objective", !!v.receipt.evaluation_id);
  markStage("receipt", !!v.receipt.receipt_id);
  const s = v.snapshot.summary, u = v.snapshot.universe;
  kv($("#snap-dl"), [["Kernel digest", s.digest], ["Head", s.head], ["Stream / seq", `${s.stream} / ${s.seq}`], ["Registry digest", s.registry_digest],
    ["ASA baseline", s.asa_baseline], ["Kernel version", s.kernel_version], ["Edges / evidence links / states", `${s.edges} / ${s.evidence_links} / ${s.states}`],
    ["Universe", `${u.universe_id} (data class: ${u.data_class})`]]);
  const r = v.receipt;
  const oid = v.observation_identity;
  const oidLine = oid
    ? (oid.digest || ["source=" + (oid.source_sha256 || "?"), "meta=" + (oid.metadata_sha256 != null ? oid.metadata_sha256 : "none"), "wcs=" + (oid.wcs_digest != null ? oid.wcs_digest : "absent")].join(" · "))
    : (v.uploaded_source && v.uploaded_source.present ? "pending pipeline observation_identity — do not cite bare RCPT for observation artefacts" : "— (no upload)");
  kv($("#rcpt-dl"), [
    ["Run storage key (run_id)", id],
    ["Observation claim identity", oidLine],
    ["Objective receipt digest (shared across keyed uploads is intentional)", r.receipt_id],
    ["Digest verified by app", String(r.receipt_id_verified)], ["receipt.json sha256", r.receipt_file_sha256],
    ["Schema", r.receipt_schema], ["Objective", `${v.objective.name} v${v.objective.version} (${v.objective.objective_id})`],
    ["Weighting policy", v.objective.weighting_policy_ref], ["Context", `${v.objective.context_label} (${v.objective.context_id})`],
    ["Evaluation / plan", `${r.evaluation_id} / ${r.plan_id}`], ["Astro commit", r.astro_commit],
    ["Issued at", `${r.issued_at} (${r.issued_at_classification})`], ["Reproduced earlier receipt", String(!!v.reproduced)]]);
  const links = $("#rcpt-links"); links.replaceChildren(el("span", { text: "Raw artifacts: " }));
  for (const a of ["receipt.json", "receipt.sha256", "snapshot.json", "evaluation.json", "plan.json", "objective.json", "context.json", "pin.json", "run.json"]) {
    links.append(el("a", { href: `/api/runs/${encodeURIComponent(id)}/artifacts/${a}`, text: a }), document.createTextNode(" "));
  }
  const sh = $("#shims"); sh.replaceChildren();
  if (v.compat_shims && v.compat_shims.length) {
    sh.hidden = false;
    for (const x of v.compat_shims) sh.append(el("p", { text: `Compatibility shim applied — ${x.id}: ${x.status}. ${x.reason}. Effect: ${x.effect}.` }));
  }
  citedList($("#exp-summary"), v.explanation.summary, id, (it) => el("li", { text: it.text }, srcLink(id, it.source)));
  const ents = $("#exp-entities"); ents.replaceChildren();
  for (const e of v.explanation.per_entity) {
    const box = el("div", { cls: "entity" }, el("h3", { text: `${e.designation} — ${e.status}, rank ${e.rank ?? "–"}, score ${e.score ?? "–"} ` }, badge(e.label)));
    const why = el("ul"); for (const w of e.why_significant_now) why.append(el("li", { text: w }));
    const not = el("ul"); for (const w of (e.why_not_more.length ? e.why_not_more : ["(no limiting factor recorded)"])) not.append(el("li", { text: w }));
    box.append(el("p", { text: "Why it scores now:" }), why, el("p", { text: "Why not more:" }), not, srcLink(id, e.source));
    ents.append(box);
  }
  const tb = $("#results-table tbody"); tb.replaceChildren();
  for (const x of v.results) {
    tb.append(el("tr", {}, el("th", { text: x.designation, attrs: { scope: "row" } }), el("td", { text: x.kind }), el("td", { text: x.status }),
      el("td", { text: x.rank ?? "–" }), el("td", { text: x.score ?? "–" }), el("td", { text: x.failed_rules.join("; ") || "–" }), el("td", {}, srcLink(id, x.source))));
  }
  const pol = $("#policy-dl"); kv(pol, Object.entries(v.label_policy).filter(([k]) => k !== "id"));
  $("#claim-counts").textContent = `Established in ASA state: ${v.claim_counts["established-in-ASA-state"]} · Hypothesis: ${v.claim_counts.hypothesis}`;
  renderClaims();
  citedList($("#unknowns-list"), v.unknowns, id, (it) => el("li", {}, badge("unknown"), document.createTextNode(` ${it.text}`), srcLink(id, it.source)));
  renderSource(v);
  renderObservation(v);
  renderAction(v);
  citedList($("#next-list"), v.next_evidence, id, (it) => el("li", {}, badge(it.label), document.createTextNode(` ${it.text}`), srcLink(id, it.source)));
}

function obsSrc(ref) {
  if (!ref) return null;
  const bits = [`schema: ${ref.schema}`];
  if (ref.record_id) bits.push(`id=${ref.record_id}`);
  if (ref.source_reference) bits.push(`source_reference=${ref.source_reference}`);
  if (ref.catalogue_provenance) {
    const p = ref.catalogue_provenance;
    bits.push(`catalogue=${p.catalogue_name || "?"}@${p.release || "?"}`);
  }
  if (ref.inference_basis && ref.inference_basis.length) bits.push(`basis=${ref.inference_basis.join(",")}`);
  return el("span", { cls: "src", text: `source: ${bits.join(" · ")}` });
}

function renderObservation(v) {
  const sec = $("#observation");
  const oe = v.observation_evidence;
  if (!oe || !oe.present) {
    sec.hidden = true;
    return;
  }
  sec.hidden = false;
  $("#obs-gap").textContent = oe.contract_note || "";
  const wcsBox = $("#obs-wcs");
  wcsBox.replaceChildren();
  if (oe.wcs) {
    wcsBox.append(
      el("p", {}, badge(oe.wcs.label || "record"), document.createTextNode(` ${oe.wcs.text}`), obsSrc(oe.wcs.source))
    );
  } else {
    wcsBox.append(el("p", { cls: "help", text: "No WCS (field absent — not invented)." }));
  }
  citedList($("#obs-loc-list"), oe.localisations || [], null, (it) => {
    const li = el("li", {}, badge(it.classification_status || it.label), document.createTextNode(` [${it.status}] ${it.text}`));
    li.append(obsSrc(it.source));
    return li;
  });
  citedList($("#obs-xm-list"), oe.crossmatches || [], null, (it) => {
    const li = el("li", {}, badge(it.classification_status || it.label),
      document.createTextNode(` [${it.resolution_state}] ${it.text}`));
    li.append(obsSrc(it.source));
    return li;
  });
}

function renderClaims() {
  if (!current) return;
  const q = $("#claim-filter").value.trim().toLowerCase();
  const items = current.claims.filter((c) => !q || `${c.group} ${c.text} ${c.label}`.toLowerCase().includes(q));
  citedList($("#claims-list"), items, current.run_id, (c) => el("li", {}, badge(c.label), document.createTextNode(` [${c.group}] ${c.text}`),
    c.reasons.length ? el("span", { cls: "reasons", text: `why ${c.label}: ${c.reasons.join("; ")}` }) : null, srcLink(current.run_id, c.source)));
}


/** U-RUN-LIST-01: never truncate before __src-/__meta-; show filename + short discriminators. */
function formatRunDiscriminators(r) {
  const bits = [];
  if (r.original_filename) bits.push(r.original_filename);
  if (r.source_sha256_short) bits.push("__src-" + r.source_sha256_short + "\u2026");
  else if (r.run_id && r.run_id.includes("__src-")) {
    const m = r.run_id.match(/__src-([0-9a-f]{12})/);
    if (m) bits.push("__src-" + m[1] + "\u2026");
  }
  if (r.meta_sha256_short) bits.push("__meta-" + r.meta_sha256_short + "\u2026");
  else if (r.meta_sha256 === "none" || (r.run_id && /__meta-none$/.test(r.run_id))) bits.push("__meta-none");
  else if (r.run_id && r.run_id.includes("__meta-")) {
    const m = r.run_id.match(/__meta-([0-9a-f]{12}|none)/);
    if (m) bits.push(m[1] === "none" ? "__meta-none" : "__meta-" + m[1] + "\u2026");
  }
  if (r.wcs_declared) bits.push("WCS declared");
  return bits.length ? bits.join(" \u00b7 ") : null;
}

function observationClaimLabel(r, v) {
  const oid = (v && v.observation_identity) || r.observation_identity;
  if (!oid) return null;
  if (oid.digest) return "observation_identity " + oid.digest;
  if (oid.source_sha256) {
    const meta = oid.metadata_sha256 != null ? String(oid.metadata_sha256) : "none";
    const wcs = oid.wcs_digest != null ? String(oid.wcs_digest) : "absent";
    return "source " + String(oid.source_sha256).slice(0, 12) + "\u2026 \u00b7 meta " + meta.slice(0, 12) + " \u00b7 wcs " + wcs.slice(0, 12);
  }
  return null;
}

async function loadRuns(q = "") {
  const data = await api(`/api/runs?q=${encodeURIComponent(q)}`);
  const ul = $("#runs-list"); ul.replaceChildren();
  if (!data.runs.length) { ul.append(el("li", { text: q ? `No runs match “${q}”.` : "No runs yet." })); return; }
  for (const r of data.runs) {
    const disc = formatRunDiscriminators(r);
    const title = disc ? `${r.objective} — ${disc}` : `${r.objective} — ${r.run_id}`;
    const a = el("a", { href: `#run-${r.run_id}`, cls: "run-title", text: title });
    a.addEventListener("click", async (ev) => {
      ev.preventDefault();
      render(await api(`/api/runs/${encodeURIComponent(r.run_id)}`));
      status(`Loaded run_id ${r.run_id}` + (r.receipt_id ? ` (Objective receipt_id ${r.receipt_id}; shared RCPT across keyed uploads is intentional).` : "."));
      $("#receipt").scrollIntoView();
    });
    const kids = [a];
    if (disc) kids.push(el("span", { cls: "run-disc", text: disc }));
    kids.push(el("span", { cls: "run-id", text: `run_id ${r.run_id}` }));
    const claim = observationClaimLabel(r);
    if (claim) kids.push(el("span", { cls: "run-disc", text: `observation claim: ${claim}` }));
    else if (r.keyed_upload) kids.push(el("span", { cls: "src", text: " observation claim: pending pipeline observation_identity (do not cite bare RCPT)" }));
    const rcptShort = r.receipt_id ? `${r.receipt_id.slice(0, 21)}…` : "—";
    kids.push(el("span", { cls: "src", text: ` ${r.issued_at} · data ${r.data_class} · Objective receipt ${rcptShort} · kernel ${r.kernel_digest.slice(0, 19)}…` }));
    ul.append(el("li", {}, ...kids));
  }
}

async function onRun(ev) {
  ev.preventDefault();
  const btn = $("#run-btn"); btn.disabled = true;
  for (const s of ["snapshot", "objective", "receipt"]) markStage(s, null);
  status("Running: verifying pin, loading universe into the pinned kernel, taking snapshot, evaluating one Objective, issuing receipt…");
  try {
    const v = await api("/api/runs", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ objective: $("#objective").value }) });
    render(v);
    status(`Done. Receipt ${v.receipt.receipt_id}${v.reproduced ? " (identical to an earlier run)" : ""}.`);
    await loadRuns($("#q").value);
  } catch (e) {
    status(`Run failed: ${e.message}`);
    markStage("receipt", false);
  } finally { btn.disabled = false; }
}


function renderSource(v) {
  const sec = $("#source");
  const us = v.uploaded_source;
  if (!us || !us.present) { sec.hidden = true; return; }
  sec.hidden = false;
  kv($("#src-dl"), [
    ["Original filename", us.original_filename],
    ["SHA-256", us.sha256],
    ["Byte size", String(us.byte_size)],
    ["Media type", us.media_type],
    ["Stored path", us.stored_path],
    ["Integrity", us.integrity_status],
    ["Registration", us.registration_policy],
    ["process_observation invoked", String(!!us.process_observation_invoked)],
    ["Observation bundle", us.observation_bundle_path || "—"],
    ["Bundle source verified", String(us.bundle_source_sha256_verified)],
  ]);
  $("#src-bridge").textContent = us.objective_bridge || us.process_observation_reason || "";
  // Also link uploaded_source.json artifact
  const links = $("#rcpt-links");
  if (links && v.run_id) {
    const a = el("a", { href: `/api/runs/${encodeURIComponent(v.run_id)}/artifacts/uploaded_source.json`, text: "uploaded_source.json" });
    links.append(document.createTextNode(" "), a);
  }
}

function renderAction(v) {
  const sec = $("#action");
  const ove = v.observed_vs_expected;
  if (!ove || !ove.present) { sec.hidden = true; return; }
  sec.hidden = false;
  const head = $("#act-headline");
  if (ove.action_ui && ove.action_ui.headline) {
    head.hidden = false;
    head.textContent = ove.action_ui.headline
      + (ove.action_ui.honesty ? ` — honesty: hypothesis_only=${ove.action_ui.honesty.hypothesis_only}; established_promoted=${ove.action_ui.honesty.established_identity_promoted}; coords_invented=${ove.action_ui.honesty.coordinates_invented}` : "");
  } else { head.hidden = true; }
  citedList($("#act-residuals"), ove.residuals || [], v.run_id, (it) =>
    el("li", {}, badge(it.label || "hypothesis"), document.createTextNode(` [${it.status}] ${it.plain_language_short || it.plain_language || ""}`), srcLink(v.run_id, it.source)));
  citedList($("#act-missing"), ove.missing_expected || [], v.run_id, (it) =>
    el("li", {}, badge(it.label || "hypothesis"), document.createTextNode(` ${it.plain_language_short || it.plain_language || it.catalogue_id || ""}`), srcLink(v.run_id, it.source)));
  citedList($("#act-recs"), ove.next_evidence_recommendations || [], v.run_id, (it) =>
    el("li", {}, badge(it.label || "hypothesis"), document.createTextNode(` [${it.code || "?"}] ${it.plain_language || ""}`), srcLink(v.run_id, it.source)));
}

async function onUpload(ev) {
  ev.preventDefault();
  const btn = $("#upload-btn"); btn.disabled = true;
  const statusEl = $("#upload-status");
  const fileInput = $("#source-file");
  if (!fileInput.files || !fileInput.files[0]) {
    statusEl.textContent = "Choose an observation source file first.";
    btn.disabled = false;
    return;
  }
  for (const s of ["snapshot", "objective", "receipt"]) markStage(s, null);
  statusEl.textContent = "Uploading: preserving source, optional process_observation, thin Objective path…";
  try {
    const fd = new FormData();
    fd.append("source", fileInput.files[0], fileInput.files[0].name);
    const meta = $("#meta-file");
    if (meta.files && meta.files[0]) fd.append("metadata", meta.files[0], meta.files[0].name);
    fd.append("objective", $("#upload-objective").value || $("#objective").value);
    const r = await fetch("/api/runs", { method: "POST", body: fd });
    const body = await r.json().catch(() => ({ error: `HTTP ${r.status}` }));
    if (!r.ok) throw new Error(body.error || `HTTP ${r.status}`);
    render(body);
    const oid = body.observation_identity;
    const oidBit = oid
      ? (oid.digest ? `; observation_identity=${oid.digest}` : `; observation_identity source=${oid.source_sha256 || "?"} meta=${oid.metadata_sha256 != null ? oid.metadata_sha256 : "none"}`)
      : "; observation_identity=pending (do not cite bare RCPT for observation)";
    statusEl.textContent = `Done. run_id=${body.run_id}; Objective receipt_id=${body.receipt.receipt_id}`
      + " (shared receipt_id across keyed uploads is intentional — thin Objective receipt is content-addressed; run_id isolates upload dirs)"
      + oidBit
      + (body.uploaded_source && body.uploaded_source.present ? `; source sha256=${body.uploaded_source.sha256}` : "")
      + (body.observation_evidence && body.observation_evidence.present ? "; observation_evidence.present=true" : "; observation_evidence.present=false")
      + (body.reproduced ? " (identical Objective receipt id reproduced)" : "");
    await loadRuns($("#q").value);
    $("#receipt").scrollIntoView();
  } catch (e) {
    statusEl.textContent = `Upload run failed: ${e.message}`;
    markStage("receipt", false);
  } finally { btn.disabled = false; }
}

document.addEventListener("DOMContentLoaded", async () => {
  $("#run-form").addEventListener("submit", onRun);
  const uf = $("#upload-form"); if (uf) uf.addEventListener("submit", onUpload);
  $("#search-form").addEventListener("submit", (ev) => { ev.preventDefault(); loadRuns($("#q").value); });
  $("#claim-filter").addEventListener("input", renderClaims);
  await loadPin();
  try { await loadObjectives(); } catch (e) { status(`Could not load objectives: ${e.message}`); }
  try { await loadRuns(); } catch (e) { status(`Could not load runs: ${e.message}`); }
});
