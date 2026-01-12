#!/usr/bin/env python3
"""Rebuild Brewfile.lock.json from the current system state.

[macOS-only] Uses sw_vers and Homebrew tooling available on macOS.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path


RE_TAP = re.compile(r'^tap\s+"([^"]+)"')
RE_BREW = re.compile(r'^brew\s+"([^"]+)"')
RE_CASK = re.compile(r'^cask\s+"([^"]+)"')
RE_MAS = re.compile(r'^mas\s+"([^"]+)"\s*,\s*id:\s*(\d+)')
RE_VSCODE = re.compile(r'^vscode\s+"([^"]+)"')


class CommandError(RuntimeError):
    pass


def run(cmd: list[str]) -> str:
    try:
        return subprocess.check_output(cmd, text=True)
    except subprocess.CalledProcessError as exc:
        raise CommandError(f"Command failed: {' '.join(cmd)}") from exc


def parse_brewfile(path: Path) -> dict[str, list]:
    taps: list[str] = []
    brews: list[str] = []
    casks: list[str] = []
    mas_entries: list[tuple[str, str]] = []
    vscode: list[str] = []

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        m = RE_TAP.match(line)
        if m:
            taps.append(m.group(1))
            continue
        m = RE_BREW.match(line)
        if m:
            brews.append(m.group(1))
            continue
        m = RE_CASK.match(line)
        if m:
            casks.append(m.group(1))
            continue
        m = RE_MAS.match(line)
        if m:
            mas_entries.append((m.group(1), m.group(2)))
            continue
        m = RE_VSCODE.match(line)
        if m:
            vscode.append(m.group(1))
            continue

    return {
        "tap": taps,
        "brew": brews,
        "cask": casks,
        "mas": mas_entries,
        "vscode": vscode,
    }


def system_info() -> dict:
    product = run(["sw_vers", "-productVersion"]).strip()
    build = run(["sw_vers", "-buildVersion"]).strip()
    arch = run(["uname", "-m"]).strip()
    return {
        "macos": {"product": product, "build": build},
        "architecture": arch,
    }


def tap_revisions(taps: list[str]) -> dict[str, str]:
    revisions: dict[str, str] = {}
    for tap in taps:
        info = json.loads(run(["brew", "tap-info", "--json", tap]))
        head = info[0].get("HEAD") or info[0].get("head")
        if not head:
            raise CommandError(f"No HEAD revision found for tap: {tap}")
        revisions[tap] = head
    return revisions


def installed_formula_map() -> dict[str, tuple[str, str]]:
    info = json.loads(run(["brew", "info", "--json=v2", "--installed"]))
    formula_map: dict[str, tuple[str, str]] = {}
    for formula in info.get("formulae", []):
        installed = formula.get("installed") or []
        if installed:
            installed_sorted = sorted(installed, key=lambda x: x.get("time", 0))
            version = installed_sorted[-1].get("version")
        else:
            version = None
        tap = formula.get("tap")
        name = formula.get("name")
        full_name = formula.get("full_name")
        aliases = formula.get("aliases") or []

        if version is None:
            continue

        for key in filter(None, [name, full_name, *aliases]):
            formula_map[key] = (version, tap)
    return formula_map


def installed_cask_map() -> dict[str, tuple[str, str]]:
    info = json.loads(run(["brew", "info", "--json=v2", "--cask", "--installed"]))
    cask_map: dict[str, tuple[str, str]] = {}
    for cask in info.get("casks", []):
        installed = cask.get("installed")
        if isinstance(installed, list):
            version = installed[-1] if installed else cask.get("version")
        elif isinstance(installed, str) and installed:
            version = installed
        else:
            version = cask.get("version")
        token = cask.get("token")
        tap = cask.get("tap")
        if token and version:
            cask_map[token] = (version, tap)
    return cask_map


def mas_versions() -> dict[str, tuple[str, str]]:
    output = run(["mas", "list"])
    versions: dict[str, tuple[str, str]] = {}
    for line in output.splitlines():
        line = line.strip()
        if not line:
            continue
        m = re.match(r"^(\d+)\s+(.+?)\s+\(([^)]+)\)$", line)
        if not m:
            continue
        app_id, name, version = m.group(1), m.group(2), m.group(3)
        versions[app_id] = (name, version)
    return versions


def vscode_versions() -> dict[str, str]:
    candidates = ["code", "cursor", "codium", "code-insiders"]
    for cmd in candidates:
        try:
            output = run([cmd, "--list-extensions", "--show-versions"])
            versions: dict[str, str] = {}
            for line in output.splitlines():
                line = line.strip()
                if not line or "@" not in line:
                    continue
                ext, version = line.split("@", 1)
                versions[ext] = version
            return versions
        except CommandError:
            continue
    raise CommandError("No VS Code CLI found (code/cursor/codium/code-insiders)")


def build_lockfile(brewfile_path: Path) -> dict:
    parsed = parse_brewfile(brewfile_path)
    entries: OrderedDict[str, OrderedDict] = OrderedDict()

    entries["tap"] = OrderedDict()
    tap_map = tap_revisions(parsed["tap"])
    for tap in parsed["tap"]:
        entries["tap"][tap] = {"revision": tap_map[tap]}

    formula_map = installed_formula_map()
    entries["brew"] = OrderedDict()
    for name in parsed["brew"]:
        item = formula_map.get(name)
        if not item:
            raise CommandError(f"Missing formula info for: {name}")
        version, tap = item
        entries["brew"][name] = {"version": version, "tap": tap}

    cask_map = installed_cask_map()
    entries["cask"] = OrderedDict()
    for name in parsed["cask"]:
        item = cask_map.get(name)
        if not item:
            raise CommandError(f"Missing cask info for: {name}")
        version, tap = item
        entries["cask"][name] = {"version": version, "tap": tap}

    entries["mas"] = OrderedDict()
    if parsed["mas"]:
        mas_map = mas_versions()
        for name, app_id in parsed["mas"]:
            item = mas_map.get(str(app_id))
            if not item:
                raise CommandError(f"Missing MAS info for: {name} ({app_id})")
            _, version = item
            entries["mas"][name] = {"id": str(app_id), "version": version}

    entries["vscode"] = OrderedDict()
    if parsed["vscode"]:
        vscode_map = vscode_versions()
        for ext in parsed["vscode"]:
            version = vscode_map.get(ext)
            if not version:
                raise CommandError(f"Missing VS Code extension info for: {ext}")
            entries["vscode"][ext] = {"version": version}

    payload: OrderedDict[str, object] = OrderedDict()
    payload["generated_at"] = datetime.now(timezone.utc).isoformat()
    payload["system"] = system_info()
    payload["entries"] = entries

    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Update Brewfile.lock.json")
    parser.add_argument("--brewfile", default="Brewfile", help="Path to Brewfile")
    parser.add_argument(
        "--lockfile",
        default="Brewfile.lock.json",
        help="Path to Brewfile.lock.json",
    )
    args = parser.parse_args()

    brewfile_path = Path(args.brewfile)
    lockfile_path = Path(args.lockfile)

    if not brewfile_path.exists():
        print(f"Brewfile not found: {brewfile_path}", file=sys.stderr)
        return 1

    try:
        payload = build_lockfile(brewfile_path)
    except CommandError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    lockfile_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
