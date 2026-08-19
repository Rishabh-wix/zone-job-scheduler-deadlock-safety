from jobs import JOBS


def round_robin(jobs, quantum):
    remaining = {
        job["job_id"]: job["burst_time"]
        for job in jobs
    }

    completion_time = {}
    first_start = {}

    ready_queue = []
    arrived = set()

    current_time = 0
    context_switches = 0
    dispatch_count = 0
    previous_job = None

    while len(completion_time) < len(jobs):

        # Add jobs that have arrived
        for job in sorted(jobs, key=lambda x: (x["arrival_time"], x["job_id"])):
            if (
                job["arrival_time"] <= current_time
                and job["job_id"] not in arrived
                and remaining[job["job_id"]] > 0
            ):
                ready_queue.append(job["job_id"])
                arrived.add(job["job_id"])

        # If queue is empty, jump to next arrival
        if not ready_queue:
            next_arrival = min(
                job["arrival_time"]
                for job in jobs
                if job["job_id"] not in arrived
                and remaining[job["job_id"]] > 0
            )

            current_time = next_arrival

            for job in sorted(
                jobs,
                key=lambda x: (x["arrival_time"], x["job_id"])
            ):
                if (
                    job["arrival_time"] <= current_time
                    and job["job_id"] not in arrived
                    and remaining[job["job_id"]] > 0
                ):
                    ready_queue.append(job["job_id"])
                    arrived.add(job["job_id"])

        job_id = ready_queue.pop(0)

        # Count a dispatch
        dispatch_count += 1

        # A context switch occurs when the running job changes
        if previous_job is not None and previous_job != job_id:
            context_switches += 1

        previous_job = job_id

        if job_id not in first_start:
            first_start[job_id] = current_time

        run_time = min(quantum, remaining[job_id])

        start_time = current_time
        end_time = current_time + run_time

        # Handle arrivals during this time slice.
        # Arrivals exactly at the quantum-expiry tick are added
        # before the expired job is re-added.
        for job in sorted(
            jobs,
            key=lambda x: (x["arrival_time"], x["job_id"])
        ):
            if (
                job["arrival_time"] <= end_time
                and job["job_id"] not in arrived
                and remaining[job["job_id"]] > 0
            ):
                if job["arrival_time"] < end_time:
                    ready_queue.append(job["job_id"])
                    arrived.add(job["job_id"])

        remaining[job_id] -= run_time
        current_time = end_time

        # Add jobs arriving exactly at this tick first
        for job in sorted(
            jobs,
            key=lambda x: (x["arrival_time"], x["job_id"])
        ):
            if (
                job["arrival_time"] == current_time
                and job["job_id"] not in arrived
                and remaining[job["job_id"]] > 0
            ):
                ready_queue.append(job["job_id"])
                arrived.add(job["job_id"])

        if remaining[job_id] == 0:
            completion_time[job_id] = current_time
        else:
            # Expired job goes to the back AFTER new arrivals
            ready_queue.append(job_id)

    results = []

    for job in jobs:
        job_id = job["job_id"]

        turnaround_time = (
            completion_time[job_id] - job["arrival_time"]
        )

        waiting_time = (
            turnaround_time - job["burst_time"]
        )

        results.append({
            "job_id": job_id,
            "waiting_time": waiting_time,
            "turnaround_time": turnaround_time,
            "completion_time": completion_time[job_id]
        })

    total_waiting = sum(
        result["waiting_time"] for result in results
    )

    total_turnaround = sum(
        result["turnaround_time"] for result in results
    )

    return (
        results,
        total_waiting / len(jobs),
        total_turnaround / len(jobs),
        context_switches,
        dispatch_count
    )


def print_results(quantum, results, avg_waiting, avg_turnaround,
                  context_switches, dispatch_count):

    print(f"\nRound Robin - Quantum {quantum}")
    print("-" * 65)

    print(
        f"{'Job':<10}"
        f"{'Waiting':<12}"
        f"{'Turnaround':<12}"
        f"{'Completion':<12}"
    )

    for result in results:
        print(
            f"{result['job_id']:<10}"
            f"{result['waiting_time']:<12}"
            f"{result['turnaround_time']:<12}"
            f"{result['completion_time']:<12}"
        )

    print("-" * 65)
    print(f"Average Waiting Time    : {avg_waiting:.3f}")
    print(f"Average Turnaround Time : {avg_turnaround:.3f}")
    print(f"Dispatches              : {dispatch_count}")
    print(f"Context Switches        : {context_switches}")


if __name__ == "__main__":

    # Required runs
    for quantum in [3, 6]:

        (
            results,
            avg_waiting,
            avg_turnaround,
            context_switches,
            dispatch_count
        ) = round_robin(JOBS, quantum)

        print_results(
            quantum,
            results,
            avg_waiting,
            avg_turnaround,
            context_switches,
            dispatch_count
        )
