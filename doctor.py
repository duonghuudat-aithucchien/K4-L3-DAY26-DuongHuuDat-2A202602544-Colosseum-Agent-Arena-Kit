"""doctor.py — Windows-friendly runner for `make doctor`."""
from __future__ import annotations

import glob
import json
import subprocess
import sys
from pathlib import Path

def main():
    # 1. check-no-key
    r = subprocess.run([sys.executable, "-m", "kit.gate_no_key"])
    if r.returncode != 0:
        sys.exit(1)

    # 2. check-world
    manifests = sorted(glob.glob("kit/world/*/manifest.json"))
    if not manifests:
        print("FAIL: no world in kit/world/ - ask your instructor for the world artifact")
        sys.exit(1)
    
    latest_manifest = manifests[-1]
    with open(latest_manifest, "r", encoding="utf-8") as f:
        m = json.load(f)
    print(f"world {m.get('world_id')} - {sum(m.get('counts', {}).values())} pages")
    
    if glob.glob("kit/world/*/truth.json"):
        print("FAIL: truth.json must never ship to students")
        sys.exit(1)

    # 3. check-referee
    from kit.referee.rubric import CLASSES
    from kit.referee.adjudicate import LOCAL_ONLY
    print(f"referee: {len(CLASSES)} classes, local_only={LOCAL_ONLY}")

    # 4. validate deck
    world_dir = Path(latest_manifest).parent
    r2 = subprocess.run([
        sys.executable, "validate_deck.py",
        "deck/deck.json", "deck/lineup.json",
        "--world", str(world_dir)
    ])
    if r2.returncode != 0:
        sys.exit(1)

    print("\nready to spar.")

if __name__ == "__main__":
    main()
