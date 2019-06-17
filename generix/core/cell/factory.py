"""
A module for a CellFactory.
"""
import random

from generix.core.cell.genome import Genome, generate_genome
from generix.core.cell.id import Cell


def register_cell(cls):
    """
    Registers cells for simulation.
    :param cls: cell class.
    :return: cell class.
    """
    factory.create(cls.__settings__['id'].value, cls.__settings__['id'], cls)
    return cls


class CellFactoryItem:
    def __init__(self, item_id, item_type, item_class):
        self.id = item_id
        self.type = item_type
        self.cls = item_class


class CellFactory:
    """
    Creates instances of different cells classes.
    """
    def __init__(self):
        """
        Constructs CellFactory object.
        """
        self._storage = []
        self._choices = {}
        self._max = 0

    @property
    def storage(self):
        return self._storage

    def create(self, item_id, item_type, item_class):
        """
        Creates new item and appends cell class to the dict of random cell choices.
        :param item_id: item id.
        :param item_type: item type (enum value).
        :param item_class: item class.
        :return: None.
        """
        self._storage.append(CellFactoryItem(item_id, item_type, item_class))
        self._storage = sorted(self._storage, key=lambda item: item.id)
        if 'chance' in item_class.__settings__.keys():
            current = item_class.__settings__['chance']
            self._choices[(self._max, self._max + current)] = item_class.__settings__['id']
            self._max += current

    def find(self, attr_key, attr_val):
        """
        Find item by attribute and value.
        :param attr_key: attribute name.
        :param attr_val: attribute value.
        :return: CellFactoryItem instance if found, None otherwise.
        """
        for item in self._storage:
            value = getattr(item, attr_key)
            if value and value == attr_val:
                return item
        return None

    def create_cell(self, name):
        """
        Creates cell instance of a specific type.
        :param name: value of Cell enum.
        :return: cell instance.
        """
        cell_cls = self.find('type', name).cls

        # TODO: загрузка генома из файла
        genome = Genome.generate(
            cell_cls.__settings__['genome_max_len'],
            cell_cls.__settings__['allowed_actions']
        )

        if name == Cell.HUNTER_CELL:
            return cell_cls(genome, cell_cls.__settings__['hp']['at_start'])
        else:
            return cell_cls(genome)

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
