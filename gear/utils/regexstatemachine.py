import re
import collections
from enum import Enum

import transitions


# regex state mapping
RegexCommand = collections.namedtuple("RegexState", "regex command")


class RegexState:
    """
    regex state machine state
    """
    def __init__(
        self,
        regex: str,
        trigger: str = None,
        src_state: Enum = None,
        dst_state: Enum = None,
        after: str = None
    ):
        self.regex = re.compile(regex)
        self.trigger = trigger
        self.src_state = src_state
        self.dst_state = dst_state
        self.after = after

    def search(self, text: str):
        res = self.regex.search(text)
        if res:
            # result found
            return res.groupdict()

        return None

    def __str__(self):
        return (
            f"<RegexState(regex='{self.regex}', trigger='{self.trigger}', "
            f"src_state={self.src_state}, dst_state={self.dst_state}', "
            f"after='{self.after}')>"
        )


class RegexStateMachine:
    """
    helper class to ease the use of regexes that are linked
    to states
    """
    def __init__(
        self,
        regex_states: list,
        states: list,
        pre_regex: str = None,
        initial="initial"
    ):
        self.regex_states = regex_states
        self.pre_regex = re.compile(pre_regex)

        # derive transisionts from regex states
        trans = [
            {
                "trigger": rs.trigger,
                "source": rs.src_state,
                "dest": rs.dst_state,
                "after": rs.after
            }
            for rs in self.regex_states
            if rs.dst_state is not None
        ]

        # prepare state machine
        self.m = transitions.Machine(
            model=self,
            states=states,
            transitions=trans,
            initial=initial
        )

        # simple counter to count matches
        self.c = collections.Counter()

    def search(
        self,
        ts: int,
        text: str
    ):
        if (self.pre_regex is not None) and not self.pre_regex.search(text):
            # if pre regex is set, but not matching the given pre regex
            # leave method to avoid checking of actual regexes from the list
            return

        for rs in self.regex_states:
            res = rs.search(text)
            if res is not None:
                if rs.trigger is not None:
                    # call transition command for regex
                    getattr(self, rs.trigger)()

                # simply count the match
                self.c[text] += 1

                return res, text

        return None
