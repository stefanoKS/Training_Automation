// Offline logic tests for simulations/sim_plc_sequence.html.
// The pure LOGIC block is extracted and evaluated with node's vm module.
// Run: node day07_09_support/tests/run_simulation_logic_tests.js

const fs = require("fs");
const path = require("path");
const vm = require("vm");

const htmlPath = path.join(__dirname, "..", "simulations", "sim_plc_sequence.html");
const html = fs.readFileSync(htmlPath, "utf8");

for (const banned of ["fetch(", "XMLHttpRequest", "WebSocket", "http://", "https://", "<script src"]) {
  if (html.includes(banned)) {
    console.error("FAIL: forbidden network reference in the simulator: " + banned);
    process.exit(1);
  }
}

const start = html.indexOf("/* LOGIC-START */");
const end = html.indexOf("/* LOGIC-END */");
if (start < 0 || end < 0) {
  console.error("FAIL: logic block markers not found");
  process.exit(1);
}
const source = html.slice(start, end);
const sandbox = { console: console };
vm.createContext(sandbox);
vm.runInContext(source, sandbox);

const step = sandbox.step;
const stepBasicSealIn = sandbox.stepBasicSealIn;
const stepExtended = sandbox.stepExtended;
const extendCommand = sandbox.extendCommand;
const stepInterlock = sandbox.stepInterlock;

let checks = 0;

function check(name, condition) {
  checks += 1;
  if (!condition) {
    console.error("FAIL: " + name);
    process.exit(1);
  }
}

function fresh(overrides) {
  return Object.assign({ run: false, armed: false, prevStart: true, extended: false }, overrides || {});
}

function advance(state, inputs) {
  const snap = step(state, inputs);
  return { snap: snap, state: fresh({ run: snap.run, armed: snap.armed, prevStart: snap.prevStart,
                                     extended: state.extended }) };
}

const base = { start: false, stopOk: true, retracted: true, extended: false };

// 1. basic seal-in keeps RUN after START is released
let stepResult = advance(fresh(), Object.assign({}, base, { start: true }));
check("basic: START starts RUN", stepResult.snap.run === true);
stepResult = advance(stepResult.state, base);
check("basic: RUN survives START release", stepResult.snap.run === true);

// 2. basic seal-in restarts when permission returns while START is held
stepResult = advance(fresh({ run: true }), Object.assign({}, base, { stopOk: false, start: true }));
check("basic: STOP clears RUN", stepResult.snap.run === false);
stepResult = advance(stepResult.state, Object.assign({}, base, { start: true }));
check("basic: permission restored with START held restores RUN", stepResult.snap.run === true);

// 3. extended logic does not restart from a held START at power-up
stepResult = advance(fresh({ extended: true }), Object.assign({}, base, { start: true }));
check("extended: held START at power-up does not run", stepResult.snap.run === false);
check("extended: held START does not arm", stepResult.snap.armed === false);

// 4. extended logic needs a release and a new rising edge
stepResult = advance(stepResult.state, base);
check("extended: START released arms", stepResult.snap.armed === true && stepResult.snap.run === false);
stepResult = advance(stepResult.state, Object.assign({}, base, { start: true }));
check("extended: new edge starts", stepResult.snap.run === true);

// 5. extended logic: STOP clears, and restoring permission with START held does not restart
stepResult = advance(fresh({ run: true, prevStart: false, extended: true }),
                     Object.assign({}, base, { stopOk: false, start: true }));
check("extended: STOP clears RUN", stepResult.snap.run === false && stepResult.snap.armed === false);
stepResult = advance(stepResult.state, Object.assign({}, base, { start: true }));
check("extended: permission restored with START held does not restart", stepResult.snap.run === false);

// 6. extended logic: a start request away from the retracted position is refused
stepResult = advance(fresh({ armed: true, prevStart: false, extended: true }),
                     Object.assign({}, base, { start: true, retracted: false }));
check("extended: start refused without retracted confirmation", stepResult.snap.run === false);

// 7. extend command needs RUN, retracted confirmation and no extended confirmation
check("extend: allowed", extendCommand(true, true, false) === true);
check("extend: refused when extended", extendCommand(true, true, true) === false);
check("extend: refused when not running", extendCommand(false, true, false) === false);

// 8. interlock rejects simultaneous requests deterministically
const both = stepInterlock({ forward: true, reverse: true, stopOk: true });
check("interlock: both rejected", both.forward === false && both.reverse === false && both.conflict === true);
check("interlock: forward only", stepInterlock({ forward: true, reverse: false, stopOk: true }).forward === true);
check("interlock: reverse only", stepInterlock({ forward: false, reverse: true, stopOk: true }).reverse === true);
check("interlock: stop clears both", stepInterlock({ forward: true, reverse: false, stopOk: false }).forward === false);

// 9. the exported helpers behave the same as the combined step function
check("helpers: basic matches step",
  stepBasicSealIn({ run: false }, Object.assign({}, base, { start: true })).run ===
  step(fresh(), Object.assign({}, base, { start: true })).run);
check("helpers: extended matches step",
  stepExtended({ run: false, armed: true, prevStart: false }, Object.assign({}, base, { start: true })).run ===
  step(fresh({ armed: true, prevStart: false, extended: true }),
       Object.assign({}, base, { start: true })).run);

console.log("SIMULATION LOGIC TESTS PASSED (" + checks + " checks)");
