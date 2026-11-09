# Service Dependency Mapper

A dependency-free Python CLI for validating a simple JSON service inventory and calculating dependency order.

## Features

- Reads a JSON service inventory.
- Validates service names and dependency references.
- Detects circular dependencies.
- Calculates topological deployment layers.
- Emits a JSON graph summary for downstream tooling.

## Input format

```json
{
  "services": [
    {"name": "database", "depends_on": []},
    {"name": "api", "depends_on": ["database"]},
    {"name": "worker", "depends_on": ["api", "database"]}
  ]
}
```

## Usage

```bash
python -m service_mapper examples/services.json
python -m service_mapper examples/services.json --json dependency-report.json
```

Services in the same layer have no dependency relationship on one another within the supplied graph. This is a planning aid, not a live service-discovery tool.

## Requirements

- Python 3.10+
- No third-party runtime dependencies

## Development

```bash
python -m unittest discover -s tests -v
```

## License

MIT. See [LICENSE](LICENSE).
