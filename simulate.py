"""Reproducible toy model for comparing bandwidth allocation policies.

This is not a packet-level network simulator. Delay and loss are illustrative
heuristics so that the project can demonstrate an end-to-end experiment workflow.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def jains_fairness(values: np.ndarray) -> float:
    """Jain's fairness index, between 0 and 1 for non-negative allocations."""
    values = np.asarray(values, dtype=float)
    if values.size == 0:
        return 1.0
    denominator = values.size * float(np.sum(values ** 2))
    if denominator == 0:
        return 1.0
    return float(np.sum(values) ** 2 / denominator)


def allocate_with_weights(demand: np.ndarray, capacity: float,
                          weights: np.ndarray) -> np.ndarray:
    """Allocate capacity proportionally to weights, respecting demand caps."""
    allocation = np.zeros_like(demand, dtype=float)
    remaining = min(float(capacity), float(np.sum(demand)))
    active = demand > 0
    while remaining > 1e-9 and np.any(active):
        active_weights = weights[active]
        proposed = remaining * active_weights / np.sum(active_weights)
        active_indices = np.flatnonzero(active)
        capped = proposed >= (demand[active] - allocation[active] - 1e-9)
        if not np.any(capped):
            allocation[active_indices] += proposed
            remaining = 0.0
        else:
            capped_indices = active_indices[capped]
            additions = demand[capped_indices] - allocation[capped_indices]
            allocation[capped_indices] += additions
            remaining -= float(np.sum(additions))
            active[capped_indices] = False
    return np.minimum(allocation, demand)


def equal_allocation(demand: np.ndarray, capacity: float) -> np.ndarray:
    return allocate_with_weights(demand, capacity, np.ones_like(demand, dtype=float))


def priority_allocation(demand: np.ndarray, capacity: float,
                        high_priority: np.ndarray, priority_fraction: float) -> np.ndarray:
    """Reserve a capacity fraction for high-priority users, then share leftovers."""
    allocation = np.zeros_like(demand, dtype=float)
    high = np.asarray(high_priority, dtype=bool)
    low = ~high
    high_capacity = min(capacity * priority_fraction, float(np.sum(demand[high])))
    allocation[high] = allocate_with_weights(
        demand[high], high_capacity, np.ones(np.count_nonzero(high), dtype=float)
    )
    remaining = capacity - float(np.sum(allocation))
    if np.any(low) and remaining > 0:
        allocation[low] = allocate_with_weights(
            demand[low], remaining, np.ones(np.count_nonzero(low), dtype=float)
        )
    # If high-priority demand was below its reserved amount, use leftover capacity
    # for any users who still have unmet demand.
    remaining = max(0.0, capacity - float(np.sum(allocation)))
    if remaining > 1e-9:
        unmet = demand - allocation
        extra = allocate_with_weights(unmet, remaining, np.ones_like(demand, dtype=float))
        allocation += extra
    return np.minimum(allocation, demand)


