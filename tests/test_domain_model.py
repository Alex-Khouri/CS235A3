import pytest

from getflix.domainmodel.actor import Actor
from getflix.domainmodel.director import Director
from getflix.domainmodel.genre import Genre
from getflix.domainmodel.movie import Movie
from getflix.domainmodel.review import Review
from getflix.domainmodel.user import User
from getflix.domainmodel.watchlist import Watchlist

@pytest.fixture
def user():
    return User("Bob", "Password1")

@pytest.fixture
def watchlist():
	watchlist = Watchlist()
	watchlist.add_movie(Movie("Moana", 2016))
	watchlist.add_movie(Movie("Ice Age", 2002))
	watchlist.add_movie(Movie("Guardians of the Galaxy", 2012))
	return watchlist


# Actor tests
def test_actor_add_actor_colleague():
	actor1 = Actor("John Doe")
	actor2 = Actor("Jane Doe")
	actor1.add_actor_colleague(actor2)
	assert len(actor1.colleagues) == 1
	assert len(actor2.colleagues) == 1

def test_actor_remove_movie():
	actor = Actor("John Doe")
	movie = Movie("Imception", 2011)
	actor.add_movie(movie)
	assert len(actor.movies) == 1
	actor.remove_movie(movie)
	assert len(actor.movies) == 0

def test_actor_check_if_this_actor_worked_with():
	actor1 = Actor("John Doe")
	actor2 = Actor("Jane Doe")
	actor1.add_actor_colleague(actor2)
	assert actor1.check_if_this_actor_worked_with(actor2) == True


# Director tests
def test_director_remove_movie():
	director = Director("Christopher Molan")
	movie = Movie("Imception", 2011)
	director.add_movie(movie)
	assert len(director.movies) == 1
	director.remove_movie(movie)
	assert len(director.movies) == 0


# Genre tests
def test_genre_remove_movie():
	genre = Genre("Weird")
	movie = Movie("Imception", 2011)
	genre.add_movie(movie)
	assert len(genre.movies) == 1
	genre.remove_movie(movie)
	assert len(genre.movies) == 0


# Movie tests
def test_movie_remove_actor():
	movie = Movie("Imception", 2011)
	actor = Actor("John Doe")
	movie.add_actor(actor)
	assert len(movie.actors) == 1
	movie.remove_actor(actor)
	assert len(movie.actors) == 0

def test_movie_remove_genre():
	movie = Movie("Imception", 2011)
	genre = Genre("Weird")
	movie.add_actor(genre)
	assert len(movie.actors) == 1
	movie.remove_actor(genre)
	assert len(movie.actors) == 0


# Review tests
def test_review_init(user):
	review = Review(user, Movie("Imception", 2011), "It was pretty weird", 6)
	assert str(review.user) == "<User bob>"
	assert str(review.movie) == "<Movie Imception, 2011>"
	assert str(review.text) == "It was pretty weird"


# User tests
def test_user_watch_movie(user):
	movie = Movie("Imception", 2011)
	movie.runtime_minutes = 120
	user.watch_movie(movie)
	assert movie in user.watched_movies
	assert user.time_spent_watching_movies_minutes == movie.runtime_minutes

def test_user_remove_review(user):
	review = Review(user, Movie("Imception", 2011), "It was pretty weird", 6)
	user.add_review(review)
	assert len(user.reviews) == 1
	user.remove_review(review)
	assert len(user.reviews) == 0


# Watchlist tests
def test_watchlist_remove_movie(watchlist):
	watchlist.remove_movie(Movie("Moana", 2016))
	watchlist.remove_movie(Movie("Guardians of the Galaxy", 2012))
	test_output = ""
	for movie in watchlist:
		test_output += str(movie) + "\n"
	assert test_output.strip() == "<Movie Ice Age, 2002>"
	assert str(watchlist) == "[<Movie Ice Age, 2002>]"

def test_watchlist_select_movie_to_watch(watchlist):
	assert str(watchlist.select_movie_to_watch(0)) == "<Movie Moana, 2016>"
	assert str(watchlist.select_movie_to_watch(1)) == "<Movie Ice Age, 2002>"
	assert str(watchlist.select_movie_to_watch(2)) == "<Movie Guardians of the Galaxy, 2012>"
	assert str(watchlist.select_movie_to_watch(3)) == "None"
	assert str(watchlist.select_movie_to_watch(-1)) == "None"

def test_watchlist_size(watchlist):
	assert watchlist.size() == 3
	watchlist.add_movie(Movie("Fight Club", 1999))
	watchlist.add_movie(Movie("Se7en", 1995))
	watchlist.add_movie(Movie("Memento", 2001))
	assert watchlist.size() == 6
	watchlist.remove_movie(Movie("Fight Club", 1999))
	watchlist.remove_movie(Movie("Se7en", 1995))
	assert watchlist.size() == 4

def test_watchlist_first_movie_in_watchlist(watchlist):
	assert str(watchlist.first_movie_in_watchlist()) == "<Movie Moana, 2016>"
	watchlist.remove_movie(Movie("Moana", 2016))
	assert str(watchlist.first_movie_in_watchlist()) == "<Movie Ice Age, 2002>"
	watchlist.remove_movie(Movie("Ice Age", 2002))
	assert str(watchlist.first_movie_in_watchlist()) == "<Movie Guardians of the Galaxy, 2012>"
	watchlist.remove_movie(Movie("Guardians of the Galaxy", 2012))
	assert str(watchlist.first_movie_in_watchlist()) == "None"