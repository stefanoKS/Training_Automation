"""Deterministic engineering models for the Day 7-9 automation course.

This module is the executable reference used by the lesson notebooks, the
offline simulations and the test suite.  Every function is deliberately small,
validates its inputs and states its assumptions.  Nothing here constitutes a
machine design, a safety validation or a manufacturer's selection.

Units
-----
* time: seconds (s), minutes (min), milliseconds (ms)
* length: millimetres (mm) except where a name says ``_m``
* mass: kilograms (kg)
* force: newtons (N)
* pressure: megapascals (MPa) in the teaching API; 1 MPa = 1e6 Pa
* torque: newton-metres (N·m)
* electrical: volts (V), amperes (A), watts (W)
* money: Japanese yen (JPY), a hypothetical training value
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
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


def _fraction(name: str, value: float, *, allow_zero: bool = True) -> float:
    _positive(name, value, allow_zero=allow_zero)
    if value > 1.0:
        raise ValueError(f"{name} must be between 0 and 1 (a fraction, not a percentage), got {value!r}")
    return float(value)


# --------------------------------------------------------------------------- #
# 1. production capacity
# --------------------------------------------------------------------------- #
def takt_time_s(available_min: float, required_pieces: float) -> float:
    """Target pace = available production time / required quantity.

    ``available_min`` is *net available* production time in minutes, excluding
    planned breaks and lunch.  The result is seconds per piece.
    """
    _positive("available_min", available_min)
    _positive("required_pieces", required_pieces)
    return available_min * 60.0 / required_pieces


def theoretical_capacity_per_h(cycle_s: float) -> float:
    """Machine-limited capacity with no downtime and no defects."""
    _positive("cycle_s", cycle_s)
    return SECONDS_PER_HOUR / cycle_s


def effective_capacity_per_h(cycle_s: float, availability: float, good_yield: float) -> float:
    """Approximate good-piece output: theoretical x availability x good yield.

    ``availability`` and ``good_yield`` are fractions (0.85, not 85).
    This is a planning estimate, not a guarantee; it does not model ramp-up,
    changeover loss in detail, or lot-size effects.
    """
    return theoretical_capacity_per_h(cycle_s) * _fraction("availability", availability) * _fraction(
        "good_yield", good_yield
    )


def capacity_report(
    available_min: float = 420.0,
    required_pieces: float = 600.0,
    cycle_s: float = 15.0,
    availability: float = 0.85,
    good_yield: float = 0.98,
) -> dict:
    """All capacity numbers used by lesson 07-01, with the formula inputs."""
    takt = takt_time_s(available_min, required_pieces)
    theoretical = theoretical_capacity_per_h(cycle_s)
    effective = effective_capacity_per_h(cycle_s, availability, good_yield)
    required_per_h = required_pieces / (available_min / 60.0)
    return {
        "available_min": available_min,
        "required_pieces": required_pieces,
        "takt_s": takt,
        "cycle_s": cycle_s,
        "cycle_meets_takt": cycle_s <= takt,
        "required_pieces_per_h": required_per_h,
        "theoretical_per_h": theoretical,
        "availability": availability,
        "good_yield": good_yield,
        "effective_per_h": effective,
        "effective_meets_required": effective >= required_per_h,
        "cycle_utilisation": cycle_s / takt,
    }


def capacity_table(cycle_values: list[float], availability: float, good_yield: float) -> list[dict]:
    """Rows for the interactive capacity chart/table."""
    rows = []
    for cycle in cycle_values:
        _positive("cycle_s", cycle)
        rows.append(
            {
                "cycle_s": float(cycle),
                "theoretical_per_h": theoretical_capacity_per_h(cycle),
                "effective_per_h": effective_capacity_per_h(cycle, availability, good_yield),
            }
        )
    return rows


# --------------------------------------------------------------------------- #
# 2. mechanics: friction, cylinder, motor
# --------------------------------------------------------------------------- #
def friction_force_n(mass_kg: float, friction_coefficient: float, gravity: float = GRAVITY) -> float:
    """Sliding friction estimate F = mu * m * g on a horizontal surface.

    This is the force needed to keep a workpiece sliding at constant speed.
    It ignores acceleration, impact, guide resistance, misalignment and the
    difference between static and sliding friction.
    """
    _positive("mass_kg", mass_kg)
    _positive("friction_coefficient", friction_coefficient, allow_zero=True)
    _positive("gravity", gravity)
    return friction_coefficient * mass_kg * gravity


def design_force_n(friction_n: float, factor: float) -> float:
    """Apply an explicit teaching safety factor to a friction estimate."""
    _positive("friction_n", friction_n, allow_zero=True)
    if factor < 1.0:
        raise ValueError("factor must be >= 1.0; a value below 1 removes margin instead of adding it")
    return friction_n * float(factor)


def theoretical_bore_mm(force_n: float, pressure_mpa: float) -> float:
    """Minimum theoretical bore for F = P * pi * D^2 / 4 (push side).

    This is a lower bound under one simplified assumption.  It is NOT a
    catalogue selection: the pressure at the piston, load factor, speed,
    side load, cushioning and manufacturer rules must still be checked.
    """
    _positive("force_n", force_n)
    _positive("pressure_mpa", pressure_mpa)
    pressure_pa = pressure_mpa * 1e6
    diameter_m = sqrt(4.0 * force_n / (pi * pressure_pa))
    return diameter_m * 1000.0


def cylinder_force_n(bore_mm: float, pressure_mpa: float, rod_mm: float = 0.0) -> float:
    """Theoretical push (rod_mm=0) or pull force of a double-acting cylinder."""
    _positive("bore_mm", bore_mm)
    _positive("pressure_mpa", pressure_mpa)
    _positive("rod_mm", rod_mm, allow_zero=True)
    if rod_mm >= bore_mm:
        raise ValueError("rod_mm must be smaller than bore_mm")
    bore_m = bore_mm / 1000.0
    rod_m = rod_mm / 1000.0
    area = pi * (bore_m**2 - rod_m**2) / 4.0
    return pressure_mpa * 1e6 * area


def cylinder_report(
    mass_kg: float = 8.0,
    friction_coefficient: float = 0.25,
    force_factor: float = 2.0,
    pressure_mpa: float = 0.4,
    stroke_mm: float = 100.0,
    rod_mm: float = 6.0,
    catalog_bore_mm: float = 16.0,
) -> dict:
    """Cylinder sizing report with the theoretical minimum kept separate."""
    friction = friction_force_n(mass_kg, friction_coefficient)
    design = design_force_n(friction, force_factor)
    bore = theoretical_bore_mm(design, pressure_mpa)
    report = {
        "mass_kg": mass_kg,
        "friction_coefficient": friction_coefficient,
        "friction_n": friction,
        "force_factor": force_factor,
        "design_force_n": design,
        "pressure_mpa": pressure_mpa,
        "theoretical_bore_mm": bore,
        "stroke_mm": stroke_mm,
        "rod_mm": rod_mm,
        "catalog_bore_mm": catalog_bore_mm,
        "catalog_is_example_only": True,
    }
    if catalog_bore_mm:
        report["catalog_push_force_n"] = cylinder_force_n(catalog_bore_mm, pressure_mpa)
        report["catalog_pull_force_n"] = cylinder_force_n(catalog_bore_mm, pressure_mpa, rod_mm)
        report["catalog_margin"] = report["catalog_push_force_n"] / design
    return report


def motor_torque_nm(power_w: float, speed_rpm: float) -> float:
    """Shaft torque from mechanical power: P = T * omega, omega = 2*pi*n/60."""
    _positive("power_w", power_w)
    _positive("speed_rpm", speed_rpm)
    omega = 2.0 * pi * speed_rpm / 60.0
    return power_w / omega


def reducer_output_speed_rpm(input_rpm: float, ratio: float) -> float:
    """Ideal reducer output speed (ignoring slip and efficiency)."""
    _positive("input_rpm", input_rpm)
    _positive("ratio", ratio)
    return input_rpm / ratio


def reducer_output_torque_nm(input_torque_nm: float, ratio: float, efficiency: float = 1.0) -> float:
    """Output torque = input torque x ratio x efficiency.

    ``efficiency`` is an explicit assumption.  The PDF example gives no
    efficiency, so 1.0 is the ideal case; lesson 07-03 also shows 0.90 as an
    added, clearly labelled assumption.
    """
    _positive("input_torque_nm", input_torque_nm)
    _positive("ratio", ratio)
    _fraction("efficiency", efficiency, allow_zero=False)
    return input_torque_nm * ratio * efficiency


def motor_report(
    power_w: float = 60.0,
    speed_rpm: float = 1200.0,
    ratio: float = 20.0,
    efficiency: float = 0.90,
) -> dict:
    torque = motor_torque_nm(power_w, speed_rpm)
    ideal_torque = reducer_output_torque_nm(torque, ratio, 1.0)
    return {
        "power_w": power_w,
        "speed_rpm": speed_rpm,
        "ratio": ratio,
        "motor_torque_nm": torque,
        "output_speed_rpm": reducer_output_speed_rpm(speed_rpm, ratio),
        "ideal_output_torque_nm": ideal_torque,
        "efficiency": efficiency,
        "delivered_output_torque_nm": reducer_output_torque_nm(torque, ratio, efficiency),
        "efficiency_is_added_assumption": True,
    }


# --------------------------------------------------------------------------- #
# 3. electrical loads
# --------------------------------------------------------------------------- #
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


def total_load_current_a(loads: list[Load]) -> float:
    return sum(load.total_current_a() for load in loads)


def load_report(loads: list[Load], supply_margin: float = 0.25) -> dict:
    """Steady-state load budget with an explicitly separate sizing margin.

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
        }
        for load in loads
    ]
    _positive("supply_margin", supply_margin, allow_zero=True)
    steady = sum(row["total_current_a"] for row in rows)
    return {
        "rows": rows,
        "steady_total_a": steady,
        "margin_fraction": supply_margin,
        "planning_current_a": steady * (1.0 + supply_margin),
        "is_sizing_approval": False,
    }


