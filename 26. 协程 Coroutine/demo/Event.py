import asyncio
from async_delay import async_delay
from gather import gather


# 以下是简易版的实现
class Event:
    def __init__(self):
        self._fut = None

    def set(self):
        if self._fut:
            self._fut.set_result(None)

    async def wait(self):
        loop = asyncio.get_running_loop()
        self._fut = loop.create_future()
        await self._fut


async def test():
    event = Event()

    async def waiter():  # 定义一个异步函数名为waiter
        print("waiter: 开始等待")  # 打印开始等待的信息
        await event.wait()  # 等待事件被触发，此处使用await挂起当前协程直到事件发生
        print("waiter: 被唤醒")  # 事件被触发后打印被唤醒的信息

    async def setter():
        print("setter: 1秒后设置事件")
        await async_delay(1)
        event.set()
        print("setter: 事件已设置")

    await gather(waiter(), setter())


if __name__ == "__main__":
    asyncio.run(test())

    """ 
    waiter: 开始等待
    setter: 1秒后设置事件
    setter: 事件已设置
    waiter: 被唤醒 
    """
