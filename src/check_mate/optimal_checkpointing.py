"""Utilities for estimating optimal checkpoint cadences."""

from __future__ import annotations

import warnings

import numpy as np
from scipy.optimize import root_scalar

_MTBAI_TO_R0_FACTOR = 10624


def _validate_positive(name: str, value: float) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be positive")


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
    _validate_positive("node_count", node_count)
    _validate_positive("node_memory", node_memory)
    chkpt_bandwidth = _resolve_bandwidth(chkpt_bandwidth)
    _validate_positive("chkpt_bandwidth", chkpt_bandwidth)

    if R_0 is None:
        _validate_positive("MTBAI", MTBAI)
        R_0 = 1 / (MTBAI * _MTBAI_TO_R0_FACTOR)

    tau_c = (node_memory / chkpt_bandwidth) / 3600
    u_chk = tau_c * node_count**2
    z_chk = R_0 * u_chk

    def rootme(z_c: float, z_chk_val: float) -> float:
        return np.exp(-z_c - z_chk_val) - (1 - z_c)

    bracket = (0.0, max(1.5 * z_chk, 1.0))
    try:
        res = root_scalar(
            rootme,
            args=(z_chk,),
            bracket=bracket,
            method="brentq",
        )
    except ValueError as exc:  # pragma: no cover - rare numerical failures
        raise RuntimeError(
            "Could not bracket root for rootme(z_c, z_chk) "
            f"with z_chk={z_chk} and bracket={bracket}."
        ) from exc

    if not res.converged:
        f_bracket_min = rootme(bracket[0], z_chk)
        f_bracket_max = rootme(bracket[1], z_chk)
        n_iter = getattr(res, "iterations", "N/A")
        raise RuntimeError(
            "Root-find convergence failure for bracket=("
            f"{bracket[0]}, {bracket[1]}). "
            f"Function values: f({bracket[0]})={f_bracket_min}, "
            f"f({bracket[1]})={f_bracket_max}. Iterations: {n_iter}."
        )

    z_c = res.root
    u_c = z_c / R_0
    return u_c / node_count


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
    _validate_positive("T_c", T_c)
    _validate_positive("T_w", T_w)

    t_c = optimal_checkpoint_cadence(
        node_count,
        node_memory,
        MTBAI=MTBAI,
        chkpt_bandwidth=chkpt_bandwidth,
        R_0=R_0,
    )
    _validate_positive("t_c", t_c)
    if t_c < 0.1:
        warnings.warn(
            (
                "Computed optimal checkpoint cadence is very small "
                f"(t_c={t_c:.4f} h); efficiency results may not be meaningful."
            ),
            UserWarning,
            stacklevel=2,
        )

    return np.exp(-(T_c + T_w) / t_c)


__all__ = [
    "optimal_checkpoint_cadence",
    "compute_efficiency",
]
