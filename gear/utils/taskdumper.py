import datetime
import json
from typing import Union, TextIO
from pathlib import Path

from gear.utils.utils import ensure_path, get_user


class TaskDumper:
    """
    class to dump the output of a task to a file
    using a header with meta information and the data
    as payload
    """
    def __init__(
        self,
        input_filename: Path = None,
        ts: datetime.datetime = None,
        user: str = None,
        payload = {}
    ):
        # header information
        self.input_filename = input_filename
        self.ts = ts
        self.user = user

        # payload
        self.payload = payload

    @property
    def input_filename(self) -> Path:
        """
        get input filename

        :return: input filename
        :rtype: Path
        """
        return self._input_filename

    @input_filename.setter
    def input_filename(self, value: Union[str, Path]):
        """
        set the input filename

        :param value: input filename
        :type value: Path
        """
        if value is None:
            self._input_filename = None

        else:
            self._input_filename = ensure_path(value)

    @property
    def ts(self) -> datetime.datetime:
        """
        get timestamp

        :return: timestamp
        :rtype: datetime.datetime
        """
        return self._ts

    @ts.setter
    def ts(self, value: Union[datetime.datetime, str]):
        """
        set the timestamp, or if None set current time

        :param value: timestamp
        :type value: datetime.datetime
        """
        assert (value is None) or isinstance(value, (datetime.datetime, str))

        if isinstance(value, str):
            # convert string to datetime
            value = datetime.datetime.strptime(
                value,
                "%Y-%m-%dT%H:%M:%S.%f"
            )

        self._ts = value or datetime.datetime.now()

    @property
    def user(self) -> str:
        """
        get user

        :return: user
        :rtype: str
        """
        return self._user

    @user.setter
    def user(self, value: str):
        """
        set the user or if None is set, set current user

        :param value: timestamp
        :type value: str
        """
        assert (value is None) or isinstance(value, str)

        self._user = value or get_user()

    @property
    def header(self) -> dict:
        """
        returns header dictionary

        :return: header dictionary
        :rtype: dict
        """
        return {
            "ts": self.ts.isoformat(),
            "input_filename":  self.input_filename.as_posix(),
            "user": self.user
        }

    def dump(self, f: TextIO):
        """
        dump header and payload as dictionary to the given file object

        :param f: file object
        :type f: TextIO
        """
        d = {
            "header": self.header,
            "payload": self.payload
        }

        # dump the dictionary
        json.dump(d, f)

    @staticmethod
    def from_file(f: TextIO) -> "TaskDumper":
        """
        create task dump instance based on data read from
        given file object

        :param f: file object
        :type f: TextIO
        :return: task dump instance based on given file object
        :rtype: TaskDumper
        """
        # load data from given file object
        d = json.load(f)

        # create new task dump instance based on obtained dictionary data
        return TaskDumper(
            input_filename=d["header"]["input_filename"],
            ts=d["header"]["ts"],
            user=d["header"]["user"],
            payload=d["payload"],
        )