def pdf_electrical_example() -> list[Load]:
    """The source PDF page 21 exercise: 3 W x 2 lamps, 0.06 A x 3 sensors, 0.15 A x 2 valves."""
    return [
        Load("lamp", 2, 24.0, power_w=3.0),
        Load("sensor", 3, 24.0, current_a=0.06),
        Load("solenoid valve", 2, 24.0, current_a=0.15),
    ]


# --------------------------------------------------------------------------- #
# 4. cost and payback
# --------------------------------------------------------------------------- #
def annual_labour_saving_jpy(
    seconds_saved_per_occurrence: float,
    occurrences_per_day: float,
    working_days_per_year: float,
    hourly_rate_jpy: float,
) -> dict:
    """Hypothetical labour-time value of a time reduction.

    It is not realised cash unless the freed time is actually redeployed or
    overtime is reduced.  Maintenance, energy and consumables are excluded.
    """
    _positive("seconds_saved_per_occurrence", seconds_saved_per_occurrence, allow_zero=True)
    _positive("occurrences_per_day", occurrences_per_day, allow_zero=True)
    _positive("working_days_per_year", working_days_per_year, allow_zero=True)
    _positive("hourly_rate_jpy", hourly_rate_jpy, allow_zero=True)
    seconds_per_day = seconds_saved_per_occurrence * occurrences_per_day
    hours_per_day = seconds_per_day / 3600.0
    hours_per_year = hours_per_day * working_days_per_year
    return {
        "seconds_per_day": seconds_per_day,
        "minutes_per_day": seconds_per_day / 60.0,
        "hours_per_day": hours_per_day,
        "hours_per_year": hours_per_year,
        "annual_value_jpy": hours_per_year * hourly_rate_jpy,
    }


