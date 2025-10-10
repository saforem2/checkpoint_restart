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

- `check-mate-hang` — watch checkpoint files for activity and terminate a job if they stall.
- `check-mate-nan` — inspect log files for `NaN`/`Inf` tokens and trigger recovery hooks.
- `get-healthy-nodes` — delegate to the bundled shell helper that prunes unresponsive nodes.
- `check-mate-launcher` — export launcher-friendly environment variables and execute a command.
- `check-mate-flush` — run the original flush helper used in PBS-style workflows.

Refer to the [project README](https://github.com/argonne-lcf/checkpoint_restart#readme) for detailed usage examples.

## Building and packaging

`check-mate` is published using the [`uv` build backend](https://docs.astral.sh/uv/). After installing
`uv` and `uv-build`, run `uv build --wheel --sdist` from the repository root to produce local
artifacts. The resulting `dist/` directory mirrors what `uv publish` will upload to package indexes.

## Packaged submission templates

Sample PBS scripts are distributed with the library and can be previewed or saved locally via

```bash
python -m check_mate.examples.fail            # print the failing job template
python -m check_mate.examples.hang --output hang.sc
```

## Testing and verification

Refer to the [project README](https://github.com/argonne-lcf/checkpoint_restart#running-the-test-suite)
for end-to-end setup instructions. The README covers creating an isolated environment, installing
the optional `dev` extras (which pull in `pytest`), and running the regression suite locally.
