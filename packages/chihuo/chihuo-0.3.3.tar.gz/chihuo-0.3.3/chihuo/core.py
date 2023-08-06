import logging
import asyncio

from .loop import ChihuoLoop
from .signal_handlers import set_signal_handlers

logger = logging.getLogger(__name__)


async def _event_alive():
    """Keep event loop alive

    Event loop could be dead if all tasks are keeping.
    The task keeps event loop to listen for events. Because it be woke up periodically.
    """

    while True:
        await asyncio.sleep(1)


def _instantiate_factories(*classes_or_instances):
    """Instantiate factories"""

    factories = []
    for obj in classes_or_instances:
        if isinstance(obj, ChihuoLoop):
            if obj.NAME is None:
                raise TypeError("factory.NAME must be given")
            factories.append(obj)
        else:
            if type(obj) is not type:
                raise TypeError("factory must be a class or instance of ChihuoLoop")
            if not issubclass(obj, ChihuoLoop):
                raise TypeError(
                    "factory must be a subclass of ChihuoLoop or instance of ChihuoLoop"
                )
            if obj.NAME is None:
                raise TypeError("factory.NAME must be given")

            factories.append(obj())
    return factories


def run(*classes_or_instances):
    """Instantiate factories and run them"""

    if not classes_or_instances:
        logger.error("No provide factory class or instance")

    assert classes_or_instances, "No provide factory class or instance"

    loop = asyncio.get_event_loop()

    # Keep event loop alive
    loop.create_task(_event_alive())

    factories = _instantiate_factories(*classes_or_instances)
    logger.info("Find factories: %s", [factory.NAME for factory in factories])

    set_signal_handlers(factories, loop)

    # Run factories
    for factory in factories:
        factory._run_()

    loop.run_forever()
