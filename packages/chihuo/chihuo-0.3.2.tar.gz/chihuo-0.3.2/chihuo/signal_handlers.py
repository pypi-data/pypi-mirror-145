from typing import Iterable, Optional, Tuple, Dict, Any
import logging
import asyncio
import functools
import signal
import copy

from .common import TaskType, TaskId
from .loop import ChihuoLoop

logger = logging.getLogger(__name__)

IS_ON_TERM = False
IS_ON_INT = False


async def cancel_all_running_tasks() -> None:
    """Cancel all running tasks, then send these tasks back to backend"""

    while True:
        # Cancel all running async tasks in the loop
        tasks = [t for t in asyncio.all_tasks() if t.get_name() != TaskType.Final.value]

        logger.info("all tasks number: %s", len(tasks))

        task_loop = [t for t in tasks if t.get_name() == TaskType.TaskLoop.value]
        needed_cancel = [t for t in tasks if t.get_name() != TaskType.TaskLoop.value]

        for task in needed_cancel:
            task.cancel()

        if len(needed_cancel) == 0:
            # Finally, cancel the `ChihuoLoop._task_loop`
            for task in task_loop:
                task.cancel()
            break

        await asyncio.sleep(1)


async def send_back_running_tasks(
    factory_and_tasks: Iterable[Tuple[ChihuoLoop, Dict[TaskId, Any]]]
) -> None:
    logger.info("[send back task]: START")

    for factory, tasks in factory_and_tasks:
        for task_id, task in tasks.items():
            logger.info(
                "[Send back task]: factory: %s, task: %s",
                factory.__class__.__name__,
                (task_id, task),
            )
            await factory.add_task((task_id, task))

    logger.info("[send back task]: END")


async def teardown(
    factories: Iterable[ChihuoLoop], loop: asyncio.AbstractEventLoop
) -> None:
    logger.info("[teardown]: START")

    # Send back running tasks
    running_tasks = [
        (factory, copy.deepcopy(factory._running_tasks)) for factory in factories
    ]
    await send_back_running_tasks(running_tasks)

    # Spawn the final task
    await cancel_all_running_tasks()

    loop.stop()

    logger.info("[teardown]: END")


def handle_stop(
    signum,
    frame,
    factories: Iterable[ChihuoLoop] = [],
    loop: Optional[asyncio.AbstractEventLoop] = None,
) -> None:
    """The handler of INT and TERM signals

    First, we set all factories to be stoped at next event loop.
    Then, we cancel all running tasks which will be sent back to backend.
    """

    assert loop, "The Event Loop can not be None"

    logger.info("[handle_stop]: signal: %s", signum)

    global IS_ON_INT
    if IS_ON_TERM or IS_ON_INT:
        return

    # Stop the factory task loop
    for factory in factories:
        factory.stop = True

    loop.create_task(teardown(factories, loop), name=TaskType.Final.value)

    IS_ON_INT = True


def set_signal_handlers(
    factories: Iterable[ChihuoLoop], loop: asyncio.AbstractEventLoop
) -> None:
    """Set signal handlers for `factories`"""

    signal.signal(
        signal.SIGTERM,
        functools.partial(handle_stop, factories=factories, loop=loop),
    )
    signal.signal(
        signal.SIGINT,
        functools.partial(handle_stop, factories=factories, loop=loop),
    )
