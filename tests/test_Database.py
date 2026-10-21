import sqlite3

import pytest

from Database import Database


@pytest.fixture
def database(tmp_path):
    db = Database(filename=str(tmp_path / "fixture.db"), isOnline=False)
    assert db.conn is not None
    yield db
    db.close_database()


def test_sensor_data_is_committed_and_queryable(database):
    database.insert_day_graph_table(21, 420, 12, 900, 42)
    rows, empty, valid = database.query_table("DayGraphTable")
    assert valid and not empty
    assert rows[0][1:] == (21, 420, 12, 900, 42)
    assert database.query_table("DayGraphTable", row=1, column=3)[0] == 12


def test_invalid_table_and_row_do_not_execute_sql(database):
    assert database.query_table("DayGraphTable WHERE 1=1 --") == (None, None, False)
    assert database.query_table("missing") == (None, None, False)
    assert database.query_table("DayGraphTable", row=50000) == (None, None, False)


def test_close_releases_sqlite_connection(tmp_path):
    db = Database(filename=str(tmp_path / "close.db"), isOnline=False)
    connection = db.conn
    db.close_database()
    with pytest.raises(sqlite3.ProgrammingError):
        connection.execute("SELECT 1")
