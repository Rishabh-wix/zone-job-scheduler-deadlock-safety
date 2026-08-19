from jobs import JOBS


def priority_scheduling(jobs, aging=False):
    current_time = 0
    completed = set()
    results = []

    while len(completed) < len(jobs):

        ready = [
            job for job in jobs
            if job["job_id"] not in completed
            and job["arrival_time"] <= current_time
        ]

        # If no job has arrived yet
        if not ready:
            current_time = min(
                job["arrival_time"]
                for job in jobs
                if job["job_id"] not in completed
            )
            continue

        def effective_priority(job):
            if not aging:
                return job["priority"]

            ticks_waited = current_time - job["arrival_time"]

            return max(
                1,
                job["priority"] - (ticks_waited // 3)
            )

        # Lower effective priority number = higher priority
        job = min(
            ready,
            key=lambda x: (
                effective_priority(x),
                x["arrival_time"],
                x["job_id"]
            )
        )

        start_time = current_time
        completion_time = start_time + job["burst_time"]

        waiting_time = start_time - job["arrival_time"]

        turnaround_time = completion_time - job["arrival_time"]

        results.append({
            "job_id": job["job_id"],
            "priority": job["priority"],
            "waiting_time": waiting_time,
            "turnaround_time": turnaround_time,
            "start_time": start_time,
            "completion_time": completion_time
        })

        current_time = completion_time
        completed.add(job["job_id"])

    return results


def print_results(title, results):

    print("\n" + title)
    print("-" * 75)

    print(
        f"{'Job':<10}"
        f"{'Priority':<10}"
        f"{'Start':<10}"
        f"{'Complete':<12}"
        f"{'Waiting':<12}"
        f"{'Turnaround':<12}"
    )

    longest_job = None
    longest_wait = -1

    for result in results:

        print(
            f"{result['job_id']:<10}"
            f"{result['priority']:<10}"
            f"{result['start_time']:<10}"
            f"{result['completion_time']:<12}"
            f"{result['waiting_time']:<12}"
            f"{result['turnaround_time']:<12}"
        )

        if result["waiting_time"] > longest_wait:
            longest_wait = result["waiting_time"]
            longest_job = result["job_id"]

    print("-" * 75)
    print(
        f"Longest waiting job: {longest_job} "
        f"({longest_wait} ticks)"
    )


if __name__ == "__main__":

    # -------------------------------
    # Run 1: Without Aging
    # -------------------------------

    results_without_aging = priority_scheduling(
        JOBS,
        aging=False
    )

    print_results(
        "Priority Scheduling - WITHOUT Aging",
        results_without_aging
    )

    # -------------------------------
    # Run 2: With Aging
    # -------------------------------

    results_with_aging = priority_scheduling(
        JOBS,
        aging=True
    )

    print_results(
        "Priority Scheduling - WITH Aging",
        results_with_aging
    )
