import time
from typing import NoReturn, Optional

import pandas as pd

from lumipy.client import Client
from lumipy.common.string_utils import indent_str

from luminesce.exceptions import ApiException


class QueryJob:
    """Class representing a query that has been submitted to Luminesce.

    """

    def __init__(self, ex_id: str, client: Client):
        """__init__ method of the Job class

        Args:
            ex_id (str): the execution ID of the query.
            client (Client): a lumipy client instance that can be used to manage the query.
        """
        self.ex_id = ex_id
        self._client = client
        self._progress_lines = []
        self._row_count = -1
        self._status = None
        self._state = None
        self.get_status()

    def delete(self) -> NoReturn:
        """Delete the query. Query can be running or finished. If running the query will be cancelled
        if it's running the query result will be deleted if it still exists.

        """
        print("Deleting query... ", end='')
        self._client.delete_query(self.ex_id)
        print("💥")

    def get_status(self) -> str:
        """Get the status of the query in Luminesce

        Returns:
            str: string containing the query status value.
        """
        status = self._client.get_status(self.ex_id)
        lines = status['progress'].split('\n')
        new_lines = [line for line in lines if line not in self._progress_lines]
        self._progress_lines += new_lines
        self._row_count = status['row_count']
        self._status = status['status']
        self._state = status['state']

        return status['status']

    def interactive_monitor(self) -> NoReturn:
        """Start interactive monitoring mode. Interactive monitoring mode will give a live printout of the
        query status and allow you to cancel the query using a keyboard interupt.

        """
        print("Query launched! 🚀")
        print('[Use ctrl+c or the stop button in jupyter to cancel]', end='\n\n')

        try:
            self.live_status()
        except KeyboardInterrupt as ki:
            self.delete()
            raise ki
        except Exception as e:
            raise e

    def get_progress(self) -> str:
        """Get progress log of the query.

        Returns:
            str: the progress log string.
        """
        return '\n'.join(self._progress_lines)

    def get_result(self, page_size: Optional[int] = 100000, verbose: Optional[bool] = True) -> pd.DataFrame:
        """Get the result of a successful query back as a Pandas DataFrame.

        Args:
            page_size Optional[int]: page size for query fetch calls (default = 100000).

        Returns:
            DataFrame: pandas dataframe containing the query result.
        """
        return self._client.get_result(self.ex_id, page_size, verbose=verbose)

    def live_status(self) -> NoReturn:
        """Start a monitoring session that prints out the live progress of the query. Refreshes with a period of one
        second. A keyboard interrupt during this method will not delete the query.

        """
        print(f"Progress of Execution ID: {self.ex_id}")

        status = self.get_status()

        start_i = 0
        while status == 'WaitingForActivation':

            if start_i != len(self._progress_lines):
                new_progress_lines = '\n'.join(self._progress_lines[start_i:])
                print(indent_str(new_progress_lines))

            start_i = len(self._progress_lines)
            status = self.get_status()
            time.sleep(0.5)

        print(indent_str('\n'.join(self._progress_lines[start_i:])))

        if status == 'RanToCompletion':
            print(f"\nQuery finished successfully! 🛰🪐")
        else:
            info_str = f"Status: {status}\nExecution ID: {self.ex_id}"
            print(f"\nQuery was unsuccessful... 💥\n{indent_str(info_str, n=4)}")
