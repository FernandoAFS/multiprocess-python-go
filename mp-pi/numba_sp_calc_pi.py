
import math
import sys
import typing as t
import numba
import time

T = t.TypeVar("T")
P = t.ParamSpec("P")

@numba.njit
def calcPi(iterations: int) -> float:
    # Refer to: https://codedrome.substack.com/p/estimating-pi-in-python
    numerator = 0.0
    pi = 1.0

    for _ in range(1, iterations + 1):
        numerator = math.sqrt(2.0 + numerator)
        pi *= numerator / 2.0

    return (1.0 / pi) * 2.0


def main():
    t0 = time.perf_counter()
    iters = int(sys.argv[1])
    res = calcPi(iters)
    dt = time.perf_counter() - t0
    print(f"time: {dt}")
    print(res)

if __name__ == "__main__":
    main()
