"""Post-install smoke test for a built wheel.

Run this against an installed dead-band to confirm the *compiled* path is the
one in use. CI runs it inside a container with no compiler, which is the
property that matters: shipping wheels is only worth anything if a user with no
toolchain gets the fast implementation.

    python scripts/smoke_wheel.py

Exits non-zero with a readable message if the compiled extension is missing or
the filter returns the wrong result. Kept as a file rather than an inline
`python -c` in the workflow, because quoting a multi-line script through YAML
and then through `docker run` is how the first version of this check broke.
"""

import datetime as dt
import sys

import dead_band

EXPECTED = [
    (0.0, dt.datetime(2020, 1, 1, 0, 0)),
    (50.0, dt.datetime(2020, 1, 1, 0, 0, 2)),
]

SERIES = [
    (0.0, dt.datetime(2020, 1, 1, 0, 0, 0)),
    # Inside the deadband, and inside max_time_interval: dropped.
    (0.5, dt.datetime(2020, 1, 1, 0, 0, 1)),
    # Outside the deadband: kept.
    (50.0, dt.datetime(2020, 1, 1, 0, 0, 2)),
]


def main() -> int:
    if not dead_band.CYTHON_AVAILABLE:
        print(
            "FAIL: dead_band.CYTHON_AVAILABLE is False -- the installed "
            "distribution has no compiled extension, so this is not a working "
            "binary wheel.",
            file=sys.stderr,
        )
        return 1

    result = dead_band.apply_deadband(SERIES, 10, 30)
    if result != EXPECTED:
        print(f"FAIL: expected {EXPECTED!r}, got {result!r}", file=sys.stderr)
        return 1

    print(f"filtered: {result}")
    print("OK: compiled extension active, no toolchain required")
    return 0


if __name__ == "__main__":
    sys.exit(main())
