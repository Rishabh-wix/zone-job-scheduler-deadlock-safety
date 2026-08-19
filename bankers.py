AVAILABLE = [3, 3, 2]

MAX_NEED = {
    "P0": [7, 5, 3],
    "P1": [3, 2, 2],
    "P2": [9, 0, 2],
    "P3": [2, 2, 2]
}

ALLOCATION = {
    "P0": [0, 1, 0],
    "P1": [2, 0, 0],
    "P2": [3, 0, 2],
    "P3": [2, 1, 1]
}


def calculate_need():
    need = {}

    for process in MAX_NEED:
        need[process] = [
            MAX_NEED[process][i] - ALLOCATION[process][i]
            for i in range(3)
        ]

    return need


def is_safe(available, allocation, need):
    work = available[:]
    finish = {
        process: False
        for process in allocation
    }

    safe_sequence = []

    while len(safe_sequence) < len(allocation):

        found = False

        for process in allocation:

            if finish[process]:
                continue

            # Check Need <= Work
            if all(
                need[process][i] <= work[i]
                for i in range(3)
            ):

                # Process can finish
                for i in range(3):
                    work[i] += allocation[process][i]

                finish[process] = True
                safe_sequence.append(process)
                found = True

        if not found:
            break

    safe = all(finish.values())

    return safe, safe_sequence


def request_resources(
    process,
    request,
    available,
    allocation,
    need
):

    print(f"\nRequest from {process}: {request}")

    # Step 1: Request <= Need
    if any(
        request[i] > need[process][i]
        for i in range(3)
    ):
        print("DENIED: Request exceeds process Need.")
        return False

    # Step 2: Request <= Available
    if any(
        request[i] > available[i]
        for i in range(3)
    ):
        print("DENIED: Request exceeds Available resources.")
        return False

    # Temporarily allocate resources
    new_available = available[:]

    new_allocation = {
        p: allocation[p][:]
        for p in allocation
    }

    new_need = {
        p: need[p][:]
        for p in need
    }

    for i in range(3):
        new_available[i] -= request[i]
        new_allocation[process][i] += request[i]
        new_need[process][i] -= request[i]

    # Check resulting state
    safe, sequence = is_safe(
        new_available,
        new_allocation,
        new_need
    )

    if safe:
        print("GRANTED")
        print("Resulting state is SAFE.")
        print("Safe sequence:", " -> ".join(sequence))
        return True

    print("DENIED")
    print("Granting the request would leave the system UNSAFE.")
    return False


def print_need_matrix(need):

    print("\nNeed Matrix")
    print("-" * 45)

    print(
        f"{'Process':<10}"
        f"{'R0':<8}"
        f"{'R1':<8}"
        f"{'R2':<8}"
    )

    for process in need:

        print(
            f"{process:<10}"
            f"{need[process][0]:<8}"
            f"{need[process][1]:<8}"
            f"{need[process][2]:<8}"
        )


if __name__ == "__main__":

    # ------------------------------------------------
    # Calculate Need Matrix
    # ------------------------------------------------

    NEED = calculate_need()

    print_need_matrix(NEED)

    # ------------------------------------------------
    # Initial Safety Check
    # ------------------------------------------------

    safe, sequence = is_safe(
        AVAILABLE,
        ALLOCATION,
        NEED
    )

    print("\nInitial System State")
    print("-" * 45)

    if safe:
        print("System is SAFE.")
        print("Safe sequence:", " -> ".join(sequence))
    else:
        print("System is UNSAFE.")

    # ------------------------------------------------
    # Request A
    # P1 requests [1, 0, 2]
    # ------------------------------------------------

    request_resources(
        "P1",
        [1, 0, 2],
        AVAILABLE,
        ALLOCATION,
        NEED
    )

    # ------------------------------------------------
    # Request B
    # P0 requests [2, 0, 2]
    # ------------------------------------------------

    request_resources(
        "P0",
        [2, 0, 2],
        AVAILABLE,
        ALLOCATION,
        NEED
    )