def payback_years(investment_jpy: float, annual_net_saving_jpy: float) -> float:
    _positive("investment_jpy", investment_jpy)
    _positive("annual_net_saving_jpy", annual_net_saving_jpy)
    return investment_jpy / annual_net_saving_jpy


def payback_report(
    seconds_saved: float = 12.0,
    occurrences_per_day: float = 180.0,
    days_per_year: float = 220.0,
    hourly_rate_jpy: float = 2400.0,
    investment_jpy: float = 450_000.0,
    annual_operating_cost_jpy: float = 0.0,
) -> dict:
    saving = annual_labour_saving_jpy(seconds_saved, occurrences_per_day, days_per_year, hourly_rate_jpy)
    net = saving["annual_value_jpy"] - annual_operating_cost_jpy
    report = {**saving, "investment_jpy": investment_jpy, "annual_operating_cost_jpy": annual_operating_cost_jpy,
              "annual_net_value_jpy": net}
    report["payback_years"] = payback_years(investment_jpy, net) if net > 0 else float("inf")
    return report


# --------------------------------------------------------------------------- #
# 4b. canonical fictional I/O assignment (single source for Days 8 and 9)
# --------------------------------------------------------------------------- #
CANONICAL_IO = (
    {"address": "X0", "kind": "input", "device": "START pushbutton", "normal": "OFF; momentary ON when pressed"},
    {"address": "X1", "kind": "input", "device": "STOP_OK permission from physical NC STOP", "normal": "ON while healthy"},
    {"address": "X2", "kind": "input", "device": "retracted position confirmation", "normal": "ON at retracted end"},
    {"address": "X3", "kind": "input", "device": "extended position confirmation", "normal": "ON at extended end"},
    {"address": "M0", "kind": "internal", "device": "RUN internal state bit", "normal": "OFF at power-up"},
    {"address": "Y0", "kind": "output", "device": "RUN indicator lamp", "normal": "OFF when not running"},
    {"address": "Y1", "kind": "output", "device": "delayed indicator lamp (T0 done)", "normal": "OFF until 3 s of RUN"},
    {"address": "Y2", "kind": "output", "device": "EXTEND solenoid command", "normal": "OFF = spring-return retract (training valve)"},
    {"address": "T0", "kind": "timer", "device": "3 s on-delay timer for Y1", "normal": "0 ms when RUN is off"},
)

