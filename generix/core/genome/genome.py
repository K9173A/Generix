"""
A module for a cell genome which represents cell logic - the way it behaves on
the board. Genome is comprised of n commands like "turn left", "eat" and etc.
"""
import random


class Genome:
    """
    Genome holds a list of commands for a CellId object.
    """
    def __init__(self, actions):
        """
        Constructs Genome object.
        :param actions: list of actions.
        """
        self._actions = actions

    @classmethod
    def generate(cls, n, allowed_actions):
        """
        Constructs Genome object with random genome.
        :param n: amount of actions to generate.
        :param allowed_actions: list of actions which will be the source.
        :return: Genome instance.
        """
        return Genome(generate_genome(n, allowed_actions))

    def __len__(self):
        """
        Gets genome size.
        :return: genome size.
        """
        return len(self._actions)

    def __str__(self):
        """
        Represents Genome as a comma-separated string of action numbers.
        :return: string of commands.
        """
        return ','.join(str(action) for action in self._actions)

    def get_cmd(self, index):
        """
        Gets name of the action from the list.
        :param index: index of action.
        :return: action name.
        """
        return self._actions[index]

    def mutate(self, n=1):
        """
        Changes n actions in genome.
        :param n: amount of actions to change.
        :return: None.
        """
        new_cmds = [random.randint(0, len(self) - 1) for _ in range(n)]
        for i in range(len(new_cmds) - 1):
            self._actions[i] = new_cmds[i]


def generate_genome(n, allowed_actions):
    """
    Generates a list of actions, picking randomly from allowed_actions list.
    :param n: amount of actions to generate.
    :param allowed_actions: list of actions which will be the source.
    :return: list of n actions.
    """
    return [random.choice(allowed_actions) for _ in range(n)]

