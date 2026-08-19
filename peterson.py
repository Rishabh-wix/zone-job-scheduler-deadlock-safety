import threading
import time
import random


# Peterson's Algorithm shared variables
flag = [False, False]
turn = 0

counter = 100


def enter_critical_section(process_id):
    global turn

    other = 1 - process_id

    flag[process_id] = True
    turn = other

    while flag[other] and turn == other:
        time.sleep(0)


def exit_critical_section(process_id):
    flag[process_id] = False


def subtract_credits():
    global counter

    enter_critical_section(0)

    try:
        value = counter
        time.sleep(random.uniform(0.001, 0.01))
        counter = value - 40
    finally:
        exit_critical_section(0)


def add_credits():
    global counter

    enter_critical_section(1)

    try:
        value = counter
        time.sleep(random.uniform(0.001, 0.01))
        counter = value + 25
    finally:
        exit_critical_section(1)


def run_peterson():
    global counter, flag, turn

    counter = 100
    flag = [False, False]
    turn = 0

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


print("Peterson's Algorithm Demonstration")
print("=" * 50)

print("Correct arithmetic result: 85")
print()

all_correct = True

for run in range(1, 6):

    result = run_peterson()

    print(f"Run {run}: Final counter = {result}")

    if result != 85:
        all_correct = False

print()

if all_correct:
    print("Peterson's Algorithm protected version is correct.")
    print("All 5 runs produced exactly 85.")
else:
    print("ERROR: A run did not produce 85.")
