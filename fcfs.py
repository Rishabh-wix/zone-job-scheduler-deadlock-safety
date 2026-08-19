from jobs import JOBS


def fcfs(jobs):
    current_time = 0
    results = []

    # FCFS: earlier arrival time first
    sorted_jobs = sorted(
        jobs,
        key=lambda job: (job["arrival_time"], job["job_id"])
    )

    for job in sorted_jobs:
        # CPU waits if the next job has not arrived yet
        if current_time < job["arrival_time"]:
            current_time = job["arrival_time"]

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

    return results


def print_results(results):
    print("\nFCFS Scheduling")
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
    results = fcfs(JOBS)
    print_results(results)