CANONICAL_IO_DEVICE_NAMES = {row["address"]: row["device"] for row in CANONICAL_IO}


def validate_io(rows) -> list[str]:
    """Return consistency problems in an I/O table.

    Checks duplicate addresses and the two classic mistakes in this course:
    reusing Y1 for a solenoid and describing X1 as a normal OFF pushbutton.
    """
    problems: list[str] = []
    addresses = [row["address"] for row in rows]
    duplicates = sorted({address for address in addresses if addresses.count(address) > 1})
    if duplicates:
        problems.append(f"duplicate addresses: {', '.join(duplicates)}")
    for row in rows:
        address = row["address"]
        device = str(row["device"]).lower()
        if address == "Y1" and ("solenoid" in device or "valve" in device or "電磁弁" in str(row["device"])):
            problems.append("Y1 is reserved for the delayed indicator lamp; use Y2 for the extend solenoid")
        if address == "X1" and str(row["normal"]).lower().startswith("off"):
            problems.append("X1 STOP_OK is ON while the physical NC stop is healthy; its normal state is ON")
    expected = {row["address"] for row in CANONICAL_IO}
    missing = sorted(expected - set(addresses))
    if missing:
        problems.append(f"missing addresses: {', '.join(missing)}")
    return problems


# --------------------------------------------------------------------------- #
# 5. IPv4 and subnets
# --------------------------------------------------------------------------- #
def parse_ipv4(text: str) -> int:
    """Parse dotted-decimal IPv4 into an integer, rejecting leading zeros."""
    if not isinstance(text, str):
        raise ValueError(f"IPv4 address must be a string, got {text!r}")
    parts = text.strip().split(".")
    if len(parts) != 4:
        raise ValueError(f"IPv4 address needs four octets: {text!r}")
    value = 0
    for part in parts:
        if not part.isdigit() or (len(part) > 1 and part.startswith("0")):
            raise ValueError(f"invalid IPv4 octet {part!r} in {text!r}")
        octet = int(part)
        if octet > 255:
            raise ValueError(f"IPv4 octet out of range: {text!r}")
        value = (value << 8) | octet
    return value


def format_ipv4(value: int) -> str:
    if not 0 <= value <= 0xFFFFFFFF:
        raise ValueError("IPv4 integer out of range")
    return ".".join(str((value >> shift) & 0xFF) for shift in (24, 16, 8, 0))


def prefix_from_mask(mask: str) -> int:
    value = parse_ipv4(mask)
    bits = f"{value:032b}"
    if "01" in bits:
        raise ValueError(f"subnet mask is not contiguous: {mask!r}")
    return bits.count("1")


def mask_from_prefix(prefix: int) -> str:
    if not isinstance(prefix, int) or isinstance(prefix, bool) or not 0 <= prefix <= 32:
        raise ValueError("prefix must be an integer from 0 to 32")
    value = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF if prefix else 0
    return format_ipv4(value)


def network_address(ip: str, prefix: int) -> int:
    mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF if prefix else 0
    return parse_ipv4(ip) & mask


def broadcast_address(ip: str, prefix: int) -> int:
    mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF if prefix else 0
    return network_address(ip, prefix) | (~mask & 0xFFFFFFFF)


def host_range(ip: str, prefix: int) -> tuple[str | None, str | None, int, str]:
    """Return (first, last, usable_count, exclusion_rule) for the subnet.

    /31 is handled per RFC 3021 (point-to-point, both addresses usable) and
    /32 is a single host.  For /0-/30 the network and broadcast addresses are
    excluded in the conventional way.
    """
    if not isinstance(prefix, int) or isinstance(prefix, bool) or not 0 <= prefix <= 32:
        raise ValueError("prefix must be an integer from 0 to 32")
    network = network_address(ip, prefix)
    broadcast = broadcast_address(ip, prefix)
    if prefix == 32:
        text = format_ipv4(network)
        return text, text, 1, "/32 is a single host; there is no network/broadcast pair to exclude."
    if prefix == 31:
        return (
            format_ipv4(network),
            format_ipv4(broadcast),
            2,
            "/31 uses RFC 3021 point-to-point addressing: both addresses are usable.",
        )
    first = network + 1
    last = broadcast - 1
    count = max(0, last - first + 1)
    return (
        format_ipv4(first),
        format_ipv4(last),
        count,
        "Conventional subnet: the all-zeros network address and the all-ones broadcast address are excluded.",
    )


def describe_subnet(ip: str, prefix: int) -> dict:
    first, last, count, rule = host_range(ip, prefix)
    network = network_address(ip, prefix)
    broadcast = broadcast_address(ip, prefix)
    return {
        "ip": ip,
        "prefix": prefix,
        "mask": mask_from_prefix(prefix),
        "network": format_ipv4(network),
        "broadcast": format_ipv4(broadcast),
        "first_host": first,
        "last_host": last,
        "usable_hosts": count,
        "exclusion_rule": rule,
        "is_host_address": first is not None and parse_ipv4(first) <= parse_ipv4(ip) <= parse_ipv4(last),
        "cidr": f"{format_ipv4(network)}/{prefix}",
    }


