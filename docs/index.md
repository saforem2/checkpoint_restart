# Check Mate

`check_mate` bundles the monitoring utilities that power the Check Mate
checkpoint/restart workflow. Use the package to:

- keep an eye on checkpoints with `check-hang`
- kill jobs that emit `NaN`/`Inf` tokens with `check-nan`
- rebuild clean allocations with `check-mate get-healthy-nodes`
- compute optimal checkpoint cadences via the Python API

The documentation is organised into the following guides:

| Guide | Summary |
| --- | --- |
| [Getting started](getting-started.md) | Install the package, verify the CLI, and run your first monitors. |
| [CLI reference](cli.md) | Complete documentation for every bundled command with worked examples. |
| [Python API](python-api.md) | Programmatic access to checkpoint cadence modelling helpers. |
| [Workflow recipes](workflows.md) | Combine the tools into resilient batch scripts. |

## Quick demo

Once the package is installed you can confirm the CLI entry point and Python
API in a few commands:

```bash
$ check-mate --version
check-mate 0.1.0
```

```python
>>> from check_mate import optimal_checkpointing as oc
>>> cadence = oc.optimal_checkpoint_cadence(
...     node_count=1024,
...     node_memory=2.5e11,
...     chkpt_bandwidth="DAOS-128",
... )
>>> f"{cadence:.3f} h"
'6.951 h'
```

Head to the individual guides for detailed explanations, diagrams, and
step-by-step walkthroughs.
