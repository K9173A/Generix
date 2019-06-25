"""

"""
class IterationStatistics:
    def __init__(self):
        self._cells_counter = {}

    @property
    def cells_counter(self):
        return self._cells_counter

    def update(self, cell_id):
        """
        Updates cell counter.
        :param cell_id: CellId enum (id).
        :return: None.
        """
        try:
            self._cells_counter[cell_id] += 1
        except KeyError:
            self._cells_counter[cell_id] = 1
