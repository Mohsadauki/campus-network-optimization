# Campus Network Optimization and Fair Bandwidth Allocation

## About this project

Universities depend on reliable internet access for teaching, research, and administration. When many people share a limited connection, some users may experience slower speeds or longer delays.

This project is a small, reproducible starting point for exploring how different bandwidth-allocation rules affect users sharing a constrained link. It uses a synthetic workload so the experiment can be run without access to a real campus network.

**Important:** this is an educational allocation model, not a packet-level network simulator. Its delay and packet-loss values are illustrative estimates, not measurements from a real network.

## Research question

How do equal, priority-based, and weighted bandwidth allocation compare when users have different levels of demand?

## Allocation policies

- **Equal share:** capacity is divided evenly among users, subject to each user's demand.
- **Priority-based:** a configurable share of capacity is reserved for high-priority users; remaining capacity is shared among users who still have unmet demand.
- **Weighted share:** users receive capacity in proportion to their configured weights, subject to their demand.

The model reallocates unused capacity when a user does not need its initial share.

## Metrics

The script reports:
- Allocated throughput per user (Mbps)
- Total allocated throughput and link utilization
- Jain's fairness index across users' allocated throughput
- An illustrative delay estimate
- An illustrative loss estimate based on unmet demand

The delay and loss formulas are simple heuristics used to demonstrate analysis workflows. They are not validated models of real network queues or packet transmission.

## Project files

```text
campus-network-optimization/
├── README.md
├── requirements.txt
├── .gitignore
├── config/
│   └── experiment.json
├── src/
│   └── simulate.py
├── tests/
│   └── test_simulate.py
├── docs/
│   └── methodology.md
└── results/
    └── .gitkeep
```

## Run on an Android phone

You can keep the code on GitHub using your phone. To run it, use a browser-based Python environment such as [Google Colab](https://colab.research.google.com/).

1. Upload the repository files to Colab, or upload the repository ZIP and extract it.
2. Install the requirements:

   ```python
   !pip install -r requirements.txt
   ```

3. Run the experiment:

   ```python
   !python src/simulate.py --config config/experiment.json --outdir results
   ```

If you use a local computer later, Python 3.10 or newer is recommended.

## Outputs

The script creates:
- `user_results.csv` — per-user demand and allocation for each policy
- `summary.csv` — summary metrics for each policy
- `summary.png` — a chart comparing throughput, fairness, and illustrative estimates

The same configuration and random seed produce the same synthetic demand and weights. Keep the configuration alongside any results you report.

## Suggested experiments

1. Run the baseline configuration.
2. Change `capacity_mbps` to 20, 50, and 100.
3. Change the number of users to 10, 20, and 50.
4. Repeat with multiple seeds and compare averages.
5. Discuss trade-offs, especially where improving one group's allocation may reduce fairness for others.

Change one parameter at a time when possible, and record each configuration used.

## Limitations and next steps

This model does not simulate packets, TCP/UDP behavior, wireless interference, queue scheduling, routing, or protocol overhead. Its delay and loss values are illustrative only. The results should not be described as measurements of Yobe State University's network.

A future version could validate the question in Mininet or another packet-level network simulator and compare the simplified model with measured results from a controlled testbed.

## Research integrity

This repository starts with a simulation model, not a completed campus-network study. Run the code before reporting results. Describe the setup, assumptions, and limitations clearly, and do not claim real-world improvements without suitable evidence.

## Author

**Muhammad Ali Abubakar**

- GitHub: [@Mohsadauki](https://github.com/Mohsadauki)
- Email: [muhammadaliabubakar6@gmail.com](mailto:muhammadaliabubakar6@gmail.com)
