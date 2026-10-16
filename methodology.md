# Methodology and assumptions

## Purpose

This first version compares allocation rules using a generated workload. It is intended as a learning and research-prototyping exercise, not a model of a specific university network.

## Workload

A seeded pseudo-random generator creates each user's offered demand within the configured range. Each user also receives a weight, and a subset is labelled high priority. All policies use the same generated demands and labels for a fair baseline comparison.

## Policies

- Equal: proportional allocation with all weights equal to one.
- Priority: reserve the configured fraction of link capacity for high-priority users, then allocate remaining capacity to standard users; any unused capacity is redistributed to unmet demand.
- Weighted: proportional allocation using the generated per-user weights.

Allocations cannot exceed demand or total link capacity.

## Metrics

Jain's fairness index is calculated from allocated throughput. Utilization is total allocated throughput divided by link capacity. The unmet-demand fraction is a proxy for demand that the model could not serve.

The reported delay value is a simple function of utilization, and the unmet-demand fraction is not actual packet loss. These proxies are included to demonstrate how metrics can be recorded, but should not be presented as measured network delay or packet loss.

## Reproducibility

The configuration file records the seed and model parameters. Running the script with the same version of Python libraries and same configuration should reproduce the generated workload and outputs.

## Limitations

The model has no packet queues, TCP congestion control, Wi-Fi contention, protocol overhead, routing, or time-varying traffic. It does not establish how a real campus network would behave. A later version should use a packet-level simulator or controlled testbed and validate assumptions with a supervisor.
