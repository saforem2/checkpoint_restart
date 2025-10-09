# Check Mate

`check_mate` bundles lightweight monitors and job-recovery helpers for large-scale simulations.

## Installation

```bash
pip install check-mate
```

## Python usage

```python
import check_mate as cm

print(cm.__version__)
```

## Command-line tools

- `check-hang` — watch checkpoint files for activity and terminate a job if they stall.
- `check-nan` — inspect log files for `NaN`/`Inf` tokens and trigger recovery hooks.
- `get-healthy-nodes` — delegate to the bundled shell helper that prunes unresponsive nodes.
- `check-mate-launcher` — export launcher-friendly environment variables and execute a command.
- `check-mate-flush` — run the original flush helper used in PBS-style workflows.

Refer to the [project README](https://github.com/argonne-lcf/checkpoint_restart#readme) for detailed usage examples.

## Testing and verification

We maintain a pytest-driven regression suite that validates the optimal checkpoint calculations and
the file-monitoring utilities. After installing the project (and optional `dev` extras), run:

```bash
pytest
```

The tests exercise filesystem interactions, process termination hooks, and numerical solvers, so a
local Python environment with `numpy`, `scipy`, and `pytest` is required.
