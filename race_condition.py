import threading
import time
import random


# Shared Zone-B compute-credit counter
counter = 100


def subtract_credits():
    global counter

    # Read-modify-write operation
    value = counter
    time.sleep(random.uniform(0.001, 0.01))
    counter = value - 40


def add_credits():
    global counter

    # Read-modify-write operation
    value = counter
    time.sleep(random.uniform(0.001, 0.01))
    counter = value + 25


def run_race_condition():
    global counter

    counter = 100

    thread1 = threading.Thread(
        target=subtract_credits
    )

    thread2 = threading.Thread(
        target=add_credits
    )

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    return counter


print("Race Condition Demonstration")
print("=" * 45)

print("Correct arithmetic result: 85")
print()

wrong_count = 0

for run in range(1, 6):

    result = run_race_condition()

    print(f"Run {run}: Final counter = {result}")

    if result != 85:
        wrong_count += 1

print()

if wrong_count > 0:
    print("Race condition observed.")
    print(f"Runs different from 85: {wrong_count}")
else:
    print(
        "This particular execution produced 85 on all runs. "
        "The program still contains an unsynchronized "
        "read-modify-write race."
    )
