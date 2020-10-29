import pytest

from getflix.repository.database_repo import DatabaseRepo
from getflix.domainmodel.actor import Actor
from getflix.domainmodel.director import Director
from getflix.domainmodel.genre import Genre
from getflix.domainmodel.movie import Movie
from getflix.domainmodel.review import Review
from getflix.domainmodel.user import User
from getflix.domainmodel.watchlist import Watchlist

import getflix.repository.database_repo as database_repo
from getflix.repository.orm import metadata, map_model_to_tables

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

@pytest.fixture
def database_repo():
    data_path = 'getflix/datafiles/Data1000Movies.csv'
    database_path = 'sqlite:///getflix/repository/getflix_database.db'
    database_engine = create_engine(database_path, connect_args={"check_same_thread": False}, poolclass=NullPool, echo=True)
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
    repo = DatabaseRepo(session_factory)
    if len(database_engine.table_names()) == 0:
        clear_mappers()
        metadata.create_all(database_engine)
        for table in reversed(metadata.sorted_tables):
            database_engine.execute(table.delete())
        map_model_to_tables()
        repo.populate(database_engine, data_path)  # Do this before mapping model to tables?
    else:
        map_model_to_tables()
        repo.load(database_engine)  # Do this before mapping model to tables?
    return (repo, database_engine)


@pytest.fixture
def user():
    return User("Bob", "Password1")


def test_repo_init(database_repo):
    repo = database_repo[0]
    database_engine = database_repo[1]
    assert len(repo.movies) == 1000
    assert len(repo.directors) == 644
    assert len(repo.actors) == 1985
    assert len(repo.genres) == 20

def test_repo_remove_user(database_repo, user):
    repo = database_repo[0]
    database_engine = database_repo[1]
    repo.add_user(user, database_engine)
    repo.add_user(user, database_engine)
    assert len(repo.users) == 1
    repo.remove_user(user, database_engine)
    assert len(repo.users) == 0

def test_repo_get_user(database_repo, user):
    repo = database_repo[0]
    database_engine = database_repo[1]
    repo.add_user(user, database_engine)
    assert repo.get_user("bob") is user

def test_repo_get_movie(database_repo):
    repo = database_repo[0]
    database_engine = database_repo[1]
    assert str(repo.get_movie(" inception ")) == "<Movie Inception, 2010>"

def test_repo_get_watchlist(database_repo, user):
    repo = database_repo[0]
    database_engine = database_repo[1]
    repo.add_user(user, database_engine)
    assert repo.get_watchlist("bob") is user.watchlist