PAGE_SIZE = 1024

PAGE_TABLE = {
    0: 5,
    1: 2,
    2: 9,
    3: 1
}

# {segment: (base, limit)}
SEGMENT_TABLE = {
    0: (1000, 400),
    1: (2200, 300),
    2: (500, 150)
}


def translate_paged_address(logical_address):
    page_number = logical_address // PAGE_SIZE
    offset = logical_address % PAGE_SIZE

    # Page not present in page table
    if page_number not in PAGE_TABLE:
        return {
            "logical_address": logical_address,
            "page": page_number,
            "offset": offset,
            "status": "PAGE FAULT"
        }

    frame_number = PAGE_TABLE[page_number]

    physical_address = (
        frame_number * PAGE_SIZE + offset
    )

    return {
        "logical_address": logical_address,
        "page": page_number,
        "offset": offset,
        "frame": frame_number,
        "physical_address": physical_address,
        "status": "OK"
    }


def translate_segmented_address(segment, offset):
    if segment not in SEGMENT_TABLE:
        return {
            "segment": segment,
            "offset": offset,
            "status": "SEGMENTATION FAULT"
        }

    base, limit = SEGMENT_TABLE[segment]

    # Offset must be strictly less than limit
    if offset >= limit:
        return {
            "segment": segment,
            "offset": offset,
            "base": base,
            "limit": limit,
            "status": "SEGMENTATION FAULT"
        }

    physical_address = base + offset

    return {
        "segment": segment,
        "offset": offset,
        "base": base,
        "limit": limit,
        "physical_address": physical_address,
        "status": "OK"
    }


def print_paging_results():
    print("PAGING ADDRESS TRANSLATION")
    print("=" * 60)

    addresses = [260, 1500, 3000, 5000]

    for address in addresses:
        result = translate_paged_address(address)

        if result["status"] == "OK":
            print(
                f"Logical Address {address}: "
                f"Page={result['page']}, "
                f"Offset={result['offset']}, "
                f"Frame={result['frame']}, "
                f"Physical Address={result['physical_address']}"
            )
        else:
            print(
                f"Logical Address {address}: "
                f"Page={result['page']}, "
                f"Offset={result['offset']} -> "
                f"PAGE FAULT"
            )


def print_segmentation_results():
    print("\nSEGMENTATION ADDRESS TRANSLATION")
    print("=" * 60)

    addresses = [
        (0, 150),
        (2, 100),
        (1, 350)
    ]

    for segment, offset in addresses:
        result = translate_segmented_address(
            segment,
            offset
        )

        if result["status"] == "OK":
            print(
                f"Logical Address ({segment}, {offset}): "
                f"Base={result['base']}, "
                f"Limit={result['limit']}, "
                f"Physical Address={result['physical_address']}"
            )
        else:
            print(
                f"Logical Address ({segment}, {offset}): "
                f"Base={result['base']}, "
                f"Limit={result['limit']} -> "
                f"SEGMENTATION FAULT"
            )


if __name__ == "__main__":
    print_paging_results()
    print_segmentation_results()
