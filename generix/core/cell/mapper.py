import sqlite3

from generix.core.statistics import GameStatistics


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class SimulationMapper:
    # Simulation - это симуляция или эпоха. Эпоха завершается, когда
    # достигается поставленное условие. Например, остаётся не более 5 выживших клеток.
    # Нас в данном случае интересует количество итераций (ходов), которые прошли за эпоху,
    # чтобы в дальнейшем вывести данные в качестве графика и смотреть за эволюцией
    # выживаемости клеток. Чем более совершенными будут геномы клеток, тем более живучими
    # они будут, соответственно количество итераций будет расти с эволюционным процессом
    def __init__(self, connection):
        self._connection = connection
        self._cursor = connection.cursor()
        self._cursor.execute("CREATE TABLE IF NOT EXISTS Simulation (id INTEGER, iterations INTEGER)")

    def __del__(self):
        self._connection.commit()
        self._connection.close()

    def find(self, id):
        query = f"SELECT id, iterations FROM Simulation WHERE id={id}"
        result = self._cursor.execute(query).fetchone()
        if not result:
            raise RecordNotFoundException(f'Record with id={id} was not found!')
        return GameStatistics(*result)

    def insert(self, simulation):
        query = f"INSERT INTO Simulation (id, iterations) VALUES " \
                f"('{simulation.id}', '{simulation.iterations}')"
        self._cursor.execute(query)
        try:
            self._connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, simulation):
        query = f"UPDATE Simulation SET iterations='{simulation.iterations}'" \
                f"WHERE id={simulation.id}"
        self._cursor.execute(query)
        try:
            self._connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, id):
        query = f"DELETE FROM Simulation WHERE id={id}"
        self._cursor.execute(query)
        try :
            self._connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)

    def find_max_id(self):
        query = f"SELECT max(id) FROM Simulation"
        result = self._cursor.execute(query).fetchone()
        return result[0] if result[0] else 0

    def select_all(self):
        self._cursor.execute("SELECT * FROM Simulation")
        return self._cursor.fetchall()


connection = sqlite3.connect(database='generix.sqlite')
simulation_mapper = SimulationMapper(connection)
