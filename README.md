# Check Mate – Checkpoint/Restart helpers for exascale computing

For questions, please contact: Huihuo Zheng <huihuo.zheng@anl.gov>

Exascale computing systems often experience instabilities that can cause job terminations before completion.

To ensure large-scale simulations can continue efficiently, checkpoint/restart mechanisms are essential.

This repository provides:

- Simple programs to simulate common job execution issues:
  (1) hanging, (2) mid-run failures, and (3) successful completion.
- Example submission scripts that automatically detect failures and restart jobs using healthy nodes.

The **key idea** is to over-allocate nodes, allowing jobs to be restarted on a healthy subset of nodes if a failure occurs.

![alt text](.docs/figures/schematic.png)

## Install the package

```bash
git clone https://github.com/argonne-lcf/checkpoint_restart
cd checkpoint_restart
pip install -e .
```
This will install the `check-hang`, `check-nan`, `get-healthy-nodes`, `check-mate-launcher`, and `check-mate-flush` command line tools into your environment.

## Python usage

```python
import check_mate as cm

print(cm.__version__)
```

## Useful Scripts

This repository includes several scripts to help manage and monitor jobs. After installation, `check-hang`, `check-nan`, and `get-healthy-nodes` will be available in your PATH.

- `check-hang`: Monitors files for updates and kills a job if it stops changing for longer than a specified timeout. This is useful for detecting hung processes.
  ```bash
  check-hang --timeout 600 --check 10 --command "mpiexec python train.py"
  ```
  **Arguments:**
  - `--timeout`: Seconds of inactivity after which the job will be killed (default: 300).
  - `--check`: Seconds between file-activity checks (default: 5).
  - `--kill-command`: Shell command to terminate the job (default: `pkill -u $USER mpiexec`).
  - `--outputs`: Colon-separated list of output files to watch (default: `chkpt/latest`).
  - `--grace`: Seconds to wait after sending the kill command before exiting (default: 10).
  - `--dry-run`: If set, do not actually run the kill command—only log the action.

- `check-nan`: Monitors text output files for `NaN` or `Inf` values and terminates the job if they are found. This is useful for catching numerical stability issues.
  ```bash
  check-nan --outputs "logs/*.out" --check 15 --kill-command "scancel $SLURM_JOB_ID"
  ```
  **Arguments:**
  - `--outputs`: Glob pattern for files to watch.
  - `--recursive`: Enable recursive globbing.
  - `--check`: Polling interval in seconds (default: 15).
  - `--timeout`: Exit with code 0 if no NaN/Inf found after this many seconds (0 disables timeout).
  - `--include-inf`: Also treat 'inf' tokens as fatal.
  - `--pid`: If set, send a signal to this PID on detection.
  - `--signal`: Signal to send when using `--pid` (default: `TERM`).
  - `--grace`: Seconds to wait before escalating to `SIGKILL` if `--pid` is used (default: 15).
  - `--kill-command`: Arbitrary shell command to run on detection.
  - `--dry-run`: Detect and report but do not kill or run commands.
  - `--verbose`: Print verbose progress messages.

- `get-healthy-nodes`: Selects a subset of healthy nodes from a larger allocation, writing them to a new nodefile. This is key to the restart mechanism.
  ```bash
  get-healthy-nodes NODEFILE NUM_NODES_TO_SELECT NEW_NODEFILE
  ```

- `check-mate-launcher`: Export launch-friendly environment variables derived from common PBS/PMI metadata before executing a command.
  ```bash
  check-mate-launcher python test_pyjob.py --hang 30
  ```
- `check-mate-flush`: Invoke the bundled flush helper to clean up processes on allocated nodes (requires `clush`).
  ```bash
  PBS_NODEFILE=NODEFILE check-mate-flush
  ```

## Simulation of job execution: hang, fail, success
The test_pyjob.py script allows you to simulate various job behaviors:
```bash
--hang N              # Hang for N seconds
--fail N              # Fail after N seconds
--compute T           # Compute time per iteration
--niters NITERS       # Total number of iterations
--checkpoint PATH     # Checkpoint file path
--checkpoint_time T   # Time to write a single checkpoint
```

```
python test_pyjob.py --fail 120 --checkpoint ./chkpt --niters 1000
```


## Example submission scripts
- [qsub_multi_mpiexec.sc](./qsub_multi_mpiexec.sc)
  submission script doing continual trials of mpiexec until success or timeout

## Various simulation examples
- [fail/](./fail): job failed after 100 seconds, restart
- [hang/](./hang): job hang, kill and restart
- [success/](./success): job run seccessfully
- [nan/](./nan): NaN after a few iterations, restart

## Checkpoint interval optimization utility
- [optimal_checkpointing.py](./optimal_checkpointing.py)
  Determine the optimal time interval of computation between checkpoints
  for a job of determined node size and checkpointed memory per node
