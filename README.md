# Checkpoint / Restart tests on exascale computing systems

This repository hosts a synthetic workload, monitoring utilities, and
PBS batch scripts used to explore fault tolerance strategies on large
Aurora-like systems.  The tools model common failure modes (hangs,
mid-run exits, and successful completions) and demonstrate how to
restart automatically when issues occur.

- **Synthetic workload** – [`test_pyjob.py`](./test_pyjob.py) simulates a
  long-running MPI job with configurable iteration time, failure, and
  hang behavior.
- **Monitoring & control** – [`check_hang.py`](./check_hang.py) and
  helper shell scripts watch for hung jobs, select healthy nodes, and
  flush processes prior to retries.
- **Batch orchestration** – [`qsub_multi_mpiexec.sc`](./qsub_multi_mpiexec.sc)
  and [`qsub_multi_qsub.sc`](./qsub_multi_qsub.sc) illustrate retry and
  self-resubmission workflows on PBS clusters.

For a step-by-step walkthrough covering local simulations, monitoring,
node management, and batch scheduling integration, see the
[Repository Usage Guide](./docs/usage_guide.md).  Sequence diagrams and
flow descriptions for the shell helpers are available in
[`docs/shell_scripts.md`](./docs/shell_scripts.md).

## Quick start

1. Clone the repository and (optionally) activate a Python virtual
   environment.
2. Make the Python helpers executable and add the repository to your
   `PATH` if you plan to call them from other directories.
3. Launch a local simulation to observe the logging and checkpointing
   behavior:

   ```bash
   python test_pyjob.py --compute 1 --niters 5 --output demo.log
   ```

4. Combine the workload with `check_hang.py` and the PBS scripts to test
   retry strategies inside an allocation.

## Repository layout

- [`docs/`](./docs) – High-level usage guide and shell script
  documentation.
- [`examples/`](./examples) – Sample configurations demonstrating
  success, hang, fail, and resubmission scenarios.
- [`flush.sh`](./flush.sh) – Cleans residual processes from allocated
  nodes (except the head node).
- [`get_healthy_nodes.sh`](./get_healthy_nodes.sh) – Selects a subset of
  healthy nodes from an allocation.
- [`local_rank.sh`](./local_rank.sh) – Prepares rank metadata for MPI
  launches.
- [`optimal_checkpointing.py`](./optimal_checkpointing.py) – Estimates
  checkpoint intervals based on system characteristics.

## Support

For questions, please contact Huihuo Zheng
(`<huihuo.zheng@anl.gov>`).
