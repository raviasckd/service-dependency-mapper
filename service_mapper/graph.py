"""Validate a service inventory and derive dependency deployment layers."""

from __future__ import annotations

from typing import Any


def build_plan(document: dict[str, Any]) -> dict[str, Any]:
    """Return a stable topological plan or raise ValueError for invalid graphs.

    Each layer contains services whose dependencies are satisfied by earlier
    layers. A cycle or unknown dependency is reported rather than guessed.
    """
    records = document.get("services")
    if not isinstance(records, list):
        raise ValueError("'services' must be a list")

    dependencies: dict[str, set[str]] = {}
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("each service must be an object")
        name = record.get("name")
        deps = record.get("depends_on", [])
        if not isinstance(name, str) or not name.strip():
            raise ValueError("service names must be non-empty strings")
        name = name.strip()
        if name in dependencies:
            raise ValueError(f"duplicate service name: {name}")
        if not isinstance(deps, list) or not all(
            isinstance(item, str) and item.strip() for item in deps
        ):
            raise ValueError(f"depends_on for {name!r} must be a list of non-empty names")
        dependencies[name] = {item.strip() for item in deps}

    for name, deps in dependencies.items():
        unknown = deps - dependencies.keys()
        if unknown:
            raise ValueError(
                f"unknown dependencies for {name!r}: {', '.join(sorted(unknown))}"
            )

    remaining = {name: set(deps) for name, deps in dependencies.items()}
    layers: list[list[str]] = []
    while remaining:
        ready = sorted(name for name, deps in remaining.items() if not deps)
        if not ready:
            raise ValueError(
                f"cycle detected among services: {', '.join(sorted(remaining))}"
            )
        layers.append(ready)
        for name in ready:
            remaining.pop(name)
        for deps in remaining.values():
            deps.difference_update(ready)

    return {
        "services": sorted(dependencies),
        "layers": layers,
        "dependency_count": sum(len(items) for items in dependencies.values()),
    }
