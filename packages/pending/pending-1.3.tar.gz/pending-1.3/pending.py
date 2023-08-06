"""
Provide a simple awaitable for a mutable sequence of scheduled future events. Instantiate, register
events and then await. Once the first one is returned, re-await to get the next, and so on.
"""

import asyncio
from typing import Tuple, Any
from datetime import datetime, timedelta
from collections.abc import Awaitable
from collections import namedtuple


Schedule = namedtuple('Schedule', ['delay', 'expected'])


class Pending(Awaitable):
    "awaitable for a mutable chronologically ordered sequence of scheduled future events"

    def __init__(self):
        "set up internal variables for managing expected events"
        self._scheduled = {}
        # (event, (number of seconds from scheduling time, the calculated future timestamp))
        self._next: Tuple[Any,Schedule] | None = None

    def _update_next(self):
        "determine the next pending event that gets returned"
        try:
            self._next = min(self._scheduled.items(), key=lambda i:i[1].expected)
        except ValueError: # when empty
            self._next = None

    def schedule(self, event:Any, seconds:int):
        "schedule an expected future event for # of seconds from now"
        expected = datetime.now() + timedelta(seconds=seconds)
        try:
            self._scheduled[event] = Schedule(seconds, expected)
        except KeyError:
            raise Exception("'%s' already scheduled", event)
        else:
            self._update_next()

    def cancel(self, event:Any):
        "cancel a given expected future event"
        try:
            del self._scheduled[event]
        except KeyError:
            raise Exception("no such event '%s' scheduled", event)
        else:
            self._update_next()

    def reschedule(self, event):
        "convenience to reschedule expected event forward in time the same # of seconds"
        try:
            seconds = self._scheduled[event].delay
        except KeyError:
            raise Exception("no such event '%s' scheduled", event)
        else:
            expected = datetime.now() + timedelta(seconds=seconds)
            self._scheduled[event] = Schedule(seconds, expected)
            self._update_next()

    def __len__(self):
        "return the number of expected events that are pending"
        return len(self._scheduled)

    def __getitem__(self, event):
        return self._scheduled[event]

    def __await__(self):
        "make this awaitable"
        return self

    def __next__(self):
        "make this an iterator"
        if self._next:
            event, (_, expected) = self._next
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