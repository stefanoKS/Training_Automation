import sys
from pathlib import Path
sys.path.insert(0, str(Path("day07_09_support/examples").resolve()))
import automation_models as am

print(am.takt_time_s(420, 600))
print(am.effective_capacity_per_h(15, 0.85, 0.98))
print(am.friction_force_n(8, 0.25), am.design_force_n(19.62, 2), am.theoretical_bore_mm(39.24, 0.4))
print(am.motor_report())
print(am.load_report(am.pdf_electrical_example()))
print(am.payback_report())
print(am.describe_subnet("192.168.10.130", 25))
print(am.subnet_pair_report("192.168.1.10", "192.168.2.20", 24)["same_subnet"])
for r in am.commissioning_matrix():
    print(r.test_id, r.status, r.actual)

plc = am.PusherSequence()
i = am.PlcInputs(start=False)
plc.step(i, 100)
i.start = True
print(plc.step(i, 100))
i.start = False
print(plc.step(i, 100))
print(plc.step(i, 100))
for _ in range(60):
    s = plc.step(i, 50)
print("T0", s.t0_ms, s.y1_delayed_lamp, s.state)