def run_experiment(config: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Run all policies on the same generated user demands."""
    rng = np.random.default_rng(int(config["seed"]))
    n = int(config["users"])
    capacity = float(config["capacity_mbps"])
    demand = rng.uniform(float(config["demand_min_mbps"]),
                         float(config["demand_max_mbps"]), size=n)
    weights = rng.integers(int(config["weight_min"]), int(config["weight_max"]) + 1, size=n)
    high_count = max(1, int(round(n * float(config["high_priority_fraction"]))))
    high_priority = np.zeros(n, dtype=bool)
    high_priority[rng.choice(n, size=min(high_count, n), replace=False)] = True

    allocations = {
        "equal": equal_allocation(demand, capacity),
        "priority": priority_allocation(
            demand, capacity, high_priority, float(config["priority_fraction"])
        ),
        "weighted": allocate_with_weights(demand, capacity, weights.astype(float)),
    }

    user_rows = []
    summary_rows = []
    base_delay = float(config["base_delay_ms"])
    delay_scale = float(config["congestion_delay_scale_ms"])

    for policy, allocation in allocations.items():
        # Illustrative proxies only; these are not packet-level delay/loss results.
        unmet_fraction = np.divide(
            np.maximum(demand - allocation, 0.0), demand,
            out=np.zeros_like(demand), where=demand > 0
        )
        utilization = float(np.sum(allocation) / capacity) if capacity > 0 else 0.0
        estimated_delay = base_delay + delay_scale * max(0.0, utilization - 0.70) / 0.30
        estimated_delay = min(estimated_delay, base_delay + delay_scale)
        fairness = jains_fairness(allocation)

        for i in range(n):
            user_rows.append({
                "policy": policy,
                "user_id": f"user_{i + 1:03d}",
                "priority_group": "high" if high_priority[i] else "standard",
                "weight": int(weights[i]),
                "demand_mbps": round(float(demand[i]), 4),
                "allocated_mbps": round(float(allocation[i]), 4),
                "unmet_demand_fraction_proxy": round(float(unmet_fraction[i]), 4),
                "estimated_delay_ms_illustrative": round(float(estimated_delay), 4),
            })

        summary_rows.append({
            "policy": policy,
            "users": n,
            "capacity_mbps": capacity,
            "total_demand_mbps": round(float(np.sum(demand)), 4),
            "total_allocated_mbps": round(float(np.sum(allocation)), 4),
            "utilization_fraction": round(utilization, 4),
            "jains_fairness_index": round(fairness, 4),
            "mean_unmet_demand_fraction_proxy": round(float(np.mean(unmet_fraction)), 4),
            "estimated_delay_ms_illustrative": round(float(estimated_delay), 4),
        })

    return pd.DataFrame(user_rows), pd.DataFrame(summary_rows)


def make_chart(summary: pd.DataFrame, output_path: Path) -> None:
    """Save a compact chart of total allocation and fairness by policy."""
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2))
    axes[0].bar(summary["policy"], summary["total_allocated_mbps"])
    axes[0].set_title("Total allocated throughput")
    axes[0].set_ylabel("Mbps")
    axes[1].bar(summary["policy"], summary["jains_fairness_index"])
    axes[1].set_title("Jain's fairness index")
    axes[1].set_ylabel("Index (0–1)")
    for ax in axes:
        ax.grid(axis="y", alpha=0.25)
    fig.suptitle("Toy-model results (not real network measurements)")
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="config/experiment.json")
    parser.add_argument("--outdir", default="results")
    args = parser.parse_args()

    config_path = Path(args.config)
    output_dir = Path(args.outdir)
    with config_path.open("r", encoding="utf-8") as handle:
        config = json.load(handle)

    if int(config["users"]) < 1:
        raise ValueError("'users' must be at least 1.")
    if float(config["capacity_mbps"]) <= 0:
        raise ValueError("'capacity_mbps' must be positive.")
    if not 0 <= float(config["priority_fraction"]) <= 1:
        raise ValueError("'priority_fraction' must be between 0 and 1.")
    if not 0 < float(config["high_priority_fraction"]) <= 1:
        raise ValueError("'high_priority_fraction' must be in (0, 1].")
    if float(config["demand_min_mbps"]) < 0 or float(config["demand_max_mbps"]) <= float(config["demand_min_mbps"]):
        raise ValueError("Demand range must satisfy 0 <= min < max.")

    output_dir.mkdir(parents=True, exist_ok=True)
    users, summary = run_experiment(config)
    users.to_csv(output_dir / "user_results.csv", index=False)
    summary.to_csv(output_dir / "summary.csv", index=False)
    make_chart(summary, output_dir / "summary.png")
    print("Experiment completed. These are synthetic toy-model results.")
    print(summary.to_string(index=False))
    print(f"\nWrote outputs to: {output_dir.resolve()}")


if __name__ == "__main__":
    main()
