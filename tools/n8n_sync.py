"""Synchronizacja workflow n8n z plikami JSON w repo przez Public API.

Klucz API: zmienna N8N_API_KEY lub N8N_LOCAL_API_KEY_TMD (nigdy w repo ani w logach).
Przyklady:
  python tools/n8n_sync.py list
  python tools/n8n_sync.py pull Ku19rXEPiP6PkDWu n8n/repo-qa-raport-workflow.json
  python tools/n8n_sync.py push Ku19rXEPiP6PkDWu n8n/repo-qa-raport-workflow.json
  python tools/n8n_sync.py create n8n/<plik>.json   (nowy workflow z pliku)
  python tools/n8n_sync.py restore [n8n]            (odtworz brakujace workflow z katalogu)
  python tools/n8n_sync.py check [n8n]              (porownaj n8n z plikami; kod 1 = rozbieznosc)
Folder w n8n (TheoreticalMD) ustawia sie w UI - Public API go nie obsluguje.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

BASE_URL = os.environ.get("N8N_BASE_URL", "http://localhost:5678").rstrip("/")
KEY_VARS = ("N8N_API_KEY", "N8N_LOCAL_API_KEY_TMD")
EXPORT_FIELDS = ("name", "nodes", "connections", "settings")
SECRET_RE = re.compile(r"bearer\s+[A-Za-z0-9._-]{16,}|x-n8n-api-key", re.IGNORECASE)
ID_RE = re.compile(r"^[A-Za-z0-9]+$")


def get_api_key() -> str:
    for name in KEY_VARS:
        value = os.environ.get(name)
        if value:
            return value
    if sys.platform == "win32":
        import winreg

        for name in KEY_VARS:
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as reg:
                    value = winreg.QueryValueEx(reg, name)[0]
            except OSError:
                continue
            if value:
                return value
    raise SystemExit("Blocker: brak klucza API (ustaw N8N_API_KEY lub N8N_LOCAL_API_KEY_TMD).")


def request(method: str, path: str, payload: dict | None = None) -> dict:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(
        BASE_URL + "/api/v1" + path,
        data=data,
        method=method,
        headers={"X-N8N-API-KEY": get_api_key(), "Content-Type": "application/json; charset=utf-8"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"Blocker: HTTP {exc.code} dla {method} {path}") from None
    except urllib.error.URLError as exc:
        raise SystemExit(f"Blocker: brak polaczenia z n8n ({exc.reason})") from None


def check_id(workflow_id: str) -> str:
    if not ID_RE.match(workflow_id):
        raise SystemExit("Blocker: niepoprawny identyfikator workflow.")
    return workflow_id


def to_export(workflow: dict) -> dict:
    return {key: workflow[key] for key in EXPORT_FIELDS if key in workflow}


def to_update_body(exported: dict) -> dict:
    body = {key: exported[key] for key in ("name", "nodes", "connections") if key in exported}
    body["settings"] = {"executionOrder": exported.get("settings", {}).get("executionOrder", "v1")}
    return body


def has_secret(text: str) -> bool:
    return bool(SECRET_RE.search(text))


def safe_print(line: str) -> None:
    enc = sys.stdout.encoding or "utf-8"
    print(line.encode(enc, "replace").decode(enc))


def cmd_list(_: argparse.Namespace) -> int:
    for item in request("GET", "/workflows?limit=250").get("data", []):
        line = f"{item['id']} | {item['name']} | active={item.get('active')}"
        print(line.encode(sys.stdout.encoding or "utf-8", "replace").decode(sys.stdout.encoding or "utf-8"))
    return 0


def cmd_pull(args: argparse.Namespace) -> int:
    exported = to_export(request("GET", f"/workflows/{check_id(args.workflow_id)}"))
    text = json.dumps(exported, ensure_ascii=False, indent=2) + "\n"
    if has_secret(text):
        raise SystemExit("Blocker: eksport zawiera wzorzec sekretu - przerwano zapis.")
    Path(args.file).write_text(text, encoding="utf-8", newline="\n")
    print(f"OK: zapisano {args.file}")
    return 0


def cmd_push(args: argparse.Namespace) -> int:
    text = Path(args.file).read_text(encoding="utf-8")
    if has_secret(text):
        raise SystemExit("Blocker: plik zawiera wzorzec sekretu - przerwano.")
    result = request("PUT", f"/workflows/{check_id(args.workflow_id)}", to_update_body(json.loads(text)))
    print(f"OK: zaktualizowano '{result.get('name')}' ({len(result.get('nodes', []))} wezlow)")
    return 0


def create_from_file(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if has_secret(text):
        raise SystemExit(f"Blocker: {path} zawiera wzorzec sekretu - przerwano.")
    result = request("POST", "/workflows", to_update_body(json.loads(text)))
    return f"{result.get('id')} | {result.get('name')}"


def cmd_create(args: argparse.Namespace) -> int:
    print(f"OK: utworzono {create_from_file(Path(args.file))}")
    return 0


def cmd_restore(args: argparse.Namespace) -> int:
    existing = {item["name"] for item in request("GET", "/workflows?limit=250").get("data", [])}
    for path in sorted(Path(args.directory).glob("*.json")):
        name = json.loads(path.read_text(encoding="utf-8")).get("name")
        if name in existing:
            print(f"POMINIETO (juz istnieje): {name}")
        else:
            print(f"OK: utworzono {create_from_file(path)}")
    print("Uwaga: przenies workflow do folderu TheoreticalMD w UI i utworz credential Header Auth.")
    return 0


COMPARE_FIELDS = ("nodes", "connections")


def compare_workflows(local: dict, remote: dict) -> list[str]:
    return [field for field in COMPARE_FIELDS if local.get(field) != remote.get(field)]


def cmd_check(args: argparse.Namespace) -> int:
    """Porownuje workflow w n8n z plikami w repo (tylko odczyt). Kod 1 = rozbieznosc."""
    remote = {}
    for item in request("GET", "/workflows?limit=250").get("data", []):
        remote[item["name"]] = item["id"]
    problems = 0
    seen = set()
    for path in sorted(Path(args.directory).glob("*.json")):
        local = json.loads(path.read_text(encoding="utf-8"))
        name = local.get("name")
        seen.add(name)
        if name not in remote:
            safe_print(f"BLOCKER brak w n8n: {name} ({path.name})")
            problems += 1
            continue
        diff = compare_workflows(local, request("GET", f"/workflows/{check_id(remote[name])}"))
        if diff:
            safe_print(f"BLOCKER rozbiezne ({', '.join(diff)}): {name} [{remote[name]}] <-> {path.name}")
            problems += 1
        else:
            safe_print(f"OK zgodne: {name} [{remote[name]}]")
    for name in sorted(set(remote) - seen):
        safe_print(f"WARNING brak pliku w repo: {name} [{remote[name]}]")
    safe_print(f"Podsumowanie: rozbieznosci={problems}")
    return 1 if problems else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list").set_defaults(func=cmd_list)
    create = sub.add_parser("create")
    create.add_argument("file")
    create.set_defaults(func=cmd_create)
    restore = sub.add_parser("restore")
    restore.add_argument("directory", nargs="?", default="n8n")
    restore.set_defaults(func=cmd_restore)
    check = sub.add_parser("check")
    check.add_argument("directory", nargs="?", default="n8n")
    check.set_defaults(func=cmd_check)
    for name, func in (("pull", cmd_pull), ("push", cmd_push)):
        p = sub.add_parser(name)
        p.add_argument("workflow_id")
        p.add_argument("file")
        p.set_defaults(func=func)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
