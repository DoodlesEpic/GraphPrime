#!/usr/bin/env python3
"""Exercise a real Linux package with WebKitWebDriver (no mocked Tauri IPC).

Usage: python3 tests/smoke-linux.py path/to/GraphPrime.AppImage
On CI: dbus-run-session -- xvfb-run -a python3 tests/smoke-linux.py ...
Requires WebKitWebDriver and PyGObject/GTK 3 for the clipboard assertion.
"""

import base64
import json
import os
from pathlib import Path
import signal
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request


ELEMENT = "element-6066-11e4-a52e-4f735466cecf"
output = Path(os.environ.get("TEST_RESULTS_DIR", "test-results"))
output.mkdir(parents=True, exist_ok=True)
binary = Path(sys.argv[1]).resolve(strict=True)
binary.chmod(binary.stat().st_mode | 0o111)
with socket.socket() as sock:
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
base = f"http://127.0.0.1:{port}"
session = None


def request(method, path, data=None):
    payload = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(
        base + path, data=payload, method=method,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            return json.load(response)["value"]
    except urllib.error.HTTPError as error:
        raise RuntimeError(error.read().decode()) from error


def command(method, path, data=None):
    return request(method, f"/session/{session}{path}", data)


def js(script, *args):
    return command("POST", "/execute/sync", {"script": script, "args": list(args)})


def wait_for(check, description, timeout=30):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if check():
            return
        time.sleep(0.2)
    raise AssertionError(f"Timed out: {description}")


def element(selector):
    return command("POST", "/element", {"using": "css selector", "value": selector})[ELEMENT]


def click(selector):
    command("POST", f"/element/{element(selector)}/click", {})


def screenshot(name):
    (output / f"{name}.png").write_bytes(base64.b64decode(command("GET", "/screenshot")))


def expected_primes(limit):
    # An independent, small reference implementation checks the Rust results.
    return [n for n in range(2, limit + 1)
            if all(n % d for d in range(2, int(n ** 0.5) + 1))]


def calculate(limit):
    entry = element('input[aria-label="Calculate primes up to"]')
    command("POST", f"/element/{entry}/clear", {})
    command("POST", f"/element/{entry}/value", {"text": str(limit)})
    click("button.button")
    primes = expected_primes(limit)
    stats = f"{len(primes)} prime numbers calculated up to {limit}"
    wait_for(lambda: stats in js("return document.body.innerText"), stats)
    wait_for(lambda: js("return !document.querySelector('button.button').disabled"),
             "calculation completes")
    assert js("return document.querySelector('.cm-content').textContent") == ", ".join(map(str, primes))
    assert f"There are {limit - len(primes) - 1} composite numbers up to {limit}" in js(
        "return document.body.innerText")
    print(f"PASS: primes and statistics up to {limit}", flush=True)
    return primes


env = {**os.environ, "TAURI_WEBVIEW_AUTOMATION": "true", "APPIMAGE_EXTRACT_AND_RUN": "1"}
with (output / "webdriver.log").open("w") as log:
    driver = subprocess.Popen(
        ["WebKitWebDriver", f"--port={port}"], env=env,
        stdout=log, stderr=subprocess.STDOUT, start_new_session=True,
    )
    try:
        def ready():
            if driver.poll() is not None:
                raise RuntimeError("WebKitWebDriver exited before startup")
            try:
                return request("GET", "/status")["ready"]
            except urllib.error.URLError:
                return False

        wait_for(ready, "WebKitWebDriver starts")
        session = request("POST", "/session", {"capabilities": {"alwaysMatch": {
            "webkitgtk:browserOptions": {"binary": str(binary)}
        }}})["sessionId"]
        wait_for(lambda: js("return !!document.querySelector('.cm-content')"), "app loads")
        js("""
          window.smokeErrors = [];
          window.addEventListener('error', e => window.smokeErrors.push(e.message));
          window.addEventListener('unhandledrejection', e => window.smokeErrors.push(String(e.reason)));
          window.addEventListener('securitypolicyviolation', e => window.smokeErrors.push(e.violatedDirective));
        """)
        assert js("return getComputedStyle(document.querySelector('.title')).color") == "rgb(255, 62, 0)"
        assert js("return getComputedStyle(document.querySelector('.input-group')).display") == "flex"
        assert js("return document.querySelectorAll('link[rel=stylesheet]').length") >= 2
        assert js("return getComputedStyle(document.querySelector('.cm-editor')).position") == "relative"
        assert js("return document.querySelector('button.button').disabled")
        wait_for(lambda: js("return !!document.querySelector('.frappe-chart svg')"), "basic graph renders")
        screenshot("initial")
        print("PASS: bundled CSS, dynamic editor styles, initial SVG graph", flush=True)

        for limit in [1, 2, 30, 1000, 10000, 100000, 100]:
            calculate(limit)
            graph = ".chart canvas" if limit >= 10000 else ".frappe-chart svg"
            wait_for(lambda: js("return !!document.querySelector(arguments[0])", graph), "graph renders")
            if limit == 100000:
                js("document.querySelector('.chart').scrollIntoView()")
                screenshot("scientific")

        click('[aria-label="Copy primes"]')
        import gi
        gi.require_version("Gtk", "3.0")
        gi.require_version("Gdk", "3.0")
        from gi.repository import Gdk, Gtk
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        copied = ", ".join(map(str, expected_primes(100)))
        wait_for(lambda: clipboard.wait_for_text() == copied, "native clipboard contains primes")
        print("PASS: native clipboard", flush=True)

        for label in ["Toggle primes fullscreen", "Toggle graph fullscreen"]:
            click(f'[aria-label="{label}"]')
            wait_for(lambda: js("return document.querySelectorAll('.fullscreen').length === 1"), label)
            screenshot(label.lower().replace(" ", "-"))
            click(f'[aria-label="{label}"]')
            wait_for(lambda: js("return !document.querySelector('.fullscreen')"), "exit fullscreen")

        for chart_type in ["dygraph", "frappe", "dygraph", "frappe"]:
            js("""
              const select = document.querySelector('select');
              select.value = arguments[0];
              select.dispatchEvent(new Event('change', {bubbles: true}));
            """, chart_type)
            selector = ".chart canvas" if chart_type == "dygraph" else ".frappe-chart svg"
            wait_for(lambda: js("return !!document.querySelector(arguments[0])", selector), "chart switch")
        print("PASS: fullscreen and repeated chart switching", flush=True)

        js("window.scrollTo(0, 0)")
        screenshot("final")
        errors = js("return window.smokeErrors")
        assert not errors, errors
        print("PASS: no JavaScript errors or CSP violations", flush=True)
    except Exception:
        if session:
            screenshot("failure")
            (output / "failure.html").write_text(command("GET", "/source"))
        raise
    finally:
        try:
            if session:
                request("DELETE", f"/session/{session}")
        finally:
            os.killpg(driver.pid, signal.SIGTERM)
            driver.wait(timeout=10)

log_text = (output / "webdriver.log").read_text()
assert "EGL_BAD_PARAMETER" not in log_text, log_text
print(f"PASS: Linux package smoke test. Evidence: {output.resolve()}")
