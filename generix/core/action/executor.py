"""

"""
from generix.core.action.id import Action
from generix.core.settings.registry import settings_reg


def execute(action, **kwargs):
    """
    Executes action called by name.
    :param action: Command name.
    :param kwargs: additional kwargs parameters.
    :return: depends on what type of Command was executed. Usually commands
             do not return anything, but some of them do.
    """
    item = settings_reg.find_option_by_key(action, 'cls')()
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
