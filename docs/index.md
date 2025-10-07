# Exacheckmate

`exacheckmate` bundles lightweight monitors and job-recovery helpers for large-scale simulations.

## Installation

```bash
pip install exacheckmate
```

## Command-line tools

- `check-hang` — watch checkpoint files for activity and terminate a job if they stall.
- `check-nan` — inspect log files for `NaN`/`Inf` tokens and trigger recovery hooks.
- `get-healthy-nodes` — delegate to the bundled shell helper that prunes unresponsive nodes.
- `exacheckmate-launcher` — export launcher-friendly environment variables and execute a command.
- `exacheckmate-flush` — run the original flush helper used in PBS-style workflows.

Refer to the [project README](https://github.com/argonne-lcf/checkpoint_restart#readme) for detailed usage examples.
