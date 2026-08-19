# Zone Job Scheduler & Deadlock Safety Engine

## Task 8 — Production Deployment Recommendation

### Production Algorithm Choice: SRTF

For the zone-controller workload, I would choose the SJF/SRTF
algorithm family, specifically SRTF, as the production scheduling
algorithm.

SRTF produced the lowest measured average waiting time of 11.500
ticks for the given fixed job set. This is better than FCFS at
18.375 ticks, showing that SRTF can significantly reduce the time
jobs spend waiting in the ready queue.

### Why the Other Algorithm Families Are Less Suitable

#### 1. FCFS

FCFS produced an average waiting time of 18.375 ticks, which is
higher than SRTF's 11.500 ticks. Therefore, FCFS provides poorer
waiting-time performance for this workload.

#### 2. Round Robin

Round Robin produced average waiting times of 22.625 ticks with
a quantum of 3 and 20.375 ticks with a quantum of 6. The quantum-3
run also produced 16 context switches compared with 10 context
switches for quantum 6. Therefore, Round Robin has higher measured
waiting time and can introduce additional scheduling overhead when
the quantum is small.

#### 3. Priority Scheduling

Non-preemptive priority scheduling without aging produced an
average waiting time of 14.125 ticks, which is still higher than
SRTF's 11.500 ticks. The no-aging run also caused Z3-J02 to wait
33 ticks, demonstrating the possibility of long waits for lower-
priority jobs.

### Final Decision

SRTF is selected because it achieved the lowest measured average
waiting time of 11.500 ticks for this workload while preserving
the preemptive behavior needed to react to shorter jobs as they
arrive.

## Part 2 — Cloud, Security & IoT Deployment Blueprint

The complete Tasks 9–14 deployment blueprint is available here:

[Architecture Blueprint](docs/architecture_blueprint.md)
