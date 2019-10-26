"""

"""
import json
import random

from generix.core.settings.settings import GENOME_FILE_PATH, LOAD_GENOME
from generix.core.settings.encoder import SettingsEncoder


class GenomeRegistry:
    """
    {
        <CellId>: {
            <Genome>: <amount_of_cells>,
            ...
        }
    }
    """
    def __init__(self, path, default_settings):
        """
        Constructs SettingsRegistry instance.
        :param path: path to the settings file.
        :param default_settings: default settings dictionary.
        """
        self._path = path
        self._settings = default_settings

    def load(self):
        """
        Loads last saved data from settings.json.
        :return: None.
        """
        with open(self._path, mode='r', encoding='utf-8') as f:
            self._settings = json.load(f)

    def save(self):
        """
        Saves current settings to the file, rewriting it.
        :return: None.
        """
        with open(self._path, mode='w', encoding='utf-8') as f:
            json.dump(self._settings, f, cls=SettingsEncoder)

    def create(self, cell_id, genome):
        """
        Adds new item to the storage.
        :param cell_id: CellId value.
        :param genome: genome commands list.
        :return: None.
        """
        cell_genomes = self._settings[cell_id]
        if genome in cell_genomes.keys():
            cell_genomes[genome] += 1
        else:
            cell_genomes[genome] = 1

    def pick_genome(self, cell_id):
        """
        Takes genome from storage.
        :param cell_id: CellId value.
        :return: genome.
        """
        try:
            cell_data = self._settings[cell_id]
        except KeyError:
            return None

        # Picks genome randomly
        genome = random.choice(cell_data.keys())

        cell_data[genome] -= 1
        if cell_data[genome] <= 0:
            del cell_data[genome]

        return genome


genome_reg = GenomeRegistry(GENOME_FILE_PATH, {})

if LOAD_GENOME:
    genome_reg.load()


