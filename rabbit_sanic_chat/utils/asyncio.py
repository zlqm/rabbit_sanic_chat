import asyncio


async def await_many_dispatch(callables):
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(_callable()) for _callable in callables]
    try:
        while True:
            await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            for i, task in enumerate(tasks):
                if task.done():
                    result = task.result()
                    tasks[i] = asyncio.ensure_future(callables[i]())
    finally:
        for task in tasks:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
