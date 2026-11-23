/*
 * Deterministic logic tests for the offline PLC simulator.
 *
 * Run from the repository root:
 *   node AI_Vision_Training/day07_09_support/tests/run_simulation_logic_tests.js
 *
 * The test extracts the LOGIC-START ... LOGIC-END block from the HTML and
 * exercises the state machine directly. It does not require a browser.
 */
"use strict";

const fs = require("fs");
const path = require("path");

const htmlPath = path.join(__dirname, "..", "simulations", "sim_plc_sequence.html");
const html = fs.readFileSync(htmlPath, "utf8");
const start = html.indexOf("/* LOGIC-START */");
const end = html.indexOf("/* LOGIC-END */");
if (start < 0 || end < 0) throw new Error("LOGIC markers missing");
const code = html.slice(start + "/* LOGIC-START */".length, end);
const api = new Function(code + "\nreturn { PusherSim, STATES };")();
const { PusherSim, STATES } = api;

let passed = 0;
function check(name, condition, detail) {
  if (!condition) throw new Error("FAIL: " + name + " :: " + (detail || ""));
  passed += 1;
}
function inputs(overrides = {}) {
  return Object.assign({ start: false, stopOk: true, retracted: true, extended: false }, overrides);
}
function normalCycle(sim) {
  const inp = inputs();
  for (let tick = 0; tick < 260; tick += 1) {
    const before = sim.snapshot();
    if (before.y2 && tick > 4) { inp.retracted = false; inp.extended = true; }
    if ((before.state === "RETRACT" || before.state === "WAIT_RETRACTED") && before.run && tick > 8) {
      inp.retracted = true; inp.extended = false;
    }
    if (tick === 3) inp.start = true;
    if (tick >= 6) inp.start = false;
    const snap = sim.step(inp, false, 50);
    if (snap.state === "COMPLETE") return snap;
  }
  throw new Error("normal cycle did not complete");
}

// 1. power restore with START held must not start
{
  const sim = new PusherSim();
  sim.powerOn(true);
  let snap;
  for (let i = 0; i < 20; i += 1) snap = sim.step(inputs({ start: true }), false, 100);
  check("power restore with held START", snap.state === "IDLE" && !snap.run, snap.state);
}
// 2. new START after release starts, and release self-holds
{
  const sim = new PusherSim();
  sim.powerOn(true);
  sim.step(inputs(), false, 100);           // release -> armed
  const pressed = sim.step(inputs({ start: true }), false, 100);
  check("START press", pressed.state === "READY" && pressed.run, pressed.state);
  const released = sim.step(inputs(), false, 100);
  check("self-holding after release", released.run && released.y0, released.state);
}
// 3. STOP has priority over the timer
{
  const sim = new PusherSim();
  normalCycle(sim);
  let snap = sim.step(inputs(), false, 100);   // re-arm
  snap = sim.step(inputs({ start: true }), false, 100);
  snap = sim.step(inputs(), false, 100);
  snap = sim.step(inputs({ stopOk: false }), false, 100);
  check("STOP during RUN", snap.state === "IDLE" && !snap.run && snap.t0 === 0, snap.state);
}
// 4. timer boundary 2999 / 3000
{
  const sim = new PusherSim();
  normalCycle(sim);
  const inp = inputs();
  while (sim.snapshot().t0 < 2999) sim.step(inp, false, 1);
  const before = sim.snapshot();
  check("timer 2999", before.t0 === 2999 && !before.y1, String(before.t0));
  const at = sim.step(inp, false, 1);
  check("timer 3000", at.t0 === 3000 && at.y1, String(at.t0));
}
// 5. missing extend confirmation gives F001
{
  const sim = new PusherSim();
  const inp = inputs();
  let snap;
  for (let i = 0; i < 10; i += 1) sim.step(inp, false, 100);
  sim.step(inp, false, 100);
  sim.step(inputs({ start: true }), false, 100);
  sim.step(inp, false, 100);
  for (let i = 0; i < 80; i += 1) snap = sim.step(inp, false, 100);
  check("F001 timeout", snap.fault === "F001" && snap.state === "FAULT", String(snap.fault));
}
// 6. conflicting sensors give F002
{
  const sim = new PusherSim();
  const snap = sim.step(inputs({ retracted: true, extended: true }), false, 100);
  check("F002 conflict", snap.fault === "F002", String(snap.fault));
}
// 7. fault reset with START held is refused
{
  const sim = new PusherSim();
  sim.step(inputs({ retracted: true, extended: true }), false, 100);
  sim.step(inputs({ start: true, retracted: false, extended: false }), false, 100);
  const refused = sim.step(inputs({ start: true, retracted: false, extended: false }), true, 100);
  check("reset refused with START held", refused.state === "FAULT", refused.state);
  sim.step(inputs(), false, 100);
  sim.step(inputs(), false, 100);
  const cleared = sim.step(inputs(), true, 100);
  check("reset after release", cleared.state === "IDLE" && cleared.fault === null, cleared.state);
  const after = sim.step(inputs(), false, 100);
  check("reset does not start motion", !after.run && !after.y2, after.state);
}
// 8. repeat cycle
{
  const sim = new PusherSim();
  normalCycle(sim);
  sim.step(inputs(), false, 100);
  const pressed = sim.step(inputs({ start: true }), false, 100);
  check("repeat cycle", pressed.state === "READY" && pressed.cycles === 2, String(pressed.cycles));
}
// 9. invalid transition
{
  const sim = new PusherSim();
  let threw = false;
  try { sim.transition("COMPLETE"); } catch (error) { threw = true; }
  check("invalid transition rejected", threw);
}
// 10. unknown state list is complete
{
  check("state list", STATES.length === 8 && STATES.includes("WAIT_RETRACTED"));
}

console.log(`SIMULATION LOGIC TESTS PASSED (${passed} checks)`);
