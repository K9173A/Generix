"""

"""


class GameStatistics:
    def __init__(self):
        self._iterations = []
        self._curr_iteration_stats = IterationStatistics()

    def get_last_iteration(self):
        return self._iterations[len(self._iterations) - 1]

    def update_counter(self, cell):
        """
        Updates counter of cells.
        :param cell: cell to be counted.
        :return: None.
        """
        self._curr_iteration_stats.update(cell.settings('id'))

    def complete_iteration(self):
        """
        Saves current iteration statistics and starts a new one.
        :return: None.
        """
        self._iterations.append(self._curr_iteration_stats)
        self._curr_iteration_stats = IterationStatistics()


class IterationStatistics:
    def __init__(self):
        self._cells_counter = {}

    @property
    def cells_counter(self):
        return self._cells_counter

    def update(self, cell_name):
        """
        Updates cell counter.
        :param cell_name: Cell enum (id).
        :return: None.
        """
        try:
            self._cells_counter[cell_name] += 1
        except KeyError:
            self._cells_counter[cell_name] = 1
