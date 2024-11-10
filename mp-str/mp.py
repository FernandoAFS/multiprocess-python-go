import asyncio
import contextlib
import dataclasses as dtcs
import functools as ft
import itertools as it
import sys
import typing as t
from concurrent import futures
import time

T = t.TypeVar("T")
P = t.ParamSpec("P")


def count_l(in_list: str) -> int:
    return len(in_list)


def gen_l_str(n: int) -> str:
    t0 = time.perf_counter()
    s = "".join(it.repeat("1", n))
    dt = time.perf_counter() - t0
    print(dt)
    return s


@dtcs.dataclass
class ConcurrentAsyncTaskController:
    executor: futures.Executor
    loop: asyncio.AbstractEventLoop

    async def request(self, f: t.Callable[[], T]) -> T:
        try:
            return await self.loop.run_in_executor(
                self.executor,
                ft.partial(f),
            )
        except RuntimeError as e:
            print("Runtime error, either not in event loop or closed executor")
            raise e


@contextlib.contextmanager
def processContext(max_workers: int):
    loop = asyncio.get_running_loop()
    with futures.ProcessPoolExecutor(max_workers=max_workers) as p:
        yield ConcurrentAsyncTaskController(p, loop)


N = 50
str_l = 10**8

async def main_mp():
    N_MULTIPROC = int(sys.argv[1])

    s = gen_l_str(str_l)
    fs = map(ft.partial, it.repeat(count_l, N), it.repeat(s))

    with processContext(N_MULTIPROC) as ctrl:
        async with asyncio.TaskGroup() as tg:
            coros = map(ctrl.request, fs)
            list(map(tg.create_task, coros))


def main_sp():
    s = gen_l_str(str_l)
    for _ in range(N):
        count_l(s)


if __name__ == "__main__":
    asyncio.run(main_mp())
    # main_sp()
