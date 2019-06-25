"""
A module for a CellFactory.
"""
import random

from generix.core.genome.genome import Genome
from generix.core.cell.id import CellId
from generix.core.settings.registry import settings_reg


class CellFactory:
    """
    Creates instances of different cells classes.
    """
    def __init__(self):
        """
        Constructs CellFactory object.
        """
        self._choices = {}
        self._max = 0
        for cell_id, cell_data in settings_reg.find('cell').items():
            if not isinstance(cell_data, dict):
                continue
            current = settings_reg.search(cell_data, 'chance')
            if current is None:
                continue
            self._choices[(self._max, self._max + current)] = cell_id
            self._max += current

    def create_cell(self, cell_id):
        """
        Creates cell instance of a specific type.
        :param cell_id: CellId value.
        :return: cell instance.
        """
        cell_data = settings_reg.find(cell_id)

        # TODO: загрузка генома из файла
        genome = Genome.generate(
            settings_reg.search(cell_data, 'genome_max_len'),
            settings_reg.search(cell_data, 'allowed_actions')
        )

        cls = settings_reg.search(cell_data, 'cls')
        if cell_id == CellId.HUNTER_CELL:
            return cls(genome, settings_reg.search(cell_data, 'at_start'))
        else:
            return cls(genome)

    def create_random_cell(self):
        """
        Gets random cell class.
        :return: cell class.
        """
        choice = random.randint(0, self._max - 1)
        for (left_bound, right_bound), cell_name in self._choices.items():
            if left_bound <= choice < right_bound:
                return self.create_cell(cell_name)
        return None


factory = CellFactory()
