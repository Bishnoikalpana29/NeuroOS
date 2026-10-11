import subprocess
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

BANKER_EXE = PROJECT_ROOT / "core" / "deadlock" / "banker_cli.exe"


def check_safety(allocation, maximum, available):
    """
    Call the existing C++ Banker's Algorithm.

    Returns the Need matrix, safety status, and safe sequence.
    Raises ValueError for invalid resource-allocation data.
    """

    if not BANKER_EXE.exists():
        raise FileNotFoundError(
            f"Banker's Algorithm executable not found: {BANKER_EXE}"
        )

    if not allocation or len(allocation) != len(maximum):
        raise ValueError("Allocation and Maximum must have the same number of processes.")

    if not available:
        raise ValueError("At least one resource type is required.")

    resource_count = len(available)

    for matrix_name, matrix in [
        ("Allocation", allocation),
        ("Maximum", maximum),
    ]:
        for row in matrix:
            if len(row) != resource_count:
                raise ValueError(
                    f"Every {matrix_name} row must match the number of resources."
                )

    if any(
        not isinstance(value, int) or isinstance(value, bool) or value < 0
        for row in allocation + maximum
        for value in row
    ):
        raise ValueError("Allocation and Maximum must contain non-negative integers.")

    if any(
        not isinstance(value, int) or isinstance(value, bool) or value < 0
        for value in available
    ):
        raise ValueError("Available resources must be non-negative integers.")

    for i, (alloc_row, max_row) in enumerate(zip(allocation, maximum)):
        for j, (alloc, maximum_value) in enumerate(zip(alloc_row, max_row)):
            if maximum_value < alloc:
                raise ValueError(
                    f"Maximum cannot be less than Allocation "
                    f"(process P{i}, resource R{j})."
                )

    process_count = len(allocation)

    input_lines = [f"{process_count} {resource_count}"]

    input_lines.extend(" ".join(map(str, row)) for row in allocation)
    input_lines.extend(" ".join(map(str, row)) for row in maximum)
    input_lines.append(" ".join(map(str, available)))

    result = subprocess.run(
        [str(BANKER_EXE)],
        input="\n".join(input_lines) + "\n",
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            result.stdout.strip()
            or result.stderr.strip()
            or "Banker's Algorithm failed."
        )

    lines = result.stdout.strip().splitlines()

    try:
        need_start = lines.index("NEED")
        status_index = next(
            i for i, line in enumerate(lines) if line in ("SAFE", "UNSAFE")
        )

        need = [
            [int(value) for value in lines[i].split()]
            for i in range(need_start + 1, status_index)
        ]

        status = lines[status_index]
        sequence = ""

        if status == "SAFE":
            sequence_line = next(
                line for line in lines[status_index + 1:]
                if line.startswith("SEQUENCE ")
            )
            sequence = sequence_line.removeprefix("SEQUENCE ")

        return {
            "need": need,
            "safe": status == "SAFE",
            "safe_sequence": sequence,
        }

    except (ValueError, StopIteration) as error:
        raise RuntimeError(
            f"Could not interpret the C++ result:\n{result.stdout}"
        ) from error