"""

"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from generix.core.settings.settings import DB_FILE_PATH
from generix.core.data.model import Experiment, Simulation, Base


# Creates engine for SQLite database.
engine = create_engine('sqlite:///{}'.format(DB_FILE_PATH))
# Creates all the defined tables (ORMs) and stores the information in metadata.
Base.metadata.create_all(engine)
# Creates session maker object which manages sessions.
make_session = sessionmaker(bind=engine)


class SQLNotFoundException(Exception):
    def __init__(self, object_name):
        self._object_name = object_name

    def __str__(self):
        return 'Object {} was not found!'.format(self._object_name)


class Database:
    """
    A wrapper for comfortable interaction with the database.
    """
    def __init__(self):
        """
        Constructs Database wrapper instance.
        """
        self._session = make_session()

    def __del__(self):
        self._session.close()

    def create_experiment(self, name):
        experiment = Experiment(name)
        self._session.add(experiment)
        self._commit()

    def create_simulation(self, experiment_name, iterations):
        experiment = self.find_experiment_by_name(experiment_name)
        if experiment is None:
            raise SQLNotFoundException(experiment)
        simulation = Simulation(experiment.id, iterations)
        self._session.add(simulation)
        self._commit()

    def find_experiment_by_id(self, id):
        return self._session.query(Experiment).filter(Experiment.id == id).first()

    def find_experiment_by_name(self, name):
        return self._session.query(Experiment).filter(Experiment.name == name).first()

    def find_experiment_simulations(self, id):
        return self._session.query(Simulation).filter(Simulation.experiment_id == id)

    def count_experiment_simulations(self, id):
        return self.find_experiment_simulations(id).count()

    def _commit(self):
        try:
            self._session.commit()
        except IntegrityError:
            self._session.rollback()
