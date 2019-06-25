"""
A module for ORM wrapper classes of database models.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Sequence
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Experiment(Base):
    """
    ORM for 'Simulation' model in the database.
    """
    __tablename__ = 'experiment'
    # PK (with autoincrementing value)
    id = Column(Integer, Sequence('experiment_id_seq', start=1, increment=1), primary_key=True)
    # Linking with FK: experiment_id
    simulation_rel = relationship('Simulation')
    # Experiment name
    name = Column(String(32))
    # Experiment date
    date = Column(DateTime, default=func.now())

    def __init__(self, name):
        self.name = name

class Simulation(Base):
    """
    ORM for 'Simulation' model in the database.
    """
    __tablename__ = 'simulation'
    # PK (with autoincrementing value)
    id = Column(Integer, Sequence('simulation_id_seq', start=1, increment=1), primary_key=True)
    # FK: 'Experiment' --< 'Simulation'
    experiment_id = Column(Integer, ForeignKey('experiment.id'))
    # The number of iterations that was done over
    iterations = Column(Integer)

    def __init__(self, experiment_id, iterations):
        self.experiment_id = experiment_id
        self.iterations = iterations