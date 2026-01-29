from __future__ import annotations
from typing import List, Dict, Callable, Type, TYPE_CHECKING, Union

from allocation.domain import events

if TYPE_CHECKING:
    from . import unit_of_work

from . import handlers


def handle(
    event: events.Event,
    uow: unit_of_work.AbstractUnitOfWork,
) -> List:
    results = []
    queue = [event]
    while queue:
        event = queue.pop(0)
        for handler in HANDLERS[type(event)]:
            results.append(handler(event, uow=uow))
            queue.extend(uow.collect_new_events())
    return results


HANDLERS = {
    events.BatchCreated: [handlers.add_batch],
    events.BatchQuantityChanged: [handlers.change_batch_quantity],
    events.AllocationRequired: [handlers.allocate],
    events.OutOfStock: [handlers.send_out_of_stock_notification],
}  # type: Dict[Type[events.Event], List[Callable]]
