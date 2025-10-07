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
