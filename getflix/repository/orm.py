from sqlalchemy import (
	Table, MetaData, Column, Integer, String, Date, DateTime, ForeignKey
)
from sqlalchemy.orm import mapper, relationship

metadata = MetaData()

# Lists of objects are stored as CSV strings of their corresponding IDs
users = Table(
	'users', metadata,
	Column('id', Integer, primary_key=True, autoincrement=True),
	Column('username', String(255), unique=True, nullable=False),
	Column('password', String(255), nullable=False)
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
	Column('actors', String(1024), nullable=False),  # CSV string of IDs
	Column('genres', String(1024), nullable=False),  # CSV string of IDs
	Column('runtime', Integer, nullable=False),
	Column('reviews', String(1024), nullable=False),  # CSV string of IDs
	Column('review_count', Integer, nullable=False),
	Column('rating', Integer, nullable=False),
	Column('votes', Integer, nullable=False),
	Column('movie_ID', String(1024), nullable=False)  # Movie title (without spaces) concatenated with year
)
actors = Table(
	'actors', metadata,
	Column('id', Integer, primary_key=True, autoincrement=True),
	Column('name', String(255), nullable=False),
	Column('movies', String(1024), nullable=False),  # CSV string of IDs
	Column('colleagues', String(1024), nullable=False)  # CSV string of IDs
)
directors = Table(
	'directors', metadata,
	Column('id', Integer, primary_key=True, autoincrement=True),
	Column('name', String(255), nullable=False),
	Column('movies', String(1024), nullable=False)  # CSV string of IDs
)
genres = Table(
	'genres', metadata,
	Column('id', Integer, primary_key=True, autoincrement=True),
	Column('name', String(255), nullable=False),
	Column('movies', String(1024), nullable=False)  # CSV string of IDs
)
watchlists = Table(
	'watchlists', metadata,
	Column('id', Integer, primary_key=True, autoincrement=True),
	Column('movies', String(1024), nullable=False)  # CSV string of IDs
)


article_tags = Table(
	'article_tags', metadata,
	Column('id', Integer, primary_key=True, autoincrement=True),
	Column('article_id', ForeignKey('articles.id')),
	Column('tag_id', ForeignKey('tags.id'))
)


def map_model_to_tables():
	mapper(User, users, properties={
		'_username': users.c.username,
		'_password': users.c.password,
		'_watchlist': relationship(model.Comment, backref='_user')
	})
	mapper(Review, comments, properties={
		'_comment': comments.c.comment,
		'_timestamp': comments.c.timestamp
	})
	articles_mapper = mapper(Movie, articles, properties={
		'_id': articles.c.id,
		'_date': articles.c.date,
		'_title': articles.c.title,
		'_first_para': articles.c.first_para,
		'_hyperlink': articles.c.hyperlink,
		'_image_hyperlink': articles.c.image_hyperlink,
		'_comments': relationship(model.Comment, backref='_article')
	})
	mapper(Genre, tags, properties={
		'_tag_name': tags.c.name,
		'_tagged_articles': relationship(
			articles_mapper,
			secondary=article_tags,
			backref="_tags"
		)
	})


if __name__ == "__main__":
	from getflix.domainmodel.actor import Actor
	from getflix.domainmodel.director import Director
	from getflix.domainmodel.genre import Genre
	from getflix.domainmodel.movie import Movie
	from getflix.domainmodel.review import Review
	from getflix.domainmodel.user import User
	from getflix.domainmodel.watchlist import Watchlist