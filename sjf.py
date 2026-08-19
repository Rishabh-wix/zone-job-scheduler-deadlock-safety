from jobs import JOBS


def sjf(jobs):
    current_time = 0
    completed = set()
    results = []

    while len(completed) < len(jobs):

        # Jobs that have already arrived and are not completed
        ready = [
            job for job in jobs
            if job["job_id"] not in completed
            and job["arrival_time"] <= current_time
        ]

        # If no job has arrived yet, jump to next arrival
        if not ready:
            current_time = min(
                job["arrival_time"]
                for job in jobs
                if job["job_id"] not in completed
            )
            continue

        # SJF:
        # shortest burst first
        # tie -> earlier arrival
        # tie -> lower job_id
        job = min(
            ready,
            key=lambda x: (
                x["burst_time"],
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
            "arrival_time": job["arrival_time"],
            "burst_time": job["burst_time"],
            "start_time": start_time,
            "completion_time": completion_time,
            "waiting_time": waiting_time,
            "turnaround_time": turnaround_time
        })

        current_time = completion_time
        completed.add(job["job_id"])

    return results


def print_results(results):
    print("\nNon-Preemptive SJF Scheduling")
    print("-" * 75)

    print(
        f"{'Job':<10}"
        f"{'Arrival':<10}"
        f"{'Burst':<8}"
        f"{'Start':<8}"
        f"{'Complete':<10}"
        f"{'Waiting':<10}"
        f"{'Turnaround':<12}"
    )

    total_waiting = 0
    total_turnaround = 0

    for result in results:
        print(
            f"{result['job_id']:<10}"
            f"{result['arrival_time']:<10}"
            f"{result['burst_time']:<8}"
            f"{result['start_time']:<8}"
            f"{result['completion_time']:<10}"
            f"{result['waiting_time']:<10}"
            f"{result['turnaround_time']:<12}"
        )

        total_waiting += result["waiting_time"]
        total_turnaround += result["turnaround_time"]

    n = len(results)

    print("-" * 75)
    print(f"Average Waiting Time    : {total_waiting / n:.3f}")
    print(f"Average Turnaround Time : {total_turnaround / n:.3f}")


if __name__ == "__main__":
    results = sjf(JOBS)
    print_results(results)
