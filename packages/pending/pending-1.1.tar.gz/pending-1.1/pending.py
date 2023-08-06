"""
Provide a simple awaitable for a mutable sequence of scheduled future events. Instantiate, register
events and then await. Once the first one is returned, re-await to get the next, and so on.
"""

import asyncio
from datetime import datetime, timedelta
from collections.abc import Awaitable


class Pending(Awaitable):
    "awaitable for a mutable chronologically ordered sequence of scheduled future events"

    def __init__(self):
        "set up internal variables for managing expected events"
        self._scheduled = {}
        self._next = None

    def _update_next(self):
        "determine the next pending event that gets returned"
        if self._scheduled:
            self._next = min(self._scheduled.items(), key=lambda i:i[1])
        else:
            self._next = None

    def schedule(self, event, seconds_from_now):
        "schedule an expected future event"
        expected = datetime.now() + timedelta(seconds=seconds_from_now)
        if event not in self._scheduled:
            self._scheduled[event] = expected
        else:
            raise KeyError("already anticipating eventsday scenario '%s'", event)
        self._update_next()

    def cancel(self, event):
        "cancel a given expected future event"
        del self._scheduled[event]
        self._update_next()

    def postpone(self, event, delay_by_seconds):
        "postpone expected future event by expecting it afresh after a given delay"
        self._scheduled[event] = datetime.now() + timedelta(seconds=delay_by_seconds)
        self._update_next()

    def __len__(self):
        "return the number of expected events that are pending"
        return len(self._scheduled)

    def __await__(self):
        "make this awaitable"
        return self

    def __next__(self):
        "this is returned as the itemake this an iterator"
        event, expected = self._next
        if datetime.now() > expected:
            del self._scheduled[event]
            self._update_next()
            raise StopIteration(event)
        return

    async def wait(self):
        "convenience coro for when awaitable is not enough, such as task creation"
        return await self

    def task(self):
        "convenience method for when a task is needed"
        return asyncio.create_task(self.wait(), name="pending")