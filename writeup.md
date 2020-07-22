`get_counts` was executed on all public thin and thick clients on July 21, 2020.

The minimum uptime across all servers was 880197 seconds (~10 days).
The maximum uptime across all servers was 4032565 seconds (~46 days).
The total uptime across all servers was 150041637 seconds (~1736 days).

Database reads is defined as nodestore reads for which the SHAMap node is not in
the TreeNodeCache

For each host, the database reads per second is defined as total database reads
divided by total uptime in seconds.

The sum of all database reads per second is 3973.5.

If all of these client handlers are replaced by reporting mode servers, every
database read on every server will hit the same Cassandra cluster. Therefore,
during this period, the Cassandra cluster would have received an average of
3973.5 reads per second. A Cassandra cluster on EC2, consisting of 10 i3.2xlarge
machines, was able to sustain over 150k reads per second; the Cassandra cluster
could handle 37.5 times the read volume observed during this period.

Note, that reporting mode servers do not execute any consensus code, which would
presumably result in less total database reads. At any time, there is only one
reporting mode server building the next ledger. A reporting mode server builds
the next ledger by extracting all new, modified or deleted leaf nodes via an ETL
process, and inserting those leaf nodes into the previous ledger. Inserting leaf
nodes usually requires some database reads, as any inner nodes on the path from
root to leaf that are not in the TreeNodeCache must be read from the database.
One can assume that building the next ledger results in about the same amount of
reads as running consensus. However, only one server across the entire cluster
is building the next ledger, versus the current situation where every server is
participating in consensus. 
