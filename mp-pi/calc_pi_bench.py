import itertools as it
import math
import sys
import time
import typing as t

T = t.TypeVar("T")
P = t.ParamSpec("P")


def calcPi(iterations: int) -> float:
    # Refer to: https://codedrome.substack.com/p/estimating-pi-in-python
    numerator = 0.0
    pi = 1.0

    for _ in range(1, iterations + 1):
        numerator = math.sqrt(2.0 + numerator)
        pi *= numerator / 2.0

    return (1.0 / pi) * 2.0


def timedCalcPi(n: int) -> float:
    """
    Return time to calc given the number of iterations
    """
    t0 = time.time_ns()
    calcPi(n)
    tf = time.time_ns()
    return tf - t0

N_REPEAT = 1
def avgTimeCalcPi(n: int) -> float:
    return sum(map(timedCalcPi, it.repeat(n, N_REPEAT))) / N_REPEAT

def optimize():
    desiredTimeNs = float(sys.argv[1])
    iters = int(sys.argv[2])
    errMarg = float(sys.argv[3])
    iterChange = int(sys.argv[4])

    while True:
        if iters < 0:
            raise Exception("iters cannot be negative")
        procTime = avgTimeCalcPi(iters)
        timeDiff = procTime - desiredTimeNs
        if abs(timeDiff) < errMarg:
            print(iters)
            return
        if timeDiff > 0:
            iters -= iterChange
        if timeDiff < 0:
            iters += iterChange
        print(f"tried {iters} got {procTime}, diff {timeDiff}")

def main():
    iters = int(sys.argv[1])
    calcPi(iters)

if __name__ == "__main__":
    main()
