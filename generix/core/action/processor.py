"""
A module for a CommandProcessor class.
"""
from generix.core.action.id import Action


def register_cmd(cls):
    """
    Registers actions for simulation.
    :param cls: action class.
    :return: action class.
    """
    cmd_enum = cls.__settings__['id']
    processor.create(cmd_enum.value, cmd_enum, cls)
    return cls


class CommandProcessorItem:
    def __init__(self, item_id, item_type, item_object):
        self.id = item_id
        self.type = item_type
        self.object = item_object

class CommandProcessor:
    """
    CommandProcessor stores all possible commands (genes) of cells.
    """
    def __init__(self):
        """
        Constructs CommandProcessor instance.
        """
        self._storage = []

    def create(self, item_id, item_type, item_class):
        """
        Creates action item in the storage.
        :param item_id: action id (int).
        :param item_type: action type (enum).
        :param item_class: action class.
        :return: None.
        """
        self._storage.append(CommandProcessorItem(item_id, item_type, item_class()))
        self._storage = sorted(self._storage, key=lambda item: item.id)

    def find(self, attr_key, attr_val):
        """
        Gets item by attribute and value.
        :param attr_key: attribute key name.
        :param attr_val: attribute value.
        :return:
        """
        for item in self._storage:
            value = getattr(item, attr_key)
            if value is None:
                continue
            if value == attr_val:
                return item
        return None

    def execute(self, action, **kwargs):
        """
        Executes action called by name.
        :param action: Command name.
        :param kwargs: additional kwargs parameters.
        :return: depends on what type of Command was executed. Usually commands
                 do not return anything, but some of them do.
        """
        item = self.find('id', action.value).object
        if action == Action.EAT:
            item.execute(
                kwargs['old_board'], kwargs['new_board'], kwargs['point'], kwargs['cell']
            )

        elif action == Action.STAY:
            item.execute(
                kwargs['board'], kwargs['point'], kwargs['cell']
            )

        elif action == Action.LOOK:
            # Look action returns an 'id' of type of neighbor cell
            return item.execute(
                kwargs['board'], kwargs['point'], kwargs['cell_types']
            )

        elif action == Action.TURN:
            item.execute(
                kwargs['cell'], kwargs['angle']
            )

        elif action == Action.MOVE:
            item.execute(
                kwargs['old_board'], kwargs['new_board'], kwargs['point'], kwargs['cell'],
                kwargs['curr_cell_types'], kwargs['next_cell_types']
            )

processor = CommandProcessor()
