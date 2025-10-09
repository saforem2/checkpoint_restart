# ✅ Check Mate

> Checkpoint/Restart helpers for exascale computing

Check Mate packages the monitoring utilities that the ALCF uses to keep
large-scale simulations alive: lightweight log inspectors, hang detectors,
and wrappers around the original shell tooling for rebuilding a healthy node
allocation. Install the Python package and you immediately gain access to
both the Python APIs and the bundled command line entry points.

## Features

- 🔍 **Runtime monitors** – `check-hang` watches checkpoint files for stalled
  updates while `check-nan` searches log files for `NaN`/`Inf` tokens.
- 🧠 **Checkpoint modelling** – the `check_mate.optimal_checkpointing`
  module computes optimal checkpoint cadences and expected efficiency.
- 🧰 **Bundled shell helpers** – `check-mate` proxies the original
  node-health, launcher, and cache-flush scripts via `importlib.resources`.
- 📚 **Full documentation** – the MkDocs site includes step-by-step guides and
  working examples for each utility.

## Installation

```bash
pip install check-mate
```

Optional extras:

```bash
# Documentation build dependencies
pip install check-mate[docs]

# Development linting hooks (ruff + pre-commit)
pip install check-mate[dev]
```

## Quick start

Verify your installation and inspect the shipped version:

```bash
$ check-mate --version
check-mate 0.1.0
```

Import the package from Python and evaluate a checkpoint cadence for a
1,024-node workload that writes 250 GB per node to the DAOS-128 storage tier:

```python
>>> import check_mate as cm
>>> from check_mate import optimal_checkpointing as oc
>>> cadence = oc.optimal_checkpoint_cadence(
...     node_count=1024,
...     node_memory=2.5e11,
...     chkpt_bandwidth="DAOS-128",
... )
>>> efficiency = oc.compute_efficiency(
...     node_count=1024,
...     node_memory=2.5e11,
...     chkpt_bandwidth="DAOS-128",
... )
>>> cm.__version__
'0.1.0'
>>> f"{cadence:.3f} h"
'6.951 h'
>>> f"{efficiency:.3%}"
'36.531%'
```

## Command line tools

The top-level dispatcher summarises every bundled helper:

```bash
$ check-mate --help
usage: check-mate [-h] [--version] {get-healthy-nodes,launcher,flush} ...

Utility command dispatcher for check-mate tools.

positional arguments:
  {get-healthy-nodes,launcher,flush}
                        Which bundled tool to execute.
  args

options:
  -h, --help            show this help message and exit
  --version             show program's version number and exit

Available commands:
  get-healthy-nodes  Select responsive nodes from a nodefile.
    Selects a subset of responsive nodes from a nodefile by delegating to the bundled shell implementation.
  launcher           Launch the check-mate job runner.
  flush              Flush all check-mate caches.
```

### Working examples

#### Select a healthy node subset

Create a tiny nodefile and ask `get-healthy-nodes` to retain a single
responsive entry. The helper pings each node and writes the first *N*
responsive hosts into the destination file:

```bash
$ printf '127.0.0.1\n127.0.0.1\n' > nodes.txt
$ check-mate get-healthy-nodes nodes.txt 1 selected.txt
Build a selected.txt nodes nodefile from nodes.txt, which contains 1 nodes
Total number of nodes checked: 1
Number of nodes that are selected: 1
$ cat selected.txt
127.0.0.1
```

#### Bootstrap launcher metadata

Mimic a PMI/PALS environment by providing the nodefile and rank metadata
before delegating to the original launcher script:

```bash
$ export PBS_NODEFILE=$(pwd)/nodes.txt
$ export PALS_LOCAL_SIZE=2
$ export PALS_LOCAL_RANKID=1
$ export PALS_RANKID=5
$ check-mate launcher -- echo "Hello from launcher"
I am 5 of 4: 1 on 22a1e6e6a625
Hello from launcher
```

#### Detect stalled checkpoints

Run the hang detector in dry-run mode against a non-existent checkpoint file
so the inactivity timer fires quickly:

```bash
$ check-hang --timeout 3 --check 1 --outputs temp.chkpt --dry-run
[2025-10-09 15:46:04] Job monitor started
Watching: temp.chkpt
Timeout: 3s | Check interval: 1s

[2025-10-09 15:46:05] Checking job status
None of the watched files exist yet; monitoring...
Job has been running for 1.0 seconds
No updates for 1.0 seconds
[2025-10-09 15:46:07] Output has not been updated for 3.0 seconds. Issuing kill command...
(dry-run) Skipping kill execution
[2025-10-09 15:46:07] Monitor exiting after inactivity timeout.
```

#### Catch NaNs in logs

Point `check-nan` at an artificial log that contains a `nan` token. The
`--dry-run` flag avoids killing anything while still demonstrating the
recovery hook:

```bash
$ cat <<'LOG' > demo.log
step=1 loss=1.23
step=2 loss=nan
LOG
$ check-nan --outputs demo.log --check 1 --timeout 0 --dry-run
[2025-10-09 15:45:18] Monitoring for NaN in: demo.log
[2025-10-09 15:45:18] Detected NaN in demo.log.
[DRY-RUN] Would terminate job (skipping actual kill).
```

### Additional scripts

- `check-mate flush` forwards directly to the original flush helper. Set the
  `PBS_NODEFILE` environment variable so the script knows which nodes to
  operate on.
- The legacy standalone executables (`check-hang`, `check-nan`) remain
  available for backwards compatibility; they share the same code as the
  examples above.

## Simulation harness

The `test_pyjob.py` helper can simulate failure, hanging, and successful runs.
Use it to validate your recovery strategy locally:

```bash
python test_pyjob.py --fail 120 --checkpoint ./chkpt --niters 1000
```

The `examples/` directory contains archived run logs for failed, hanging,
successful, and NaN-producing workloads.

## Documentation

Comprehensive usage notes—including full CLI reference material, Python API
explanations, and job orchestration walkthroughs—live under `docs/` and can be
served locally with MkDocs:

```bash
pip install check-mate[docs]
mkdocs serve
```

Visit the hosted documentation for the latest guides and recipes.

## License

This project is distributed under the terms of the MIT License. See
[LICENSE](LICENSE) for details.

## Contact

For questions please contact Huihuo Zheng <huihuo.zheng@anl.gov>.

