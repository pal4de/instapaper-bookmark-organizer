#!/usr/bin/env python3
"""
Instapaper Bookmark Organizer CLI

A CLI tool to efficiently organize Instapaper bookmarks with domain-based
rule learning. Uses xAuth for one-time authentication, then stores tokens
securely for subsequent runs.

Install:
  uv sync

Run:
  uv run python main.py
  # or
  uv run instapaper-organize

Environment Variables (required):
  INSTAPAPER_CONSUMER_KEY     - Your Instapaper API consumer key
  INSTAPAPER_CONSUMER_SECRET  - Your Instapaper API consumer secret

First run only (xAuth):
  INSTAPAPER_USERNAME  - Your Instapaper email
  INSTAPAPER_PASSWORD  - Your Instapaper password

Configuration files:
  ~/.config/instapaper-cli/credentials.json  - OAuth tokens (permission 600)
  ~/.config/instapaper-cli/rules.json        - Domain-to-folder rules

API docs: https://www.instapaper.com/api
"""

from __future__ import annotations

import json
import os
import stat
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse

import requests
from requests_oauthlib import OAuth1

API_BASE = "https://www.instapaper.com/api/1"
CFG_DIR = Path(os.path.expanduser("~/.config/instapaper-cli"))
CRED_PATH = CFG_DIR / "credentials.json"
RULES_PATH = CFG_DIR / "rules.json"


@dataclass
class Folder:
    folder_id: int
    title: str


def require_env(name: str) -> str:
    v = os.getenv(name)
    if not v:
        raise SystemExit(f"Missing env: {name}")
    return v


def ensure_private_file(path: Path) -> None:
    """
    Ensure file permission is 600 (rw-------) where possible.
    """
    try:
        os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)
    except Exception:
        # On some FS/platforms chmod may fail; continue anyway.
        pass


def load_json(path: Path, default):
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data) -> None:
    CFG_DIR.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    tmp.replace(path)
    ensure_private_file(path)


def oauth_access_token_xauth(
    consumer_key: str,
    consumer_secret: str,
    username: str,
    password: str,
) -> Tuple[str, str]:
    """
    POST /api/1/oauth/access_token
    data: x_auth_username, x_auth_password, x_auth_mode=client_auth
    Returns: oauth_token, oauth_token_secret
    """
    url = f"{API_BASE}/oauth/access_token"
    auth = OAuth1(consumer_key, consumer_secret)  # request signed by consumer only

    r = requests.post(
        url,
        auth=auth,
        data={
            "x_auth_username": username,
            "x_auth_password": password,
            "x_auth_mode": "client_auth",
        },
        timeout=30,
    )
    r.raise_for_status()

    # response: oauth_token=...&oauth_token_secret=...
    parts = dict(kv.split("=", 1) for kv in r.text.strip().split("&"))
    return parts["oauth_token"], parts["oauth_token_secret"]


def api_post(auth: OAuth1, path: str, data: Optional[dict] = None) -> dict:
    url = f"{API_BASE}{path}"
    payload = data or {}

    last_err: Optional[Exception] = None
    for attempt in range(6):
        try:
            r = requests.post(url, auth=auth, data=payload, timeout=30)
            if r.status_code in (429, 500, 502, 503, 504):
                time.sleep(0.6 * (2**attempt))
                continue
            r.raise_for_status()
            return r.json() if r.text else {}
        except Exception as e:
            last_err = e
            time.sleep(0.6 * (2**attempt))
    raise SystemExit(f"API request failed: {path}: {last_err}")


def list_folders(auth: OAuth1) -> List[Folder]:
    raw = api_post(auth, "/folders/list", {})
    out: List[Folder] = []
    for x in raw:
        if x.get("type") == "folder":
            out.append(Folder(folder_id=int(x["folder_id"]), title=str(x["title"])))
    return out


def list_unread_bookmarks(auth: OAuth1, limit: int = 25) -> List[dict]:
    res = api_post(
        auth, "/bookmarks/list", {"folder_id": "unread", "limit": str(limit)}
    )
    return res.get("bookmarks", [])


def move_bookmark(auth: OAuth1, bookmark_id: int, folder_id: int) -> None:
    api_post(
        auth,
        "/bookmarks/move",
        {"bookmark_id": str(bookmark_id), "folder_id": str(folder_id)},
    )


def domain_of(url: str) -> str:
    try:
        return urlparse(url).netloc.lower()
    except Exception:
        return ""