def same_subnet(ip_a: str, ip_b: str, prefix: int) -> bool:
    return network_address(ip_a, prefix) == network_address(ip_b, prefix)


def subnet_pair_report(ip_a: str, ip_b: str, prefix: int) -> dict:
    a = describe_subnet(ip_a, prefix)
    b = describe_subnet(ip_b, prefix)
    return {
        "a": a,
        "b": b,
        "same_subnet": a["cidr"] == b["cidr"],
        "explanation": (
            f"{ip_a}/{prefix} is in {a['cidr']} and {ip_b}/{prefix} is in {b['cidr']}."
            + (" They share the same network, so they can communicate directly if the physical link, "
               "VLAN and host configuration also allow it." if a["cidr"] == b["cidr"] else
               " They are in different networks, so a router or routing configuration is normally required.")
        ),
    }


# --------------------------------------------------------------------------- #
# 6. PLC sequence simulation
# --------------------------------------------------------------------------- #
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
    y1_delayed_lamp: bool
    y2_extend_solenoid: bool
    t0_ms: int
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
    Y1          delayed indicator (T0 done)
    Y2          extend solenoid command (OFF = spring-return retract)
    T0          3 s on-delay timer for Y1
    ==========  ==========================================

    Restart rule: a RUN state is never resumed automatically.  After power-up,
    a STOP or a fault reset the program requires the START input to be released
    and pressed again while the retracted position is confirmed.
    """

    timer_ms: int = 3000
    motion_timeout_ms: int = 3000
    max_cycles: int = 10_000

    def __post_init__(self) -> None:
        for name in ("timer_ms", "motion_timeout_ms"):
            value = getattr(self, name)
            if not isinstance(value, int) or value <= 0:
                raise ValueError(f"{name} must be a positive integer number of milliseconds")
        self.power_on()

    # ------------------------------------------------------------------ setup
    def power_on(self) -> PlcSnapshot:
        """Initialise as a cold power-up with START treated as possibly held."""
        self.state = "IDLE"
        self.run = False
        self.t0_ms = 0
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

    # ------------------------------------------------------------------ core
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
            self.t0_ms = 0
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
            self.t0_ms = 0
            self.motion_ms = 0
            self.fresh_start_required = True
            self.start_armed = False
            self.reset_prev = bool(reset)
            self.start_prev = inputs.start
            return self.snapshot()

        # Re-arm only after START is released and the machine is settled.
        if not inputs.start and self.state in ("IDLE", "COMPLETE"):
            self.start_armed = True

        # Self-holding timer T0 runs with the RUN state.
        if self.run:
            self.t0_ms = min(self.t0_ms + dt_ms, self.timer_ms)
        else:
            self.t0_ms = 0

        started_this_step = False
        start_edge = inputs.start and not self.start_prev
        if start_edge and self.start_armed and self.state in ("IDLE", "COMPLETE"):
            if not inputs.retracted or inputs.extended:
                # Not at a confirmed safe starting position: refuse the start.
                self.start_armed = False
            else:
                self.transition_to("READY")
                self.run = True
                self.t0_ms = 0
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
        self.t0_ms = 0
        self.motion_ms = 0
        self.fault_code = code
        self.fresh_start_required = True
        self.start_armed = False
        self.fault_reason = reason

    # ------------------------------------------------------------- reporting
    @property
    def y2_extend_solenoid(self) -> bool:
        return self.state in ("EXTEND", "WAIT_EXTENDED")

    @property
    def y0_run_lamp(self) -> bool:
        return self.run

    @property
    def y1_delayed_lamp(self) -> bool:
        return self.run and self.t0_ms >= self.timer_ms

    def snapshot(self) -> PlcSnapshot:
        return PlcSnapshot(
            state=self.state,
            run=self.run,
            y0_run_lamp=self.y0_run_lamp,
            y1_delayed_lamp=self.y1_delayed_lamp,
            y2_extend_solenoid=self.y2_extend_solenoid,
            t0_ms=self.t0_ms,
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
        f"Y0={int(snapshot.y0_run_lamp)} Y1={int(snapshot.y1_delayed_lamp)} "
        f"Y2={int(snapshot.y2_extend_solenoid)} | T0={snapshot.t0_ms:4d} ms | fault={fault}"
    )


# --------------------------------------------------------------------------- #
# 7. commissioning test simulation
# --------------------------------------------------------------------------- #
TEST_STATUSES = ("PASS", "FAIL", "NOT TESTED", "BLOCKED")


@dataclass
class TestSpec:
    test_id: str
    requirement_id: str
    title_ja: str
    title_en: str
    gate: str
    preconditions: str
    procedure: str
    expected: str
    scenario: str
    evaluator: str


@dataclass
class TestRecord:
    test_id: str
    requirement_id: str
    preconditions: str
    procedure: str
    expected: str
    actual: str
    status: str
    evidence: str
    operator: str
    date: str
    corrective_action: str = ""

    def __post_init__(self) -> None:
        if self.status not in TEST_STATUSES:
            raise ValueError(f"invalid test status {self.status!r}")

    def as_row(self) -> list[str]:
        return [
            self.test_id,
            self.requirement_id,
            self.expected,
            self.actual,
            self.status,
            self.evidence,
        ]


TRAINING_DATE = "2026-11-23"  # build/session date; simulation evidence, not a real measurement


def _drive_normal(plc: PusherSequence, *, stop_at_ms: int | None = None, stop_hold: bool = False) -> dict:
    """Drive one normal cycle by feeding position feedback after each command."""
    inputs = PlcInputs(start=False, stop_ok=True, retracted=True, extended=False)
    visited = [plc.state]
    for tick in range(200):
        elapsed = tick * 50
        # position feedback follows the last command with a small delay
        if plc.y2_extend_solenoid and plc.state in ("EXTEND", "WAIT_EXTENDED") and tick > 4:
            inputs.retracted, inputs.extended = False, True
        if plc.state in ("RETRACT", "WAIT_RETRACTED") and plc.run and tick > 8:
            inputs.retracted, inputs.extended = True, False
        if stop_at_ms is not None and elapsed >= stop_at_ms and stop_hold:
            inputs.stop_ok = False
        if elapsed == 150:
            inputs.start = True
        if elapsed >= 300:
            inputs.start = False
        snapshot = plc.step(inputs, 50)
        visited.append(snapshot.state)
        if snapshot.state == "COMPLETE":
            break
    return {"final": plc.snapshot(), "visited": visited}


def _drive_timeout(plc: PusherSequence, *, conflict: bool = False, slow: bool = False) -> dict:
    inputs = PlcInputs(start=False, stop_ok=True, retracted=True, extended=False)
    visited = [plc.state]
    for tick in range(300):
        elapsed = tick * 50
        if conflict and tick > 10:
            inputs.retracted, inputs.extended = True, True
        elif plc.y2_extend_solenoid and plc.state == "WAIT_EXTENDED" and tick > 4:
            if slow:
                inputs.retracted, inputs.extended = False, elapsed > 4000
            else:
                inputs.retracted, inputs.extended = False, False  # sensor never confirms
        if elapsed == 150:
            inputs.start = True
        if elapsed >= 300:
            inputs.start = False
        snapshot = plc.step(inputs, 50)
        visited.append(snapshot.state)
        if snapshot.state == "FAULT":
            break
    return {"final": plc.snapshot(), "visited": visited}


def _drive_power_restore(plc: PusherSequence) -> dict:
    # START is physically held while power is restored.  The expected result is
    # that nothing starts; a subsequent release and press is a separate event.
    inputs = PlcInputs(start=True, stop_ok=True, retracted=True, extended=False)
    plc.power_on()
    for _ in range(20):
        plc.step(inputs, 100)
    held = plc.snapshot()
    inputs.start = False
    plc.step(inputs, 100)
    inputs.start = True
    after_release_press = plc.step(inputs, 100)
    return {"final": held, "after_release_press": after_release_press,
            "visited": ["POWER_ON", held.state, after_release_press.state]}


def run_scenario(name: str) -> dict:
    plc = PusherSequence()
    if name == "normal_cycle":
        return _drive_normal(plc)
    if name == "timer_only":
        inputs = PlcInputs(start=False, stop_ok=True, retracted=True, extended=False)
        trace = [plc.step(inputs, 50) for _ in range(3)]
        inputs.start = True
        trace.append(plc.step(inputs, 50))       # READY
        inputs.start = False
        for _ in range(3):                        # EXTEND, WAIT_EXTENDED
            trace.append(plc.step(inputs, 50))
        for _ in range(70):                       # keep RUN, timer accumulates
            trace.append(plc.step(inputs, 50))
        return {"final": plc.snapshot(), "trace": trace, "visited": [s.state for s in trace]}
    if name == "stop_during_timer":
        inputs = PlcInputs(start=False, stop_ok=True, retracted=True, extended=False)
        for _ in range(2):
            plc.step(inputs, 100)
        inputs.start = True
        plc.step(inputs, 100)
        inputs.start = False
        for _ in range(15):
            plc.step(inputs, 100)
        inputs.stop_ok = False
        snap = plc.step(inputs, 100)
        return {"final": snap, "visited": [snap.state]}
    if name == "sensor_stuck_off":
        return _drive_timeout(plc)
    if name == "retract_stuck":
        return _drive_retract_timeout(plc)
    if name == "sensor_conflict":
        return _drive_timeout(plc, conflict=True)
    if name == "motion_slow":
        return _drive_timeout(plc, slow=True)
    if name == "power_restore_start_held":
        return _drive_power_restore(plc)
    if name == "fault_reset":
        result = _drive_timeout(plc)
        inputs = PlcInputs(start=False, stop_ok=True, retracted=True, extended=False)
        plc.step(inputs, 100, reset=False)
        plc.step(inputs, 100, reset=True)
        plc.step(inputs, 100, reset=False)
        return {"final": plc.snapshot(), "visited": result["visited"] + ["RESET"]}
    raise ValueError(f"unknown scenario {name!r}")


def _drive_retract_timeout(plc: PusherSequence) -> dict:
    """Drive a normal extend, then keep X2 OFF so the retract confirmation never arrives."""
    inputs = PlcInputs(start=False, stop_ok=True, retracted=True, extended=False)
    visited = [plc.state]
    for tick in range(300):
        elapsed = tick * 50
        if plc.state in ("EXTEND", "WAIT_EXTENDED") and tick > 4:
            inputs.retracted, inputs.extended = False, True
        if plc.state in ("RETRACT", "WAIT_RETRACTED"):
            inputs.retracted, inputs.extended = False, False  # X2 stuck OFF
        if elapsed == 150:
            inputs.start = True
        if elapsed >= 300:
            inputs.start = False
        snapshot = plc.step(inputs, 50)
        visited.append(snapshot.state)
        if snapshot.state == "FAULT":
            break
    return {"final": plc.snapshot(), "visited": visited}


def normal_cycle(plc: PusherSequence | None = None) -> dict:
    """Run one normal cycle with position feedback and return the trace.

    Public wrapper used by the lesson notebook; the driving logic is the same
    deterministic code used by the commissioning test matrix.
    """
    return _drive_normal(plc or PusherSequence())


def _eval(record: TestRecord, scenario_result: dict, name: str) -> TestRecord:
    final = scenario_result["final"]
    if name == "normal_cycle":
        ok = final.state == "COMPLETE" and final.cycle_count == 1
        record.actual = f"final state={final.state}, cycles={final.cycle_count}"
    elif name == "timer_only":
        trace = scenario_result["trace"]
        y1_at = next((s.t0_ms for s in trace if s.y1_delayed_lamp), None)
        at_one_second = next((s for s in trace if s.elapsed_ms >= 1000), final)
        if record.test_id == "T02":
            ok = (
                final.cycle_count == 1
                and at_one_second.run
                and at_one_second.y0_run_lamp
                and not at_one_second.y1_delayed_lamp
            )
            record.actual = (
                f"at {at_one_second.elapsed_ms} ms: RUN={at_one_second.run}, "
                f"Y0={at_one_second.y0_run_lamp}, Y1={at_one_second.y1_delayed_lamp}"
            )
        elif record.test_id == "T03":
            at_two_seconds = next((s for s in trace if s.elapsed_ms >= 2000), final)
            ok = (
                at_one_second.run and at_one_second.y0_run_lamp
                and at_two_seconds.run and at_two_seconds.y0_run_lamp
                and at_two_seconds.cycle_count == 1
            )
            record.actual = (
                f"START released; RUN={at_two_seconds.run}, Y0={at_two_seconds.y0_run_lamp} "
                f"at {at_two_seconds.elapsed_ms} ms"
            )
        else:
            ok = y1_at == 3000 and final.cycle_count == 1
            record.actual = f"first Y1 at T0={y1_at} ms; timer stays latched while RUN is held"
    elif name == "stop_during_timer":
        ok = final.state == "IDLE" and not final.run and final.t0_ms == 0
        record.actual = f"state={final.state}, run={final.run}, T0={final.t0_ms} ms"
    elif name == "sensor_stuck_off":
        ok = final.fault_code == "F001"
        record.actual = f"fault={final.fault_code}, state={final.state}"
    elif name == "sensor_conflict":
        ok = final.fault_code == "F002"
        record.actual = f"fault={final.fault_code}, state={final.state}"
    elif name == "motion_slow":
        ok = final.fault_code == "F001"
        record.actual = f"fault={final.fault_code} after timeout"
    elif name == "power_restore_start_held":
        after = scenario_result.get("after_release_press")
        ok = (
            final.state == "IDLE"
            and not final.run
            and after is not None
            and after.state == "READY"
            and after.run
        )
        record.actual = (
            f"held START: state={final.state}, run={final.run}; "
            f"new press after release: state={after.state if after else 'n/a'}, run={after.run if after else 'n/a'}"
        )
    elif name == "fault_reset":
        ok = final.state == "IDLE" and final.fault_code is None and not final.run
        record.actual = f"state={final.state}, fault={final.fault_code}, run={final.run}"
    else:
        ok = False
        record.actual = "not evaluated"
    record.status = "PASS" if ok else "FAIL"
    return record


TEST_SPECS = [
    TestSpec("T01", "R-01", "電源投入時に自動起動しない", "No automatic start at power-up", "G3",
             "Power available; START may be held.", "Apply power with START held for 1 s.",
             "IDLE, RUN off, no motion output.", "power_restore_start_held", "power restore"),
    TestSpec("T02", "R-02", "STARTで運転状態になる", "START establishes RUN", "G3",
             "Retracted confirmed; STOP_OK on.", "Press and release START.",
             "RUN on, Y0 on, Y1 off before 3 s.", "timer_only", "timer"),
    TestSpec("T03", "R-03", "STARTを離しても自己保持する", "RUN is self-held after START release", "G3",
             "RUN established.", "Release START and scan for 1 s.",
             "RUN remains on until STOP or fault.", "timer_only", "timer"),
    TestSpec("T04", "R-04", "3秒タイマーでY1点灯", "Y1 turns on at 3 s", "G3",
             "RUN established.", "Hold RUN for 3 s.", "Y1 on exactly at T0 = 3000 ms.",
             "timer_only", "timer"),
    TestSpec("T05", "R-05", "停止要求がタイマーより優先", "STOP has priority over the timer", "G3",
             "RUN and T0 running.", "Turn STOP_OK off before 3 s.",
             "RUN off, Y0/Y1 off, T0 reset to 0.", "stop_during_timer", "stop"),
    TestSpec("T06", "R-06", "前進端確認で後退へ移る", "Extended confirmation advances the sequence", "G3",
             "START accepted.", "Feed X3 ON and X2 OFF after extend command.",
             "RETRACT then COMPLETE after X2 returns.", "normal_cycle", "sequence"),
    TestSpec("T07", "R-07", "前進端未確認はタイムアウト異常", "Missing extend confirmation times out", "G3",
             "START accepted.", "Keep X3 OFF beyond 3 s.", "FAULT F001; Y2 off.",
             "sensor_stuck_off", "fault"),
    TestSpec("T08", "R-08", "前後端同時ONは異常", "Conflicting position sensors are a fault", "G3",
             "Power on.", "Force X2 and X3 ON together.", "FAULT F002; outputs off.",
             "sensor_conflict", "fault"),
    TestSpec("T09", "R-09", "故障リセットで動作しない", "Fault reset does not move the machine", "G3",
             "FAULT active; START released.", "Reset the fault.", "IDLE, all outputs off, START still required.",
             "fault_reset", "fault"),
    TestSpec("T10", "R-10", "動作遅れもタイムアウトで検出", "Slow motion is caught by the timeout", "G3",
             "START accepted.", "Confirm X3 after 4 s.", "FAULT F001 at the timeout.",
             "motion_slow", "fault"),
    TestSpec("T11", "R-11", "実機の通電試験は未実施", "Energised hardware test not performed", "G5",
             "Requires approved equipment, isolation procedure and qualified supervision.",
             "Perform an approved energised functional test.", "Only a supervised, approved test can pass.",
             "blocked", "hardware"),
    TestSpec("T12", "R-12", "安全機能の検証は対象外", "Safety-function validation is out of scope", "G5",
             "Requires a risk assessment and a validated safety system.",
             "Validate the protective stop function.", "Out of scope for this course.",
             "blocked", "safety"),
]


def run_test_spec(spec: TestSpec) -> TestRecord:
    record = TestRecord(
        test_id=spec.test_id,
        requirement_id=spec.requirement_id,
        preconditions=spec.preconditions,
        procedure=spec.procedure,
        expected=spec.expected,
        actual="",
        status="NOT TESTED",
        evidence="offline deterministic simulation" if spec.scenario != "blocked" else "no hardware / no approval",
        operator="training simulator",
        date=TRAINING_DATE,
    )
    if spec.scenario == "blocked":
        record.status = "BLOCKED"
        record.actual = "Not performed in the classroom; requires supervised hardware and approval."
        return record
    result = run_scenario(spec.scenario)
    return _eval(record, result, spec.scenario)


def commissioning_matrix() -> list[TestRecord]:
    return [run_test_spec(spec) for spec in TEST_SPECS]


def matrix_markdown(records: list[TestRecord]) -> str:
    lines = ["| Test | Req | Expected | Actual | Status | Evidence |", "|---|---|---|---|---|---|"]
    for record in records:
        lines.append("| " + " | ".join(record.as_row()) + " |")
    return "\n".join(lines)
