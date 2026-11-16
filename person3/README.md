# Person 3 – Monitoring and Performance Evaluation

## Scope
Person 3 is responsible for monitoring TCP content-server availability and measuring application-level response time and throughput, then documenting performance observations.

## Files
- `person3_monitor.py` – copy the monitoring script from the project `person3/` directory.
- `normal.csv` – five-round Mininet normal-operation measurements for Server1 and Server2.
- `response_time.png` – comparison of average response time from `normal.csv`.
- `throughput.png` – comparison of average application-level throughput from `normal.csv`.

## Test environment and method
The measurements were collected in the Mininet topology. Server1 was addressed at `10.0.0.2:5001` and Server2 at `10.0.0.3:5002`. The monitor issued five content-request rounds to each server and recorded success, response time, response bytes and application-level throughput.

Response time is recorded in milliseconds. Throughput is recorded in bytes per second and is calculated at the application level; it is not physical link capacity.

## Normal-operation results

| Metric | Server1 | Server2 |
|---|---:|---:|
| Successful requests | 5/5 | 5/5 |
| Average response time | 28.66 ms | 28.99 ms |
| Average throughput | 1432.00 B/s | 1415.79 B/s |

Both servers successfully served all five requests. In this run, Server1 had a slightly lower average response time and slightly higher average application-level throughput. These are observations from this specific Mininet run, not a claim about general performance.

## Integrated gateway failure and recovery evidence
Separate gateway-client tests were performed:
- Normal: both backends reported UP; the gateway selected Server2 and delivered `file1`.
- Failure test: after the attempted Server2 stop, both backends were reported DOWN and the gateway returned “No healthy backend”. This did not demonstrate successful failover because Server1 was also unavailable at that moment.
- Partial recovery: Server1 was restarted while Server2 remained DOWN; the gateway selected Server1 and delivered `file1`.
- Recovery: both servers reported UP; the gateway selected Server1 and delivered `file1`.

These gateway tests were observed in terminal output/screenshots. They are separate from the direct-server measurements in `normal.csv`. Do not describe `normal.csv` as gateway-only performance data.

## Remaining evidence to add
If further monitoring runs are completed, add separately collected Mininet failure and recovery CSVs. Do not label older localhost CSVs or a refused connection to an unused port as Mininet failure/recovery measurements.

## Limitations
- Results are from an emulated Mininet network.
- Throughput is application-level and based on the small response payload.
- The monitor represented by `person3_monitor.py` tests backend servers directly; gateway selection/failover is evidenced separately by gateway-client output.
