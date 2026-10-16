# Campus Network Optimization: Fair Bandwidth Allocation

When many people share a small internet connection, some get slow speeds while others get plenty. This project is a small simulation I built to compare three ways of sharing a limited link among users who want different amounts of bandwidth.

**Please note:** this is a simple allocation model . It is a packet level network simulator, and the numbers are measurements of a real network, including the Yobe State University network.

## Research question

How do equal, priority and weighted sharing compare when users have different demands?

## The three policies

- **Equal:** every user gets the same share, but nobody gets more than they asked for. Unused capacity goes to users who still want more.
- **Priority:** part of the capacity is kept for high-priority users. The rest is shared among the other users, and any leftover goes to whoever still has unmet demand.
- **Weighted:** users get capacity in proportion to a weight, again capped at their demand.

## What the script reports

- How much each user asked for and how much they got (Mbps)
- Total allocated throughput and link utilization
- Jain's fairness index on the allocated Mbps
- Jain's fairness index on the share of demand each user got (satisfaction)
- Average satisfaction for high-priority and standard users
- A rough delay estimate and an unmet-demand figure (both simple proxies, not real delay or packet loss)

I report two fairness numbers because they can rank the policies differently. Jain's index on raw Mbps rewards giving everyone the same amount, even if some users asked for much less. The satisfaction version looks at how much of each user's own demand was served.

## Folder layout

```text
campus-network-optimization/
  README.md
  requirements.txt
  config/experiment.json
  src/simulate.py
  tests/test_simulate.py
  docs/methodology.md
  results/
```

## How to run it

On a computer, or on a phone using Google Colab:

```text
pip install -r requirements.txt
python src/simulate.py --config config/experiment.json --outdir results
```

To run the tests:

```text
python -m unittest tests.test_simulate
```

The script writes three files into the results folder: `user_results.csv`, `summary.csv` and `summary.png`. The same config file and seed always give the same results, so keep the config with any results you report.

## Things to try

1. Run the default config.
2. Change `capacity_mbps` to 20, 50 and 100.
3. Change the number of users to 10, 20 and 50.
4. Repeat with several seeds and average the results.

Change one thing at a time and write down the settings you used.

## What to know before reading the results

- When total demand is higher than capacity, all three policies use the whole link. Total throughput, utilization and the delay estimate then come out the same for every policy, so only the fairness and satisfaction figures separate them.
- When capacity is higher than total demand, everyone gets everything they asked for and the policies give identical results.
- The model has no packets, TCP behaviour, wireless interference or routing. A next step would be to test the same question in a packet-level simulator such as Mininet and compare.

## Author

Muhammad Ali Abubakar
GitHub: [@Mohsadauki](https://github.com/Mohsadauki)
Email: muhammadaliabubakar6@gmail.com
