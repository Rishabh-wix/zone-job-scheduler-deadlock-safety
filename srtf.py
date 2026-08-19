from jobs import JOBS


def srtf(jobs):
    remaining = {
        job["job_id"]: job["burst_time"]
        for job in jobs
    }

    completion_times = {}
    start_times = {}

    current_time = 0
    completed_count = 0

    while completed_count < len(jobs):

        ready = [
            job for job in jobs
            if job["arrival_time"] <= current_time
            and remaining[job["job_id"]] > 0
        ]

        # CPU idle
        if not ready:
            current_time = min(
                job["arrival_time"]
                for job in jobs
                if remaining[job["job_id"]] > 0
                and job["arrival_time"] > current_time
            )
            continue

        # SRTF:
        # shortest remaining time first
        # tie -> earlier arrival
        # tie -> lower job_id
        job = min(
            ready,
            key=lambda x: (
                remaining[x["job_id"]],
                x["arrival_time"],
                x["job_id"]
            )
        )

        job_id = job["job_id"]

        if job_id not in start_times:
            start_times[job_id] = current_time

        # Run for exactly one tick
        remaining[job_id] -= 1
        current_time += 1

        if remaining[job_id] == 0:
            completion_times[job_id] = current_time
            completed_count += 1

    results = []

    for job in jobs:
        job_id = job["job_id"]

        completion_time = completion_times[job_id]

        turnaround_time = (
            completion_time - job["arrival_time"]
        )

        waiting_time = (
            turnaround_time - job["burst_time"]
        )

        results.append({
            "job_id": job_id,
            "arrival_time": job["arrival_time"],
            "burst_time": job["burst_time"],
            "start_time": start_times[job_id],
            "completion_time": completion_time,
            "waiting_time": waiting_time,
            "turnaround_time": turnaround_time
        })

    return results


def print_results(results):
    print("\nSRTF Scheduling")
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
    results = srtf(JOBS)
    print_results(results)
