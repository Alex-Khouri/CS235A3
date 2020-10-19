import pytest

from getflix.repository.memory_repo import MemoryRepo
from getflix.domainmodel.actor import Actor
from getflix.domainmodel.director import Director
from getflix.domainmodel.genre import Genre
from getflix.domainmodel.movie import Movie
from getflix.domainmodel.review import Review
from getflix.domainmodel.user import User
from getflix.domainmodel.watchlist import Watchlist

@pytest.fixture
def repo():
    return MemoryRepo('tests/data/Data1000Movies.csv')

@pytest.fixture
def user():
    return User("Bob", "Password1")


def test_repo_init(repo):
    assert len(repo.movies) == 1000
    assert len(repo.directors) == 644
    assert len(repo.actors) == 1985
    assert len(repo.genres) == 20

def test_repo_remove_user(repo, user):
    repo.add_user(user)
    repo.add_user(user)
    assert len(repo.users) == 1
    repo.remove_user(user)
    assert len(repo.users) == 0

def test_repo_get_user(repo, user):
    repo.add_user(user)
    assert repo.get_user("bob") is user

def test_repo_get_movie(repo):
    assert str(repo.get_movie(" inception ")) == "<Movie Inception, 2010>"

def test_repo_get_watchlist(repo, user):
    repo.add_user(user)
    assert repo.get_watchlist("bob") is user.watchlist