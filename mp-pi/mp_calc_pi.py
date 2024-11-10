import asyncio
import contextlib
import dataclasses as dtcs
import functools as ft
import itertools as it
import math
import sys
import typing as t
from concurrent import futures

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


@dtcs.dataclass
class ConcurrentAsyncTaskController:
    executor: futures.Executor
    loop: asyncio.AbstractEventLoop

    async def request(self, f: t.Callable[[], T]) -> T:
        try:
            return await self.loop.run_in_executor(self.executor, f)
        except RuntimeError as e:
            print("Runtime error, either not in event loop or closed executor")
            raise e


@contextlib.contextmanager
def processContext(max_workers: int):
    loop = asyncio.get_running_loop()
    with futures.ProcessPoolExecutor(max_workers=max_workers) as p:
        yield ConcurrentAsyncTaskController(p, loop)


async def main():
    N_MULTIPROC = int(sys.argv[1])
    n_iter = 25200000
    N = 50

    ls = it.repeat(n_iter, N)
    fs = map(ft.partial, it.repeat(calcPi), ls)

    with processContext(N_MULTIPROC) as ctrl:
        async with asyncio.TaskGroup() as tg:
            coros = map(ctrl.request, fs)
            list(map(tg.create_task, coros))


if __name__ == "__main__":
    asyncio.run(main())
