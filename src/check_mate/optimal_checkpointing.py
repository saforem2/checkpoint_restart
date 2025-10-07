"""Utilities for estimating optimal checkpoint cadences."""

from __future__ import annotations


def _resolve_bandwidth(value: float | int | str) -> float:
    if value == "DAOS-128":
        return 5000.0
    if value == "LUSTRE":
        return 650.0
    if isinstance(value, (float, int)):
        return float(value)
    raise TypeError('chkpt_bandwidth must be float, "DAOS-128", or "LUSTRE"')


def optimal_checkpoint_cadence(
    node_count: int,
    node_memory: float,
    MTBAI: float = 0.67,
    chkpt_bandwidth: float | int | str = "DAOS-128",
    R_0: float | None = None,
) -> float:
    """Calculate the optimal checkpoint cadence in hours."""
    import numpy as np
    from scipy.optimize import root_scalar

    if R_0 is None:
        R_0 = 1 / (MTBAI * 10624)

    chkpt_bandwidth = _resolve_bandwidth(chkpt_bandwidth)
    tau_c = (node_memory / chkpt_bandwidth) / 3600
    u_chk = tau_c * node_count**2
    z_chk = R_0 * u_chk

    def rootme(z_c, z_chk):
        return np.exp(-z_c - z_chk) - (1 - z_c)

    bracket_min = 0.0
    bracket_max = max(1.5 * z_chk, 1.0)

    res = root_scalar(rootme, args=(z_chk,), bracket=(bracket_min, bracket_max))
    if not res.converged:
        raise RuntimeError(
            "Root-find convergence failure for bracket=("
            f"{bracket_min}, {bracket_max})."
        )

    z_c = res.root
    u_c = z_c / R_0
    t_c = u_c / node_count
    return t_c


def compute_efficiency(
    node_count: int,
    node_memory: float,
    MTBAI: float = 0.67,
    chkpt_bandwidth: float | int | str = "DAOS-128",
    R_0: float | None = None,
    T_c: float = 4.0,
    T_w: float = 3.0,
) -> float:
    """Compute expected efficiency for the given checkpoint parameters."""
    import numpy as np

    t_c = optimal_checkpoint_cadence(
        node_count,
        node_memory,
        MTBAI=MTBAI,
        chkpt_bandwidth=chkpt_bandwidth,
        R_0=R_0,
    )
    if T_c <= 0:
        raise ValueError("T_c must be positive")
    if T_w <= 0:
        raise ValueError("T_w must be positive")

    return np.exp(-(T_c + T_w) / t_c)


__all__ = [
    "optimal_checkpoint_cadence",
    "compute_efficiency",
]
