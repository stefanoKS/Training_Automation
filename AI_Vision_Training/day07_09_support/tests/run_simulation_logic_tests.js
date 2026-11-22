// Deterministic logic tests for the six offline simulations.
// Run: node day07_09_support/tests/run_simulation_logic_tests.js
// Exits non-zero on the first failure and prints a summary otherwise.
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const SIM_DIR = path.resolve(__dirname, "..", "simulations");

function loadLogic(file) {
  const html = fs.readFileSync(path.join(SIM_DIR, file), "utf8");
  const match = html.match(/\/\* LOGIC-START \*\/([\s\S]*?)\/\* LOGIC-END \*\//);
  if (!match) throw new Error("missing LOGIC markers in " + file);
  const sandbox = { module: { exports: {} }, exports: {} };
  vm.createContext(sandbox);
  vm.runInContext(match[1] + "\n;module.exports.__api = {" +
    ["rollerSpeed", "digitalSignal", "analogFromVoltage", "analogFromCurrent", "encoderCounts",
     "logicAnd", "logicOr", "logicNot", "selfHold", "onDelay", "counterStep", "explain",
     "STATES", "isReady", "nextState", "canAutoRestart", "cameraMath", "decideResult"]
      .map(name => name + ": (typeof " + name + " === 'undefined' ? undefined : " + name + ")").join(",") +
    "};", sandbox);
  return sandbox.module.exports.__api;
}

let checks = 0;
function ok(condition, message) {
  checks += 1;
  if (!condition) throw new Error("FAILED: " + message);
}
function close(actual, expected, tolerance, message) {
  ok(Math.abs(actual - expected) <= tolerance, message + " (got " + actual + ", expected " + expected + ")");
}

const roller = loadLogic("sim_roller_speed.html");
close(roller.rollerSpeed(100, 100).circumferenceMm, 314.159265, 0.001, "circumference 100mm");
close(roller.rollerSpeed(100, 100).mPerMin, 31.4159265, 0.001, "roller 100mm/100rpm m/min");
close(roller.rollerSpeed(80, 200).mPerMin, 50.265482, 0.001, "roller 80mm/200rpm m/min");
close(roller.rollerSpeed(100, 100).mPerS, 0.523599, 0.001, "roller m/s");
ok(roller.rollerSpeed(100, 0).mPerMin === 0, "zero rpm gives zero speed");

const sensor = loadLogic("sim_sensor_signals.html");
ok(sensor.digitalSignal(true) === 1 && sensor.digitalSignal(false) === 0, "digital states");
close(sensor.analogFromVoltage(7.5, 200, 10), 150, 1e-9, "0-10V 0-200kPa at 7.5V");
close(sensor.analogFromVoltage(5, 100, 10), 50, 1e-9, "0-10V 0-100kPa midpoint");
close(sensor.analogFromCurrent(12, 100), 50, 1e-9, "4-20mA midpoint");
close(sensor.analogFromCurrent(20, 100), 100, 1e-9, "4-20mA maximum");
ok(sensor.encoderCounts(500, 1, 4) === 2000, "PPR500 x4");
ok(sensor.encoderCounts(500, 1, 2) === 1000, "PPR500 x2");
ok(sensor.encoderCounts(1000, 1, 4) === 4000, "PPR1000 x4");

const ladder = loadLogic("sim_ladder_logic.html");
ok(ladder.logicAnd(0, 0) === 0 && ladder.logicAnd(0, 1) === 0 && ladder.logicAnd(1, 0) === 0 && ladder.logicAnd(1, 1) === 1, "AND truth table");
ok(ladder.logicOr(0, 0) === 0 && ladder.logicOr(0, 1) === 1 && ladder.logicOr(1, 0) === 1 && ladder.logicOr(1, 1) === 1, "OR truth table");
ok(ladder.logicNot(0) === 1 && ladder.logicNot(1) === 0, "NOT truth table");
ok(ladder.selfHold(1, 0, 0) === 1, "self-hold sets");
ok(ladder.selfHold(0, 0, 1) === 1, "self-hold remembers");
ok(ladder.selfHold(0, 1, 1) === 0, "self-hold stop clears");
ok(ladder.selfHold(1, 1, 1) === 0, "stop wins over start");
ok(ladder.onDelay(1, 1999, 2000).completed === 0, "on-delay before preset");
ok(ladder.onDelay(1, 2000, 2000).completed === 1, "on-delay at preset");
ok(ladder.onDelay(0, 1500, 2000).nextElapsed === 0, "on-delay resets when input off");
ok(ladder.counterStep(0, 1, 3, 0).count === 1, "counter increments on edge");
ok(ladder.counterStep(2, 0, 3, 0).count === 2, "counter holds without edge");
ok(ladder.counterStep(2, 1, 3, 0).done === 1, "counter reaches preset");
ok(ladder.counterStep(2, 0, 3, 1).count === 0, "counter reset");
ok(typeof ladder.explain("and", { x0: 1, x1: 1 }).ja === "string", "explanation is bilingual text");

const sequence = loadLogic("sim_machine_sequence.html");
const ready = { controllerOk: true, sensorOk: true, cameraReady: true, aiOk: true, noQualityFault: true, modeAuthorized: true };
ok(sequence.isReady(ready) === true, "readiness true");
ok(sequence.isReady(Object.assign({}, ready, { aiOk: false })) === false, "readiness false without AI");
ok(sequence.nextState("IDLE", Object.assign({}, ready)).state === "READY", "IDLE to READY");
ok(sequence.nextState("READY", { start: true }).state === "STARTING", "READY to STARTING");
ok(sequence.nextState("READY", { start: true, stop: true }).state === "STOPPING", "stop priority in READY");
ok(sequence.nextState("STARTING", { stop: true }).state === "STOPPING", "stop priority in STARTING");
ok(sequence.nextState("STARTING", { startTimeout: true }).state === "FAULT", "start timeout to FAULT");
ok(sequence.nextState("RUNNING", { fault: true }).state === "FAULT", "fault from RUNNING");
ok(sequence.nextState("FAULT", { reset: true }).state === "RECOVERY", "FAULT to RECOVERY");
ok(sequence.nextState("RECOVERY", { reset: true, restartPermit: true }).state === "IDLE", "RECOVERY to IDLE with permit");
ok(sequence.nextState("RECOVERY", { reset: true }).state === "RECOVERY", "no restart without permit");
ok(sequence.canAutoRestart() === false, "no automatic restart");

const camera = loadLogic("sim_camera_timing.html");
close(camera.cameraMath(30, 600, 4096, 0.2, 1).mmPerPixel, 0.146484375, 1e-9, "pixel scale 600/4096");
close(camera.cameraMath(30, 600, 4096, 0.2, 1).lineRate, 2500, 1e-6, "line rate 2500");
close(camera.cameraMath(30, 600, 4096, 0.2, 0.5).travelPerExposureMm, 0.25, 1e-9, "travel 0.25mm");
close(camera.cameraMath(60, 400, 2048, 0.1, 0.2).mmPerPixel, 0.1953125, 1e-9, "pixel scale 400/2048");
close(camera.cameraMath(60, 400, 2048, 0.1, 0.2).lineRate, 10000, 1e-6, "line rate 10000");
close(camera.cameraMath(30, 600, 4096, 0.2, 1).mmPerS, 500, 1e-9, "30 m/min is 500 mm/s");

const protocol = loadLogic("sim_ai_result_protocol.html");
ok(protocol.decideResult({ type: "OK", id: 101 }, null).decision === "ACCEPT_OK", "valid OK accepted");
ok(protocol.decideResult({ type: "NG", id: 101 }, null).decision === "ACCEPT_NG", "valid NG accepted");
ok(protocol.decideResult({ type: "INVALID", id: 101 }, null).decision === "HOLD", "invalid is held");
ok(protocol.decideResult({ type: "OK", id: 101, valid: false }, null).decision === "HOLD", "valid=false is held");
ok(protocol.decideResult({ type: "TIMEOUT", id: 101 }, null).decision === "HOLD", "timeout is held");
ok(protocol.decideResult({ type: "OK", id: 100 }, 101).decision === "REJECT_STALE", "stale ID rejected");
ok(protocol.decideResult({ type: "DUPLICATE", id: 101 }, 101).decision === "REJECT_DUPLICATE", "duplicate ID rejected");
ok(protocol.decideResult({ type: "OK", id: 101 }, 101).decision === "REJECT_DUPLICATE", "same ID not accepted twice");
ok(protocol.decideResult({ type: "OK", id: 102 }, 101).decision === "ACCEPT_OK", "new ID accepted");

const banned = ["fetch(", "XMLHttpRequest", "WebSocket", "http://", "https://", "<script src"];
for (const file of fs.readdirSync(SIM_DIR).filter(name => name.endsWith(".html"))) {
  const html = fs.readFileSync(path.join(SIM_DIR, file), "utf8");
  for (const token of banned) ok(!html.includes(token), file + " must not contain " + token);
  ok(html.includes("<noscript>"), file + " needs a no-JavaScript fallback");
}

console.log("SIMULATION LOGIC TESTS PASSED: " + checks + " checks across 6 simulations");
