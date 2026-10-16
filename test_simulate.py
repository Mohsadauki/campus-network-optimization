import unittest
import numpy as np

from src.simulate import (
    allocate_with_weights,
    equal_allocation,
    jains_fairness,
    priority_allocation,
    run_experiment,
)


class AllocationTests(unittest.TestCase):
    def test_fairness_equal_values_is_one(self):
        self.assertAlmostEqual(jains_fairness(np.array([2.0, 2.0, 2.0])), 1.0)

    def test_fairness_nonnegative(self):
        self.assertGreaterEqual(jains_fairness(np.array([1.0, 3.0, 5.0])), 0.0)
        self.assertLessEqual(jains_fairness(np.array([1.0, 3.0, 5.0])), 1.0)

    def test_equal_allocation_respects_capacity_and_demand(self):
        demand = np.array([10.0, 10.0, 10.0])
        allocation = equal_allocation(demand, 12.0)
        self.assertAlmostEqual(float(np.sum(allocation)), 12.0)
        self.assertTrue(np.all(allocation <= demand + 1e-9))

    def test_weighted_allocation_respects_capacity(self):
        demand = np.array([10.0, 10.0, 10.0])
        allocation = allocate_with_weights(demand, 12.0, np.array([1.0, 2.0, 3.0]))
        self.assertAlmostEqual(float(np.sum(allocation)), 12.0)
        self.assertTrue(np.all(allocation >= 0.0))
        self.assertTrue(np.all(allocation <= demand + 1e-9))

    def test_priority_allocation_respects_capacity(self):
        demand = np.array([8.0, 8.0, 8.0, 8.0])
        high = np.array([True, False, False, False])
        allocation = priority_allocation(demand, 10.0, high, 0.5)
        self.assertLessEqual(float(np.sum(allocation)), 10.0 + 1e-9)
        self.assertTrue(np.all(allocation <= demand + 1e-9))

    def test_run_is_reproducible(self):
        config = {
            "seed": 10, "capacity_mbps": 20, "users": 5,
            "demand_min_mbps": 1, "demand_max_mbps": 8,
            "priority_fraction": 0.3, "high_priority_fraction": 0.2,
            "weight_min": 1, "weight_max": 4,
            "base_delay_ms": 10, "congestion_delay_scale_ms": 80,
        }
        users1, summary1 = run_experiment(config)
        users2, summary2 = run_experiment(config)
        self.assertTrue(users1.equals(users2))
        self.assertTrue(summary1.equals(summary2))


class ModelBehaviourTests(unittest.TestCase):
    config = {
        "seed": 10, "capacity_mbps": 20, "users": 10,
        "demand_min_mbps": 2, "demand_max_mbps": 10,
        "priority_fraction": 0.5, "high_priority_fraction": 0.3,
        "weight_min": 1, "weight_max": 4,
        "base_delay_ms": 10, "congestion_delay_scale_ms": 80,
    }

    def test_total_allocation_never_exceeds_capacity(self):
        _, summary = run_experiment(self.config)
        self.assertTrue((summary["total_allocated_mbps"] <= self.config["capacity_mbps"] + 1e-6).all())

    def test_satisfaction_is_between_zero_and_one(self):
        users, _ = run_experiment(self.config)
        self.assertTrue(users["satisfaction"].between(0, 1).all())

    def test_priority_policy_serves_high_priority_users_better(self):
        _, summary = run_experiment(self.config)
        row = summary[summary["policy"] == "priority"].iloc[0]
        self.assertGreater(row["mean_satisfaction_high_priority"],
                           row["mean_satisfaction_standard"])


if __name__ == "__main__":
    unittest.main()
