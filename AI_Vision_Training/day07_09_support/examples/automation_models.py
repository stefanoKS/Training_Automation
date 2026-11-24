"""Deterministic engineering models for the Day 7-9 training course.

This module is the executable reference used by the lesson notebooks, the
offline demonstrations and the test suite.  Every function is deliberately
small, validates its inputs and states its assumptions.  Nothing here is a
machine design, a safety validation or a manufacturer's selection.

Units
-----
* time: seconds (s), minutes (min), milliseconds (ms)
* length: millimetres (mm) except where a name says ``_m``
* mass: kilograms (kg)
* force: newtons (N)
* pressure: megapascals (MPa) in the teaching API; 1 MPa = 1 N/mm^2
* torque: newton-metres (N.m)
* electrical: volts (V), amperes (A), watts (W), kilowatt-hours (kWh)
* money: Japanese yen (JPY), a hypothetical training value

Scope note
----------
Days 7-9 were simplified by management.  Availability/OEE models, subnet
arithmetic, commissioning test matrices and proposal scoring are deliberately
absent: they are no longer part of the active curriculum.  They remain
recoverable from Git history.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from math import pi, sqrt

GRAVITY = 9.81  # m/s^2, teaching value
SECONDS_PER_HOUR = 3600.0


# --------------------------------------------------------------------------- #
# validation helpers
# --------------------------------------------------------------------------- #
def _positive(name: str, value: float, *, allow_zero: bool = False) -> float:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise ValueError(f"{name} must be a number, got {value!r}")
    if value != value or value in (float("inf"), float("-inf")):
        raise ValueError(f"{name} must be finite, got {value!r}")
    if allow_zero and value < 0:
        raise ValueError(f"{name} must be >= 0, got {value!r}")
    if not allow_zero and value <= 0:
        raise ValueError(f"{name} must be > 0, got {value!r}")
    return float(value)


def _fraction(name: str, value: float) -> float:
    _positive(name, value)
    if value > 1.0:
        raise ValueError(f"{name} must be between 0 and 1 (a fraction, not a percentage), got {value!r}")
    return float(value)


# --------------------------------------------------------------------------- #
# 1. production capacity (Day 7-01)
# --------------------------------------------------------------------------- #
def takt_time_s(available_min: float, required_pieces: float) -> float:
    """Target pace = available production time / required quantity.

    ``available_min`` is *net available* production time in minutes, excluding
    breaks and lunch.  The result is seconds per piece: the pace the line has
    to keep to finish the required quantity in the available time.
    """
    _positive("available_min", available_min)
    _positive("required_pieces", required_pieces)
    return available_min * 60.0 / required_pieces


def capacity_per_h(cycle_s: float, pieces_per_cycle: float = 1.0) -> float:
    """Theoretical capacity: pieces finished per hour at a defined cycle time.

    ``pieces_per_cycle`` must be stated, because 15 s per *cycle* is 240
    cycles/hour but only 240 pieces/hour when one piece leaves per cycle.
    This is an upper bound with no stoppage, no defect and no ramp-up.
    """
    _positive("cycle_s", cycle_s)
    _positive("pieces_per_cycle", pieces_per_cycle)
    return SECONDS_PER_HOUR / cycle_s * pieces_per_cycle


def required_rate_per_h(required_pieces: float, available_min: float) -> float:
    """Required production rate in pieces/hour over the available time."""
    _positive("required_pieces", required_pieces)
    _positive("available_min", available_min)
    return required_pieces / (available_min / 60.0)


def capacity_report(
    available_min: float = 420.0,
    required_pieces: float = 600.0,
    cycle_s: float = 15.0,
    pieces_per_cycle: float = 1.0,
) -> dict:
    """All capacity numbers used by lesson 07-01, with their inputs."""
    takt = takt_time_s(available_min, required_pieces)
    return {
        "available_min": available_min,
        "required_pieces": required_pieces,
        "takt_s": takt,
        "cycle_s": cycle_s,
        "pieces_per_cycle": pieces_per_cycle,
        "cycle_meets_takt": cycle_s <= takt,
        "required_pieces_per_h": required_rate_per_h(required_pieces, available_min),
        "theoretical_per_h": capacity_per_h(cycle_s, pieces_per_cycle),
    }


def capacity_table(cycle_values: list[float], pieces_per_cycle: float = 1.0) -> list[dict]:
    """Rows for the capacity chart: cycle time against theoretical capacity."""
    rows = []
    for cycle in cycle_values:
        _positive("cycle_s", cycle)
        rows.append(
            {
                "cycle_s": float(cycle),
                "theoretical_per_h": capacity_per_h(cycle, pieces_per_cycle),
            }
        )
    return rows


# --------------------------------------------------------------------------- #
# 2. mechanics: friction, cylinder, motor (Day 7-03)
# --------------------------------------------------------------------------- #
def friction_force_n(mass_kg: float, friction_coefficient: float, gravity: float = GRAVITY) -> float:
    """Sliding friction estimate F = mu * m * g on a horizontal surface.

    Static friction can be higher than sliding friction for many interfaces,
    so this is a starting estimate, not a design value.
    """
    _positive("mass_kg", mass_kg)
    _positive("friction_coefficient", friction_coefficient, allow_zero=True)
    _positive("gravity", gravity)
    return mass_kg * gravity * friction_coefficient


def design_force_n(friction_n: float, factor: float) -> float:
    """Illustrative design force = estimated load * a teaching margin factor.

    The factor is an example (2 here), not a universal design rule.
    """
    _positive("friction_n", friction_n, allow_zero=True)
    if not isinstance(factor, (int, float)) or isinstance(factor, bool) or factor < 1:
        raise ValueError(f"factor must be a number >= 1, got {factor!r}")
    return friction_n * float(factor)


def theoretical_bore_mm(force_n: float, pressure_mpa: float) -> float:
    """Bore that just produces ``force_n`` at ``pressure_mpa``: D = sqrt(4F/(pi P)).

    Pressure is a gauge pressure and the result ignores friction, load ratio,
    rod-side area, back pressure and dynamic effects.
    """
    _positive("force_n", force_n, allow_zero=True)
    _positive("pressure_mpa", pressure_mpa)
    return sqrt(4.0 * force_n / (pi * pressure_mpa))


def cylinder_force_n(bore_mm: float, pressure_mpa: float, rod_mm: float = 0.0) -> float:
    """Theoretical cylinder force in newtons.

    Extension uses the piston area pi*D^2/4.  Retraction uses the annulus
    pi*(D^2-d^2)/4.  ``pressure_mpa`` is the effective gauge pressure; opposing
    gauge pressure, friction, dynamic loads and losses are not modelled.
    """
    _positive("bore_mm", bore_mm)
    _positive("pressure_mpa", pressure_mpa)
    _positive("rod_mm", rod_mm, allow_zero=True)
    if rod_mm >= bore_mm:
        raise ValueError(f"rod diameter {rod_mm} must be smaller than bore {bore_mm}")
    if rod_mm:
        area = pi * (bore_mm ** 2 - rod_mm ** 2) / 4.0
    else:
        area = pi * bore_mm ** 2 / 4.0
    return pressure_mpa * area


def cylinder_report(bore_mm: float = 20.0, rod_mm: float = 8.0, pressure_mpa: float = 0.5) -> dict:
    """Extension and retraction force for one simplified cylinder example."""
    return {
        "bore_mm": bore_mm,
        "rod_mm": rod_mm,
        "pressure_mpa": pressure_mpa,
        "extension_force_n": cylinder_force_n(bore_mm, pressure_mpa),
        "retraction_force_n": cylinder_force_n(bore_mm, pressure_mpa, rod_mm) if rod_mm else None,
        "assumptions": [
            "gauge pressure at the cylinder is uniform",
            "opposing gauge pressure is negligible",
            "friction and dynamic loads are ignored",
            "values are theoretical, not a catalogue selection",
        ],
    }


def angular_speed_rad_s(speed_rpm: float) -> float:
    """Angular speed omega = 2*pi*rpm/60 in rad/s."""
    _positive("speed_rpm", speed_rpm)
    return 2.0 * pi * speed_rpm / 60.0


def motor_torque_nm(power_w: float, speed_rpm: float) -> float:
    """Shaft torque from *mechanical* output power: T = P / omega.

    Mechanical output power is not electrical input power; motor efficiency
    and drive losses are separate.
    """
    _positive("power_w", power_w)
    return power_w / angular_speed_rad_s(speed_rpm)


def reducer_output_speed_rpm(input_rpm: float, ratio: float) -> float:
    """Output speed of an ideal reduction gearbox."""
    _positive("input_rpm", input_rpm)
    _positive("ratio", ratio)
    return input_rpm / ratio


def reducer_output_torque_nm(input_torque_nm: float, ratio: float, efficiency: float = 1.0) -> float:
    """Output torque of a reduction gearbox including its own efficiency.

    Reducer efficiency is not motor efficiency; both losses exist.
    """
    _positive("input_torque_nm", input_torque_nm)
    _positive("ratio", ratio)
    _fraction("efficiency", efficiency)
    return input_torque_nm * ratio * efficiency


def motor_report(power_w: float = 60.0, speed_rpm: float = 1200.0, ratio: float = 20.0,
                 efficiency: float = 0.90) -> dict:
    """Worked motor/reducer example for lesson 07-03."""
    torque = motor_torque_nm(power_w, speed_rpm)
    return {
        "mechanical_power_w": power_w,
        "speed_rpm": speed_rpm,
        "motor_torque_nm": torque,
        "ratio": ratio,
        "output_speed_rpm": reducer_output_speed_rpm(speed_rpm, ratio),
        "ideal_output_torque_nm": reducer_output_torque_nm(torque, ratio, 1.0),
        "estimated_output_torque_nm": reducer_output_torque_nm(torque, ratio, efficiency),
        "assumptions": [
            "60 W is mechanical output power at the motor shaft",
            "the load is steady; starting and acceleration torque are not modelled",
            "reducer efficiency does not replace motor efficiency",
        ],
    }


# --------------------------------------------------------------------------- #
# 3. electrical power, current and energy (Day 8-01)
# --------------------------------------------------------------------------- #
def dc_power_w(voltage_v: float, current_a: float) -> float:
    """Steady DC power P = V * I (watts)."""
    _positive("voltage_v", voltage_v)
    _positive("current_a", current_a, allow_zero=True)
    return voltage_v * current_a


@dataclass
class Load:
    """One DC load group.  Give either current_a or power_w, not both."""

    name: str
    quantity: int
    voltage_v: float
    current_a: float | None = None
    power_w: float | None = None

    def unit_current_a(self) -> float:
        if self.quantity < 0:
            raise ValueError("quantity must be >= 0")
        if self.voltage_v <= 0:
            raise ValueError("voltage_v must be > 0")
        if (self.current_a is None) == (self.power_w is None):
            raise ValueError(f"{self.name}: give exactly one of current_a or power_w")
        if self.current_a is not None:
            _positive("current_a", self.current_a, allow_zero=True)
            return float(self.current_a)
        _positive("power_w", self.power_w, allow_zero=True)
        return float(self.power_w) / float(self.voltage_v)

    def total_current_a(self) -> float:
        return self.unit_current_a() * self.quantity

    def total_power_w(self) -> float:
        return self.total_current_a() * self.voltage_v


def total_load_current_a(loads: list[Load]) -> float:
    return sum(load.total_current_a() for load in loads)


def load_report(loads: list[Load], supply_margin: float = 0.25) -> dict:
    """Steady-state load budget with an explicitly separate planning margin.

    The margin is a planning allowance, not a substitute for checking inrush,
    derating, terminal ratings, wire ampacity and protective-device coordination.
    """
    rows = [
        {
            "name": load.name,
            "quantity": load.quantity,
            "voltage_v": load.voltage_v,
            "unit_current_a": load.unit_current_a(),
            "total_current_a": load.total_current_a(),
            "total_power_w": load.total_power_w(),
        }
        for load in loads
    ]
    _positive("supply_margin", supply_margin, allow_zero=True)
    voltage = rows[0]["voltage_v"] if rows else 24.0
    steady = sum(row["total_current_a"] for row in rows)
    return {
        "rows": rows,
        "steady_total_a": steady,
        "total_power_w": steady * voltage,
        "margin_fraction": supply_margin,
        "planning_current_a": steady * (1.0 + supply_margin),
        "is_sizing_approval": False,
    }


def training_power_budget() -> list[Load]:
    """The Day 8-01 budget: PLC, four sensors, two valves and one lamp on DC24V."""
    return [
        Load("PLC", 1, 24.0, current_a=0.35),
        Load("sensor", 4, 24.0, current_a=0.025),
        Load("solenoid valve", 2, 24.0, current_a=0.15),
        Load("indicator lamp", 1, 24.0, current_a=0.05),
    ]


def energy_kwh(power_w: float, hours: float) -> float:
    """Electrical energy in kWh = power in kW * time in hours."""
    _positive("power_w", power_w, allow_zero=True)
    _positive("hours", hours, allow_zero=True)
    return power_w / 1000.0 * hours


def energy_cost_jpy(kwh: float, rate_jpy_per_kwh: float) -> float:
    """Cost estimate; the rate is an illustrative training value."""
    _positive("kwh", kwh, allow_zero=True)
    _positive("rate_jpy_per_kwh", rate_jpy_per_kwh, allow_zero=True)
    return kwh * rate_jpy_per_kwh


# --------------------------------------------------------------------------- #
# 4. cost and payback (Day 7-01)
# --------------------------------------------------------------------------- #
def labour_time_report(
    seconds_saved_per_occurrence: float,
    occurrences_per_day: float,
    working_days_per_year: float,
    hourly_rate_jpy: float,
) -> dict:
    """Hypothetical labour-time value of a time reduction.

    It is not realised cash unless the freed time is redeployed or overtime is
    actually reduced.  Maintenance, energy and consumables are excluded.
    """
    _positive("seconds_saved_per_occurrence", seconds_saved_per_occurrence, allow_zero=True)
    _positive("occurrences_per_day", occurrences_per_day, allow_zero=True)
    _positive("working_days_per_year", working_days_per_year, allow_zero=True)
    _positive("hourly_rate_jpy", hourly_rate_jpy, allow_zero=True)
    seconds_per_day = seconds_saved_per_occurrence * occurrences_per_day
    hours_per_day = seconds_per_day / SECONDS_PER_HOUR
    hours_per_year = hours_per_day * working_days_per_year
    return {
        "seconds_per_day": seconds_per_day,
        "minutes_per_day": seconds_per_day / 60.0,
        "hours_per_day": hours_per_day,
        "hours_per_year": hours_per_year,
        "annual_value_jpy": hours_per_year * hourly_rate_jpy,
    }


def annual_net_benefit_jpy(annual_value_jpy: float, annual_operating_cost_jpy: float = 0.0) -> float:
    """Annual net benefit = annual value - annual incremental operating cost."""
    _positive("annual_value_jpy", annual_value_jpy, allow_zero=True)
    _positive("annual_operating_cost_jpy", annual_operating_cost_jpy, allow_zero=True)
    return annual_value_jpy - annual_operating_cost_jpy


def payback_years(investment_jpy: float, annual_net_benefit_jpy: float) -> float:
    """Simple payback = investment / annual net benefit.

    Undefined (infinite) when the annual net benefit is zero or negative.
    """
    _positive("investment_jpy", investment_jpy)
    if not isinstance(annual_net_benefit_jpy, (int, float)) or isinstance(annual_net_benefit_jpy, bool):
        raise ValueError("annual_net_benefit_jpy must be a number")
    if annual_net_benefit_jpy <= 0:
        return float("inf")
    return investment_jpy / float(annual_net_benefit_jpy)


def payback_report(
    seconds_saved: float = 12.0,
    occurrences_per_day: float = 180.0,
    days_per_year: float = 220.0,
    hourly_rate_jpy: float = 2400.0,
    investment_jpy: float = 450_000.0,
    annual_operating_cost_jpy: float = 0.0,
) -> dict:
    """Worked financial example used by lesson 07-01."""
    labour = labour_time_report(seconds_saved, occurrences_per_day, days_per_year, hourly_rate_jpy)
    net = annual_net_benefit_jpy(labour["annual_value_jpy"], annual_operating_cost_jpy)
    return {
        **labour,
        "investment_jpy": investment_jpy,
        "annual_operating_cost_jpy": annual_operating_cost_jpy,
        "annual_net_benefit_jpy": net,
        "payback_years": payback_years(investment_jpy, net),
    }


# --------------------------------------------------------------------------- #
# 5. sensors, NPN/PNP and PLC input compatibility (Day 8-02)
# --------------------------------------------------------------------------- #
def plc_input_compatibility(output_type: str, plc_common: str) -> dict:
    """Describe the conventional current path for a 3-wire sensor and a PLC input.

    ``output_type`` is "PNP" (sources current when active) or "NPN" (sinks
    current when active).  ``plc_common`` is where the PLC input common
    terminal is connected: "0V" (sinking input) or "+24V" (sourcing input).

    Returns the compatibility result and a conceptual current path.  This is a
    teaching model; actual wiring follows the sensor and PLC datasheets.
    """
    kind = str(output_type).upper()
    common = str(plc_common).upper().replace(" ", "")
    if kind not in ("PNP", "NPN"):
        raise ValueError(f"output_type must be PNP or NPN, got {output_type!r}")
    if common not in ("0V", "+24V", "24V"):
        raise ValueError(f"plc_common must be '0V' or '+24V', got {plc_common!r}")
    common = "0V" if common == "0V" else "+24V"
    compatible = (kind == "PNP" and common == "0V") or (kind == "NPN" and common == "+24V")
    if kind == "PNP":
        path = "+24V -> PNP sensor output -> PLC input circuit -> 0V (common)"
        note = "PNP sources current into a sinking input whose common is 0V."
    else:
        path = "+24V (common) -> PLC input circuit -> NPN sensor output -> 0V"
        note = "NPN sinks current from a sourcing input whose common is +24V."
    return {
        "output_type": kind,
        "plc_common": common,
        "compatible": compatible,
        "current_path": path,
        "note": note,
        "is_detection_principle": False,
    }


def sensor_output_state(sensor_normally_closed: bool, target_present: bool) -> bool:
    """Physical NO/NC behaviour of a sensor output, separate from NPN/PNP."""
    if not isinstance(sensor_normally_closed, bool) or not isinstance(target_present, bool):
        raise ValueError("arguments must be booleans")
    return (not target_present) if sensor_normally_closed else target_present


# --------------------------------------------------------------------------- #
# 6. PLC models (Day 8-03)
# --------------------------------------------------------------------------- #
CANONICAL_IO = (
    {"address": "X0", "kind": "input", "device": "START pushbutton", "normal": "OFF; momentary ON when pressed"},
    {"address": "X1", "kind": "input", "device": "STOP_OK permission from a physical NC STOP", "normal": "ON while healthy"},
    {"address": "X2", "kind": "input", "device": "retracted position confirmation", "normal": "ON at the retracted end"},
    {"address": "X3", "kind": "input", "device": "extended position confirmation", "normal": "ON at the extended end"},
    {"address": "X4", "kind": "input", "device": "product present at the inspection position", "normal": "ON while a product is present"},
    {"address": "M0", "kind": "internal", "device": "RUN internal state bit", "normal": "OFF at power-up"},
    {"address": "M1", "kind": "internal", "device": "START armed (a fresh press is accepted)", "normal": "OFF after each accepted start"},
    {"address": "Y0", "kind": "output", "device": "RUN indicator lamp", "normal": "OFF when not running"},
    {"address": "Y2", "kind": "output", "device": "EXTEND solenoid command", "normal": "OFF = spring-return retract (training valve)"},
)

CANONICAL_IO_DEVICE_NAMES = {row["address"]: row["device"] for row in CANONICAL_IO}


def validate_io(rows) -> list[str]:
    """Return consistency problems in an I/O table.

    Checks duplicate addresses, a missing address and the classic mistake of
    describing X1 (a healthy-NC permission) as normally OFF.
    """
    problems: list[str] = []
    addresses = [row["address"] for row in rows]
    duplicates = sorted({address for address in addresses if addresses.count(address) > 1})
    if duplicates:
        problems.append(f"duplicate addresses: {', '.join(duplicates)}")
    for row in rows:
        address = row["address"]
        device = str(row["device"]).lower()
        if address in ("Y1", "Y0") and ("solenoid" in device or "valve" in device or "電磁弁" in str(row["device"])):
            problems.append(f"{address} is an indicator output; use Y2 for the extend solenoid")
        if address == "X1" and str(row["normal"]).lower().startswith("off"):
            problems.append("X1 STOP_OK is ON while the physical NC stop is healthy; its normal state is ON")
    expected = {row["address"] for row in CANONICAL_IO}
    missing = sorted(expected - set(addresses))
    if missing:
        problems.append(f"missing addresses: {', '.join(missing)}")
    return problems


@dataclass
class BasicSealIn:
    """The *basic* seal-in rung only: M0 = X1 AND (X0 OR M0).

    It demonstrates the memory principle and nothing else.  It has no start
    arming, no edge detection and no restart prevention: if STOP permission is
    restored while START is still held, RUN returns.  Lesson 08-03 uses this
    to show why the extended logic exists.
    """

    run: bool = False

    def step(self, start: bool, stop_ok: bool = True) -> bool:
        self.run = bool(stop_ok) and (bool(start) or self.run)
        return self.run


@dataclass
class StartGate:
    """Extended start logic: fresh edge, arming, stop priority, confirmed position.

    The armed bit becomes true only after START is seen released while the
    machine is idle and the retracted position is confirmed.  A rising edge of
    START while armed starts the cycle.  STOP, a fault and power-up clear it.
    """

    run: bool = False
    armed: bool = False
    start_prev: bool = True  # conservative: a held START at power-up is not an edge
    fault: bool = False

    def power_on(self) -> None:
        self.run = False
        self.armed = False
        self.start_prev = True

    def step(self, start: bool, stop_ok: bool = True, retracted: bool = True,
             extended: bool = False, reset: bool = False) -> dict:
        if self.fault and reset and not start and stop_ok:
            self.fault = False
        if self.fault or not stop_ok:
            self.run = False
            self.armed = False
        elif not start and retracted and not extended:
            self.armed = True
        edge = bool(start) and not self.start_prev
        if edge and self.armed and retracted and not extended:
            self.run = True
            self.armed = False
        self.start_prev = bool(start)
        return {"run": self.run, "armed": self.armed, "start_edge": edge, "fault": self.fault}


STATES = ("IDLE", "READY", "EXTEND", "WAIT_EXTENDED", "RETRACT", "WAIT_RETRACTED", "COMPLETE", "FAULT")

ALLOWED_TRANSITIONS = {
    "IDLE": {"READY", "FAULT"},
    "READY": {"EXTEND", "IDLE", "FAULT"},
    "EXTEND": {"WAIT_EXTENDED", "IDLE", "FAULT"},
    "WAIT_EXTENDED": {"RETRACT", "IDLE", "FAULT"},
    "RETRACT": {"WAIT_RETRACTED", "IDLE", "FAULT"},
    "WAIT_RETRACTED": {"COMPLETE", "IDLE", "FAULT"},
    "COMPLETE": {"READY", "IDLE", "FAULT"},
    "FAULT": {"IDLE"},
}


@dataclass
class PlcInputs:
    """Fictional training inputs.  X1 is ON when the physical NC STOP is healthy."""

    start: bool = False       # X0 START pushbutton, ON while pressed
    stop_ok: bool = True      # X1 STOP_OK / permission, ON in normal condition
    retracted: bool = True    # X2 retracted position sensor
    extended: bool = False    # X3 extended position sensor


@dataclass
class PlcSnapshot:
    state: str
    run: bool
    y0_run_lamp: bool
    y2_extend_solenoid: bool
    motion_ms: int
    fault_code: str | None
    cycle_count: int
    fresh_start_required: bool
    start_armed: bool
    stop_ok: bool
    retracted: bool
    extended: bool
    elapsed_ms: int

    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class PusherSequence:
    """Deterministic PLC-like scan model for the pusher machine.

    Mapping (fictional training addresses, not real terminal numbers):

    ==========  ==========================================
    X0          START pushbutton (NO, ON while pressed)
    X1          STOP_OK permission (ON while NC STOP healthy)
    X2          retracted position confirmation
    X3          extended position confirmation
    M0          RUN internal state
    Y0          RUN indicator
    Y2          extend solenoid command (OFF = spring-return retract)
    ==========  ==========================================

    Restart rule: a RUN state is never resumed automatically.  After power-up,
    a STOP or a fault reset, the program requires START to be released and
    pressed again while the retracted position is confirmed.
    """

    motion_timeout_ms: int = 3000
    max_cycles: int = 10_000

    def __post_init__(self) -> None:
        if not isinstance(self.motion_timeout_ms, int) or self.motion_timeout_ms <= 0:
            raise ValueError("motion_timeout_ms must be a positive integer")
        self.power_on()

    def power_on(self) -> PlcSnapshot:
        """Initialise as a cold power-up with START treated as possibly held."""
        self.state = "IDLE"
        self.run = False
        self.motion_ms = 0
        self.fault_code: str | None = None
        self.cycle_count = 0
        self.fresh_start_required = True
        self.start_armed = False
        self.start_prev = True  # be conservative: a held START is not an edge
        self.reset_prev = True
        self.elapsed_ms = 0
        self.last_inputs = PlcInputs()
        return self.snapshot()

    def transition_to(self, new_state: str) -> None:
        if new_state not in STATES:
            raise ValueError(f"unknown state {new_state!r}")
        if new_state not in ALLOWED_TRANSITIONS[self.state]:
            raise ValueError(f"invalid transition {self.state} -> {new_state}")
        self.state = new_state

    def step(self, inputs: PlcInputs, dt_ms: int = 100, reset: bool = False) -> PlcSnapshot:
        if not isinstance(inputs, PlcInputs):
            raise ValueError("inputs must be a PlcInputs instance")
        if not isinstance(dt_ms, int) or dt_ms <= 0:
            raise ValueError("dt_ms must be a positive integer")
        self.elapsed_ms += dt_ms
        self.last_inputs = inputs

        # Fault detection is independent of the sequence step.
        if inputs.retracted and inputs.extended and self.state != "FAULT":
            self._enter_fault("F002", "both position sensors ON (impossible state)")

        if self.state == "FAULT":
            self.run = False
            self.motion_ms = 0
            reset_edge = bool(reset) and not self.reset_prev
            if reset_edge and not inputs.start and inputs.stop_ok:
                self.transition_to("IDLE")
                self.fault_code = None
                self.fresh_start_required = True
                self.start_armed = False
            self.reset_prev = bool(reset)
            self.start_prev = inputs.start
            return self.snapshot()

        # Ordinary STOP: abort, de-energise the command, require a fresh start.
        if not inputs.stop_ok:
            if self.state != "IDLE":
                self.transition_to("IDLE")
            self.run = False
            self.motion_ms = 0
            self.fresh_start_required = True
            self.start_armed = False
            self.reset_prev = bool(reset)
            self.start_prev = inputs.start
            return self.snapshot()

        # Re-arm only after START is released and the machine is settled.
        if not inputs.start and self.state in ("IDLE", "COMPLETE"):
            self.start_armed = True

        started_this_step = False
        start_edge = inputs.start and not self.start_prev
        if start_edge and self.start_armed and self.state in ("IDLE", "COMPLETE"):
            if not inputs.retracted or inputs.extended:
                self.start_armed = False  # not at a confirmed starting position
            else:
                self.transition_to("READY")
                self.run = True
                self.motion_ms = 0
                self.fresh_start_required = False
                self.start_armed = False
                self.cycle_count += 1
                started_this_step = True

        if started_this_step:
            pass
        elif self.state == "READY":
            self.transition_to("EXTEND")
            self.motion_ms = 0
        elif self.state == "EXTEND":
            self.transition_to("WAIT_EXTENDED")
            self.motion_ms = 0
        elif self.state == "WAIT_EXTENDED":
            self.motion_ms += dt_ms
            if inputs.extended and not inputs.retracted:
                self.transition_to("RETRACT")
                self.motion_ms = 0
            elif self.motion_ms > self.motion_timeout_ms:
                self._enter_fault("F001", "extend confirmation not reached before timeout")
        elif self.state == "RETRACT":
            self.transition_to("WAIT_RETRACTED")
            self.motion_ms = 0
        elif self.state == "WAIT_RETRACTED":
            self.motion_ms += dt_ms
            if inputs.retracted and not inputs.extended:
                self.transition_to("COMPLETE")
                self.motion_ms = 0
            elif self.motion_ms > self.motion_timeout_ms:
                self._enter_fault("F003", "retract confirmation not reached before timeout")

        self.reset_prev = bool(reset)
        self.start_prev = inputs.start
        return self.snapshot()

    def _enter_fault(self, code: str, reason: str) -> None:
        self.state = "FAULT"
        self.run = False
        self.motion_ms = 0
        self.fault_code = code
        self.fresh_start_required = True
        self.start_armed = False
        self.fault_reason = reason

    @property
    def y2_extend_solenoid(self) -> bool:
        return self.state in ("EXTEND", "WAIT_EXTENDED")

    @property
    def y0_run_lamp(self) -> bool:
        return self.run

    def snapshot(self) -> PlcSnapshot:
        return PlcSnapshot(
            state=self.state,
            run=self.run,
            y0_run_lamp=self.y0_run_lamp,
            y2_extend_solenoid=self.y2_extend_solenoid,
            motion_ms=self.motion_ms,
            fault_code=self.fault_code,
            cycle_count=self.cycle_count,
            fresh_start_required=self.fresh_start_required,
            start_armed=self.start_armed,
            stop_ok=self.last_inputs.stop_ok,
            retracted=self.last_inputs.retracted,
            extended=self.last_inputs.extended,
            elapsed_ms=self.elapsed_ms,
        )


def snapshot_line(snapshot: PlcSnapshot) -> str:
    """Compact one-line trace used by the notebook and the test report."""
    fault = snapshot.fault_code or "-"
    return (
        f"{snapshot.elapsed_ms:6d} ms | {snapshot.state:<14} | RUN={int(snapshot.run)} "
        f"Y0={int(snapshot.y0_run_lamp)} Y2={int(snapshot.y2_extend_solenoid)} | fault={fault}"
    )


def normal_cycle(plc: PusherSequence | None = None) -> dict:
    """Drive one complete teaching cycle with confirmation sensors."""
    plc = plc or PusherSequence()
    released = PlcInputs()
    plc.step(released, 100)
    visited = [plc.state]
    inputs = PlcInputs(start=True)
    plc.step(inputs, 100)
    visited.append(plc.state)
    inputs.start = False
    for _ in range(2):
        plc.step(inputs, 100)
        visited.append(plc.state)
    inputs.extended, inputs.retracted = True, False
    for _ in range(2):
        plc.step(inputs, 100)
        visited.append(plc.state)
    inputs.extended, inputs.retracted = False, True
    for _ in range(2):
        plc.step(inputs, 100)
        visited.append(plc.state)
    return {"final": plc.snapshot(), "visited": visited}


@dataclass
class MotorInterlock:
    """Mutually exclusive forward/reverse commands with conflict rejection.

    Both requests at the same time are rejected (both outputs OFF) instead of
    depending on scan order.  Real reversing contactors also need electrical
    and/or mechanical interlocking and a suitable safety design.
    """

    forward: bool = False
    reverse: bool = False
    conflict: bool = False

    def step(self, forward_req: bool, reverse_req: bool, stop_ok: bool = True) -> dict:
        if not stop_ok:
            self.forward = self.reverse = self.conflict = False
        elif forward_req and reverse_req:
            self.forward = self.reverse = False
            self.conflict = True
        else:
            self.forward = bool(forward_req)
            self.reverse = bool(reverse_req)
            self.conflict = False
        return {"forward": self.forward, "reverse": self.reverse, "conflict": self.conflict}


def interlock_allows(required_conditions: dict[str, bool], command: bool) -> bool:
    """A command is only issued when every interlock condition is true."""
    if not isinstance(required_conditions, dict) or not required_conditions:
        raise ValueError("required_conditions must be a non-empty dict")
    return bool(command) and all(bool(value) for value in required_conditions.values())


# --------------------------------------------------------------------------- #
# 7. camera optics and inspection timing (Day 9)
# --------------------------------------------------------------------------- #
def object_space_sampling_mm_per_px(field_of_view_mm: float, image_pixels: float) -> float:
    """Object-space size of one pixel: FOV across the sensor / pixels across it."""
    _positive("field_of_view_mm", field_of_view_mm)
    _positive("image_pixels", image_pixels)
    return field_of_view_mm / image_pixels


def defect_size_px(defect_mm: float, sampling_mm_per_px: float) -> float:
    """Approximate number of pixels covered by a defect (ignores optics and blur)."""
    _positive("defect_mm", defect_mm)
    _positive("sampling_mm_per_px", sampling_mm_per_px)
    return defect_mm / sampling_mm_per_px


def motion_blur_mm(speed_mm_s: float, exposure_s: float) -> float:
    """Object movement during one exposure: distance = speed * time."""
    _positive("speed_mm_s", speed_mm_s, allow_zero=True)
    _positive("exposure_s", exposure_s, allow_zero=True)
    return speed_mm_s * exposure_s


def motion_blur_px(speed_mm_s: float, exposure_s: float, sampling_mm_per_px: float) -> float:
    """Motion blur expressed in object-space pixels."""
    _positive("sampling_mm_per_px", sampling_mm_per_px)
    return motion_blur_mm(speed_mm_s, exposure_s) / sampling_mm_per_px


def exposure_time_s(target_blur_px: float, speed_mm_s: float, sampling_mm_per_px: float) -> float:
    """Exposure that limits blur on the object to ``target_blur_px`` pixels.

    Illustrative engineering target, not a guarantee of inspection performance.
    """
    _positive("target_blur_px", target_blur_px)
    _positive("speed_mm_s", speed_mm_s)
    _positive("sampling_mm_per_px", sampling_mm_per_px)
    return target_blur_px * sampling_mm_per_px / speed_mm_s


def line_rate_lps(speed_mm_s: float, sampling_mm_per_line: float) -> float:
    """Ideal line rate for a line-scan camera: speed / sampling along motion."""
    _positive("speed_mm_s", speed_mm_s)
    _positive("sampling_mm_per_line", sampling_mm_per_line)
    return speed_mm_s / sampling_mm_per_line


def frame_interval_move_mm(speed_mm_s: float, fps: float) -> float:
    """Material movement between consecutive nominal frames."""
    _positive("speed_mm_s", speed_mm_s)
    _positive("fps", fps)
    return speed_mm_s / fps


INSPECTION_RESULTS = ("OK", "NG", "INVALID")


def inspection_decision(result: str | None, *, image_available: bool = True,
                        inference_ok: bool = True, communication_ok: bool = True) -> str:
    """Map an inference result to an inspection decision.

    A missing image, a failed inference or a failed communication link yields
    INVALID.  INVALID must never be treated as OK; the machine response has to
    be designed and validated for the real equipment.
    """
    if not image_available or not inference_ok or not communication_ok:
        return "INVALID"
    if result not in ("OK", "NG"):
        return "INVALID"
    return result


def imaging_checklist() -> list[dict]:
    """Items that must be recorded to reproduce an imaging condition."""
    return [
        {"item_ja": "カメラ機種", "item_en": "camera model"},
        {"item_ja": "レンズ", "item_en": "lens"},
        {"item_ja": "作動距離", "item_en": "working distance"},
        {"item_ja": "視野", "item_en": "field of view"},
        {"item_ja": "カメラ角度", "item_en": "camera angle"},
        {"item_ja": "照明の種類", "item_en": "light type"},
        {"item_ja": "照明の位置", "item_en": "light position"},
        {"item_ja": "露光時間", "item_en": "exposure time"},
        {"item_ja": "ゲイン", "item_en": "gain"},
        {"item_ja": "フレームレート／ライン速度", "item_en": "frame rate or line rate"},
        {"item_ja": "材料速度", "item_en": "material speed"},
        {"item_ja": "画像解像度", "item_en": "image resolution"},
        {"item_ja": "代表的な欠陥サンプル", "item_en": "representative defect samples"},
        {"item_ja": "環境条件", "item_en": "environmental conditions"},
    ]
