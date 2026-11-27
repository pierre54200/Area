"""Minimal executable contract smoke test; not a replacement for Schemathesis."""
import json, pathlib, re
HERE = pathlib.Path(__file__).parent
spec = (HERE / "../../shared/openapi.yaml").resolve().read_text()
implemented = json.loads((HERE / "implementation.json").read_text())
# Parse the intentionally small YAML path/method subset used by this POC.
paths = {}
current = None
for line in spec.splitlines():
    m = re.match(r"^  (\S+):$", line)
    if m:
        current = m.group(1); paths[current] = []
    m = re.match(r"^    (get|post|patch|put|delete):$", line)
    if m and current: paths[current].append(m.group(1).upper())
declared = {f"{method} {path}" for path, methods in paths.items() for method in methods}
assert declared == set(implemented), f"Contract mismatch: missing={declared-set(implemented)}, extra={set(implemented)-declared}"
print(f"OK: {len(declared)} route/method pairs match the OpenAPI contract")
