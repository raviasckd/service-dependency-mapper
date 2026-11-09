"""CLI for service dependency map validation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from service_mapper.graph import build_plan


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate and order service dependencies.")
    parser.add_argument("input", type=Path, help="JSON service inventory")
    parser.add_argument("--json", dest="json_path", type=Path, help="Write plan to a JSON file")
    args = parser.parse_args(argv)
    try:
        document = json.loads(args.input.read_text(encoding="utf-8"))
        plan = build_plan(document)
        rendered = json.dumps(plan, indent=2)
        print(rendered)
        if args.json_path:
            args.json_path.write_text(rendered + "\n", encoding="utf-8")
        return 0
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        print(f"service-mapper: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
