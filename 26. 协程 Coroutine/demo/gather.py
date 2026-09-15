import asyncio
from async_delay import async_delay
from typing import Coroutine


def gather(*aws: Coroutine) -> asyncio.Future:
    loop = asyncio.get_running_loop()
    tasks: list[asyncio.Task[Any]] = [asyncio.create_task(aw) for aw in aws]
    future: asyncio.Future[list[Any]] = loop.create_future()
    results: list[Any] = [None] * len(tasks)  # 预分配,按位置存放结果
    remaining: int = len(tasks)

    def on_done(task: asyncio.Task[Any], index: int) -> None:
        nonlocal remaining
        if future.done():
            return  # 已经有异常了,不再处理
        try:
            results[index] = task.result()
        except Exception as exc:
            future.set_exception(exc)
            return
        remaining -= 1
        if remaining == 0:
            future.set_result(results)

    for index, task in enumerate(tasks):
        task.add_done_callback(lambda t, i=index: on_done(t, i))

    return future


async def coro(name: str, duration: int):
    await async_delay(duration)
    return f"{name} 完成"


async def main():
    results = await gather(
        coro("A", 2),
        coro("B", 1),
        coro("C", 3),
    )
    print(results)  # 预期: ['A 完成', 'B 完成', 'C 完成']


asyncio.run(main())
