"""
Provide a simple awaitable for a mutable sequence of scheduled future events. Instantiate, register
events and then await. Once the first one is returned, re-await to get the next, and so on.
"""

import asyncio
from datetime import datetime, timedelta


class Pending:
    "awaitable for a mutable chronologically ordered sequence of scheduled future events"

    def __init__(self):
        "set up internal variables for managing expected events"
        self._expected = {}
        self._next = None

    def _update_next(self):
        "determine the next pending event that gets returned"
        if self._expected:
            self._next = min(self._expected.items(), key=lambda i:i[1])
        else:
            self._next = None

    def expect(self, event, seconds_from_now):
        "register an expected future event"
        expected = datetime.now() + timedelta(seconds=seconds_from_now)
        if event not in self._expected:
            self._expected[event] = expected
        else:
            raise KeyError("already anticipating eventsday scenario '%s'", event)
        self._update_next()

    def cancel(self, event):
        "cancel a given expected future event"
        del self._expected[event]
        self._update_next()

    def postpone(self, event, delay_by_seconds):
        "postpone expected future event by expecting it afresh after a given delay"
        self._expected[event] = datetime.now() + timedelta(seconds=delay_by_seconds)
        self._update_next()

    def __len__(self):
        "return the number of expected events that are pending"
        return len(self._expected)

    def __await__(self):
        "make this awaitable"
        return self

    def __next__(self):
        "this is returned as the itemake this an iterator"
        event, expected = self._next
        if datetime.now() > expected:
            del self._expected[event]
            self._update_next()
            raise StopIteration(event)
        return
