# Methodology

## Purpose

This first version compares bandwidth allocation rules on a generated workload. It is a learning and prototyping exercise. It describes specific university network.

## Workload

A random number generator with a fixed seed gives each user a demand within the range set in the config file. Each user also gets a weight, and a share of users is marked as high priority. All three policies use the same demands, weights and priority labels, so the comparison is fair.

## Policies

- **Equal:** capacity is divided evenly. A user never receives more than their demand, and unused capacity is passed on to users who still want more.
- **Priority:** a set fraction of the link is reserved for high-priority users. The remaining capacity goes to the other users. Anything still unused is given to users with unmet demand.
- **Weighted:** capacity is divided in proportion to each user's weight, capped at their demand.

No user can receive more than they asked for, and the total can never go above the link capacity.

## Metrics

- **Utilization:** total allocated Mbps divided by link capacity.
- **Jain's fairness index on allocation:** calculated from the Mbps each user received.
- **Satisfaction:** allocated Mbps divided by demand, for each user. Jain's index is also calculated on this value, and the average is reported separately for high-priority and standard users.
- **Unmet-demand fraction and delay estimate:** simple proxies. The delay estimate is a function of utilization only and levels off at its maximum when the link is full. Neither one is a real measurement of delay or packet loss.

## Why two fairness measures

Jain's index on raw Mbps gives its best score when every user gets the same amount, so equal sharing will usually win. That ignores that users ask for different amounts. The satisfaction version compares how much of each user's own demand was met. The two can rank the policies differently, so both are reported.

## Reproducing results

The config file stores the seed and all model settings. Running the script with the same config and the same library versions gives the same output.

## Limitations

The model has no packet queues, TCP congestion control, Wi-Fi contention, protocol overhead, routing or traffic that changes over time. It cannot show how a real campus network behaves. A later version should use a packet-level simulator or a small test network, and the assumptions should be checked with a supervisor.
