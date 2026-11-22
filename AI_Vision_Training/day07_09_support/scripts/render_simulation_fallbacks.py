"""Render static fallback screenshots of the offline simulations and check for JS errors.

Run from any directory:
    python AI_Vision_Training\\day07_09_support\\scripts\\render_simulation_fallbacks.py

Requires Playwright and a locally installed Chrome or Edge. Each simulation is opened
from disk (file://), driven through a few interactions, and screenshotted so that the
lesson keeps a static visual even where JavaScript is unavailable.
"""

from __future__ import annotations

import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
SIMULATIONS = ROOT / "day07_09_support" / "simulations"
FALLBACK = SIMULATIONS / "fallback"

BROWSERS = (
    Path("C:/Program Files/Google/Chrome/Application/chrome.exe"),
    Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"),
)


def exercise(page, name: str) -> None:
    """Apply a small interaction so the screenshot shows a meaningful state."""
    if name == "sim_ladder_logic":
        page.click('button[data-kind="hold"]')
        page.check("#cX0")
        page.wait_for_timeout(150)
    elif name == "sim_machine_sequence":
        page.click("#bStart")
        page.wait_for_timeout(120)
        page.click("#bStart")
        page.wait_for_timeout(120)
    elif name == "sim_sensor_signals":
        page.check("#presence")
        page.wait_for_timeout(120)
    elif name == "sim_ai_result_protocol":
        page.select_option("#type", "TIMEOUT")
        page.click("#bSend")
        page.wait_for_timeout(120)


def main() -> int:
    chrome = next((candidate for candidate in BROWSERS if candidate.exists()), None)
    if chrome is None:
        print("Chrome or Edge not found; cannot render fallbacks", file=sys.stderr)
        return 1
    FALLBACK.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, executable_path=str(chrome))
        try:
            page = browser.new_page(viewport={"width": 1100, "height": 1000}, device_scale_factor=1.5)
            page.on("pageerror", lambda error: errors.append(str(error)))
            for html in sorted(SIMULATIONS.glob("sim_*.html")):
                page.goto(html.as_uri())
                page.evaluate("document.fonts.ready")
                exercise(page, html.stem)
                page.screenshot(path=str(FALLBACK / f"{html.stem}.png"), full_page=True)
                print(f"Rendered {html.stem}.png")
        finally:
            browser.close()
    if errors:
        print("Browser errors:\n" + "\n".join(errors), file=sys.stderr)
        return 1
    print("All simulations rendered without page errors")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
