from sqlalchemy import (
	Table, MetaData, Column, Integer, String, Date, DateTime, ForeignKey
)
from sqlalchemy.orm import mapper, relationship

metadata = MetaData()

# Lists of objects are stored as CSV strings of primary key IDs
users = Table(
	'users', metadata,
	Column('id', Integer, primary_key=True, autoincrement=True),
	Column('username', String(255), unique=True, nullable=False),
	Column('password', String(255), nullable=False),
	Column('watched', String(1024), nullable=False),  # CSV string of IDs
	Column('reviews', String(1024), nullable=False),  # CSV string of IDs
	Column('watchlist', ForeignKey('watchlists.id')),
	Column('timewatching', Integer, nullable=False)
)
reviews = Table(
	'reviews', metadata,
	Column('id', Integer, primary_key=True, autoincrement=True),
	Column('user_id', ForeignKey('users.id')),
	Column('movie_id', ForeignKey('movies.id')),
	Column('text', String(1024), nullable=False),
	Column('rating', Integer, nullable=False),
	Column('timestamp', DateTime, nullable=False),
	Column('date', String(1024), nullable=False),
)
movies = Table(
	'movies', metadata,
	Column('id', Integer, primary_key=True, autoincrement=True),
	Column('title', String(255), nullable=False),
	Column('year', Integer, nullable=False),
	Column('description', String(1024), nullable=False),
	Column('director_id', ForeignKey('directors.id')),
	Column('csvActors', String(1024), nullable=False),  # CSV string of codes
	Column('csvGenres', String(1024), nullable=False),  # CSV string of codes
	Column('runtime', Integer, nullable=False),
	Column('reviews', String(1024), nullable=False),  # CSV string of IDs
	Column('review_count', Integer, nullable=False),
	Column('rating', Integer, nullable=False),
	Column('votes', Integer, nullable=False),
	Column('code', String(255), nullable=False)
)
actors = Table(
	'actors', metadata,
	Column('id', Integer, primary_key=True, autoincrement=True),
	Column('name', String(255), nullable=False),
	Column('csvMovies', String(1024), nullable=False),  # CSV string of codes
	Column('csvColleagues', String(1024), nullable=False),  # CSV string of codes
	Column('code', String(255), nullable=False)
)
directors = Table(
	'directors', metadata,
	Column('id', Integer, primary_key=True, autoincrement=True),
	Column('name', String(255), nullable=False),
	Column('csvMovies', String(1024), nullable=False),  # CSV string of codes
	Column('code', String(255), nullable=False)
)
genres = Table(
	'genres', metadata,
	Column('id', Integer, primary_key=True, autoincrement=True),
	Column('name', String(255), nullable=False),
	Column('csvMovies', String(1024), nullable=False),  # CSV string of codes
	Column('code', String(255), nullable=False)
)
watchlists = Table(
	'watchlists', metadata,
	Column('id', Integer, primary_key=True, autoincrement=True),
	Column('movies', String(1024), nullable=False)  # CSV string of IDs
)


def map_model_to_tables():
	mapper(User, users, properties={
		'user_username': users.c.username,
		'user_password': users.c.password,
		'user_watched': users.c.watched,
		'user_reviews': users.c.reviews,
		'user_watchlist': relationship(Watchlist),
		'user_timewatching': users.c.timewatching
	})
	mapper(Review, reviews, properties={
		'review_user': relationship(User),
		'review_movie': relationship(Movie),
		'review_text': reviews.c.text,
		'review_rating': reviews.c.rating,
		'review_timestamp': reviews.c.timestamp,
		'review_date': reviews.c.date
	})
	mapper(Movie, movies, properties={
		'movie_title': movies.c.title,
		'movie_year': movies.c.year,
		'movie_description': movies.c.description,
		'movie_director': relationship(Director, backref='director_movies'),
		'movie_actors': movies.c.actors,
		'movie_genres': movies.c.genres,
		'movie_runtime_minutes': movies.c.runtime,
		'movie_reviews': movies.c.reviews,
		'movie_review_count': movies.c.review_count,
		'movie_rating': movies.c.rating,
		'movie_votes': movies.c.votes,
		'movie_code': movies.c.code
	})
	mapper(Actor, actors, properties={
		'actor_name': actors.c.name,
		'actor_movies': actors.c.movies,
		'actor_colleagues': actors.c.colleagues,
		'actor_code': actors.c.code
	})
	mapper(Director, directors, properties={
		'director_name': directors.c.name,
		'director_movies': directors.c.movies,
		'director_code': directors.c.code
	})
	mapper(Genre, genres, properties={
		'genre_name': genres.c.name,
		'genre_movies': genres.c.movies,
		'genre_code': genres.c.code
	})
	mapper(Watchlist, watchlists, properties={
		'watchlist_movie_list': watchlists.c.movies
	})


if __name__ == "__main__":
	from getflix.domainmodel.actor import Actor
	from getflix.domainmodel.director import Director
	from getflix.domainmodel.genre import Genre
	from getflix.domainmodel.movie import Movie
	from getflix.domainmodel.review import Review
	from getflix.domainmodel.user import User
	from getflix.domainmodel.watchlist import Watchlist