def suggest_folder(domain: str, rules: Dict[str, int]) -> Optional[int]:
    if domain in rules:
        return rules[domain]
    # allow suffix rules: ".example.com"
    for k, v in rules.items():
        if k.startswith(".") and domain.endswith(k):
            return v
    return None


def ensure_credentials(consumer_key: str, consumer_secret: str) -> Tuple[str, str]:
    """
    Load cached (token, secret), otherwise perform xAuth once and cache.
    """
    cred = load_json(CRED_PATH, default=None)
    if cred and "oauth_token" in cred and "oauth_token_secret" in cred:
        return cred["oauth_token"], cred["oauth_token_secret"]

    username = os.getenv("INSTAPAPER_USERNAME")
    password = os.getenv("INSTAPAPER_PASSWORD")
    if not username or password is None:
        raise SystemExit(
            "No cached token. Set INSTAPAPER_USERNAME and INSTAPAPER_PASSWORD for first run."
        )

    token, secret = oauth_access_token_xauth(
        consumer_key, consumer_secret, username, password
    )
    save_json(CRED_PATH, {"oauth_token": token, "oauth_token_secret": secret})
    return token, secret


def build_keymap(folders: List[Folder], max_keys: int = 9) -> Dict[str, Folder]:
    return {str(i + 1): folders[i] for i in range(min(max_keys, len(folders)))}


def pick_folder_name(folders: List[Folder], folder_id: int) -> Optional[str]:
    for f in folders:
        if f.folder_id == folder_id:
            return f.title
    return None


def main() -> None:
    consumer_key = require_env("INSTAPAPER_CONSUMER_KEY")
    consumer_secret = require_env("INSTAPAPER_CONSUMER_SECRET")

    token, secret = ensure_credentials(consumer_key, consumer_secret)
    auth = OAuth1(consumer_key, consumer_secret, token, secret)

    folders = list_folders(auth)
    if not folders:
        raise SystemExit("No user-created folders. Create folders in Instapaper first.")

    keymap = build_keymap(folders, max_keys=9)
    rules: Dict[str, int] = load_json(RULES_PATH, default={})

    print("Folders (1..9):")
    for k, f in keymap.items():
        print(f"  {k}: {f.title} (id={f.folder_id})")
    print(
        "\nControls: [1-9]=move  [a]=auto(move by rule)  [s]=save rule for domain  [n]=skip  [q]=quit\n"
    )

    while True:
        bookmarks = list_unread_bookmarks(auth, limit=25)
        # bookmarks includes "meta" objects too; filter below
        items = [b for b in bookmarks if b.get("type") == "bookmark"]

        if not items:
            print("No unread bookmarks.")
            break

        for b in items:
            bid = int(b["bookmark_id"])
            title = (b.get("title") or "").strip() or "(no title)"
            url = (b.get("url") or "").strip()
            dom = domain_of(url)

            suggested_id = suggest_folder(dom, rules) if dom else None
            sug_name = pick_folder_name(folders, suggested_id) if suggested_id else None

            print(f"[{bid}] {title}")
            print(f"  {dom or url}")
            if sug_name:
                print(f"  suggestion: {sug_name}")

            cmd = input("> ").strip().lower()

            if cmd == "q":
                save_json(RULES_PATH, rules)
                return

            if cmd in ("n", ""):
                print()
                continue

            if cmd == "a":
                if not suggested_id:
                    print("  no suggestion\n")
                    continue
                try:
                    move_bookmark(auth, bid, suggested_id)
                    print(f"  moved -> {sug_name}\n")
                except Exception as e:
                    print(f"  move failed: {e}\n")
                continue

            if cmd == "s":
                if not dom:
                    print("  no domain; cannot save rule\n")
                    continue
                print("Pick folder key to bind this domain to:")
                for k, f in keymap.items():
                    print(f"  {k}: {f.title}")
                k = input("folder key> ").strip()
                if k not in keymap:
                    print("  invalid key\n")
                    continue
                rules[dom] = keymap[k].folder_id
                save_json(RULES_PATH, rules)
                print(f"  saved: {dom} -> {keymap[k].title}\n")
                continue

            if cmd in keymap:
                try:
                    move_bookmark(auth, bid, keymap[cmd].folder_id)
                    if dom:
                        rules.setdefault(
                            dom, keymap[cmd].folder_id
                        )  # lightweight learning
                    print(f"  moved -> {keymap[cmd].title}\n")
                except Exception as e:
                    print(f"  move failed: {e}\n")
                continue

            print("  unknown command\n")

    save_json(RULES_PATH, rules)


if __name__ == "__main__":
    main()
