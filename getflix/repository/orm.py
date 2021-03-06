from sqlalchemy import (
	Table, MetaData, Column, Integer, String, Date, DateTime, ForeignKey
)
from sqlalchemy.orm import mapper, relationship

from getflix.domainmodel.actor import Actor
from getflix.domainmodel.director import Director
from getflix.domainmodel.genre import Genre
from getflix.domainmodel.movie import Movie
from getflix.domainmodel.review import Review
from getflix.domainmodel.user import User
from getflix.domainmodel.watchlist import Watchlist


metadata = MetaData()

# Lists of objects are stored as CSV strings of domain model codes attributes (names contain 'code')
users = Table(
	'users', metadata,
	Column('id', Integer, primary_key=True, autoincrement=True),
	Column('username', String(255), unique=True, nullable=False),
	Column('password', String(255), nullable=False),
	Column('watched_codes', String(1024), nullable=False),
	Column('review_codes', String(1024), nullable=False),
	Column('timewatching', Integer, nullable=False),
	Column('watchlist_code', String(255), nullable=False),
	Column('code', String(1024), nullable=False)
)
reviews = Table(
	'reviews', metadata,
	Column('id', Integer, primary_key=True, autoincrement=True),
	Column('user_code', String(255), nullable=False),
	Column('movie_code', String(255), nullable=False),
	Column('text', String(1024), nullable=False),
	Column('rating', Integer, nullable=False),
	Column('timestamp', String(255), nullable=False),
	Column('date', String(255), nullable=False),
	Column('code', String(255), nullable=False)
)
movies = Table(
	'movies', metadata,
	Column('id', Integer, primary_key=True, autoincrement=True),
	Column('title', String(255), nullable=False),
	Column('year', Integer, nullable=False),
	Column('description', String(1024), nullable=False),
	Column('director_code', String(255), nullable=False),
	Column('actor_codes', String(1024), nullable=False),
	Column('genre_codes', String(1024), nullable=False),
	Column('runtime_minutes', Integer, nullable=False),
	Column('review_codes', String(1024), nullable=False),
	Column('review_count', Integer, nullable=False),
	Column('rating', String(255), nullable=False),
	Column('votes', Integer, nullable=False),
	Column('code', String(255), nullable=False)
)
actors = Table(
	'actors', metadata,
	Column('id', Integer, primary_key=True, autoincrement=True),
	Column('name', String(255), nullable=False),
	Column('movie_codes', String(1024), nullable=False),
	Column('colleague_codes', String(1024), nullable=False),
	Column('code', String(255), nullable=False)
)
directors = Table(
	'directors', metadata,
	Column('id', Integer, primary_key=True, autoincrement=True),
	Column('name', String(255), nullable=False),
	Column('movie_codes', String(1024), nullable=False),
	Column('code', String(255), nullable=False)
)
genres = Table(
	'genres', metadata,
	Column('id', Integer, primary_key=True, autoincrement=True),
	Column('name', String(255), nullable=False),
	Column('movie_codes', String(1024), nullable=False),
	Column('code', String(255), nullable=False)
)
watchlists = Table(
	'watchlists', metadata,
	Column('id', Integer, primary_key=True, autoincrement=True),
	Column('user_code', String(255), nullable=False),
	Column('movie_codes', String(1024), nullable=False),
	Column('code', String(255), nullable=False)
)


def map_model_to_tables():
	mapper(User, users, properties={
		'user_username': users.c.username,
		'user_password': users.c.password,
		'user_watched_codes': users.c.watched_codes,
		'user_review_codes': users.c.review_codes,
		'user_timewatching': users.c.timewatching,
		'user_watchlist_code': users.c.watchlist_code,
		'user_code': users.c.code
	})
	mapper(Review, reviews, properties={
		'review_user_code': reviews.c.user_code,
		'review_movie_code': reviews.c.movie_code,
		'review_text': reviews.c.text,
		'review_rating': reviews.c.rating,
		'review_timestamp': reviews.c.timestamp,
		'review_date': reviews.c.date,
		'review_code': reviews.c.code
	})
	mapper(Movie, movies, properties={
		'movie_title': movies.c.title,
		'movie_year': movies.c.year,
		'movie_description': movies.c.description,
		'movie_director_code': movies.c.director_code,
		'movie_actor_codes': movies.c.actor_codes,
		'movie_genre_codes': movies.c.genre_codes,
		'movie_runtime_minutes': movies.c.runtime_minutes,
		'movie_review_codes': movies.c.review_codes,
		'movie_review_count': movies.c.review_count,
		'movie_rating': movies.c.rating,
		'movie_votes': movies.c.votes,
		'movie_code': movies.c.code
	})
	mapper(Actor, actors, properties={
		'actor_name': actors.c.name,
		'actor_movie_codes': actors.c.movie_codes,
		'actor_colleague_codes': actors.c.colleague_codes,
		'actor_code': actors.c.code
	})
	mapper(Director, directors, properties={
		'director_name': directors.c.name,
		'director_movie_codes': directors.c.movie_codes,
		'director_code': directors.c.code
	})
	mapper(Genre, genres, properties={
		'genre_name': genres.c.name,
		'genre_movie_codes': genres.c.movie_codes,
		'genre_code': genres.c.code
	})
	mapper(Watchlist, watchlists, properties={
		'watchlist_user_code': watchlists.c.user_code,
		'watchlist_movie_codes': watchlists.c.movie_codes,
		'watchlist_code': watchlists.c.code
	})