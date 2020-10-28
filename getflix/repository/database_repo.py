from getflix.datafilereaders.movie_file_csv_reader import MovieFileCSVReader

from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack
from werkzeug.security import generate_password_hash


class SessionContextManager:
	def __init__(self, session_factory):
		self.__session_factory = session_factory
		self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

	def __enter__(self):
		return self

	def __exit__(self, *args):
		self.rollback()

	@property
	def session(self):
		return self.__session

	def commit(self):
		self.__session.commit()

	def rollback(self):
		self.__session.rollback()

	def reset(self):
		self.close()
		self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

	def close(self):
		if not self.__session is None:
			self.__session.close()

	def execute(self, query):
		self.__session.execute(query)
		self.__session.commit()
		self.__session.close()


class DatabaseRepo:

	def __init__(self, session_factory):
		self.session_manager = SessionContextManager(session_factory)
		self.repo_genres = set()
		self.repo_actors = set()
		self.repo_directors = set()
		self.repo_movies = list()
		self.repo_users = list()

	@property
	def movies(self):
		return self.repo_movies

	@property
	def actors(self):
		return self.repo_actors

	@property
	def directors(self):
		return self.repo_directors

	@property
	def genres(self):
		return self.repo_genres

	@property
	def users(self):
		return self.repo_users

	@movies.setter
	def movies(self, newMovies):
		if isinstance(newMovies, list):
			self.repo_movies = newMovies

	@actors.setter
	def actors(self, newActors):
		if isinstance(newActors, set):
			self.repo_actors = newActors

	@directors.setter
	def directors(self, newDirectors):
		if isinstance(newDirectors, set):
			self.repo_directors = newDirectors

	@genres.setter
	def genres(self, newGenres):
		if isinstance(newGenres, set):
			self.repo_genres = newGenres

	@users.setter
	def users(self, newUsers):
		if isinstance(newUsers, list):
			self.repo_users = newUsers

	def populate(self, engine, data_path):
		conn = engine.raw_connection()
		cursor = conn.cursor()
		csvReader = MovieFileCSVReader(data_path)
		csvReader.read_csv_file()
		self.repo_genres = csvReader.dataset_of_genres
		self.repo_actors = csvReader.dataset_of_actors
		self.repo_directors = csvReader.dataset_of_directors
		self.repo_movies = csvReader.dataset_of_movies
		for genre in self.repo_genres:
			cursor.execute(f"""INSERT INTO genres (name, movie_codes, code)
							VALUES ("{genre.name}", "{genre.movie_codes}", "{genre.code}")""")
		for actor in self.repo_actors:
			cursor.execute(f"""INSERT INTO actors (name, movie_codes, colleague_codes, code)
							VALUES ("{actor.actor_full_name}", "{actor.movie_codes}",
									"{actor.colleague_codes}", "{actor.code}")""")
		for director in self.repo_directors:
			cursor.execute(f"""INSERT INTO directors (name, movie_codes, code)
							VALUES ("{director.director_full_name}", "{director.movie_codes}",
									"{director.code}")""")
		for movie in self.repo_movies:
			movie_description = movie.description.replace("\"", "'")  # Potentially find a way to retain double-quotes?
			cursor.execute(f"""INSERT INTO movies (title, year, description, director_code, actor_codes,
							genre_codes, runtime_minutes, reviews, review_count, rating, votes, code)
							VALUES ("{movie.title}", {movie.year}, "{movie_description}",
									"{movie.director_code}", "{movie.actor_codes}", "{movie.genre_codes}",
									{movie.runtime_minutes}, "{movie.reviews}", {movie.review_count},
									"{movie.rating}", {movie.votes}, "{movie.code}")""")
		conn.commit()
		conn.close()

	def load(self, engine):
		conn = engine.raw_connection()
		cursor = conn.cursor()
		cursor.execute("""SELECT name, movie_codes, code FROM genres""")
		genres = cursor.fetchall()
		cursor.execute("""SELECT name, movie_codes, colleague_codes, code FROM actors""")
		actors = cursor.fetchall()
		cursor.execute("""SELECT name, movie_codes, code FROM directors""")
		directors = cursor.fetchall()
		cursor.execute("""SELECT title, year, description, director_code, actor_codes,
						genre_codes, runtime_minutes, reviews, review_count, rating, votes, code
						FROM movies""")
		movies = cursor.fetchall()

		# Updated ORM to match updated domain model objects099
		# Fetch users, reviews, and watchlists and load into memory

		conn.commit()
		conn.close()

	def add_user(self, newUser):
		if newUser not in self.repo_users and newUser.username not in [user.username for user in self.repo_users]:
			self.repo_users.append(newUser)
			return True
		else:
			return False

	def remove_user(self, remUser):
		if remUser in self.repo_users:
			self.repo_users.remove(remUser)
			return True
		else:
			return False

	def get_user(self, username):
		if username is not None:
			for user in self.repo_users:
				if user.username.strip().lower() == username.strip().lower():
					return user
		return None

	def get_movie(self, movieTitle):
		if movieTitle is None:
			return None
		for movie in self.repo_movies:
			if movie.title.strip().lower() == movieTitle.strip().lower():
				return movie
		return None

	def get_watchlist(self, username):
		if username is not None:
			user = self.get_user(username)
			if user is not None:
				return user.watchlist
		return None


if __name__ == "__main__":
	from getflix.domainmodel.actor import Actor
	from getflix.domainmodel.director import Director
	from getflix.domainmodel.genre import Genre
	from getflix.domainmodel.movie import Movie
	from getflix.domainmodel.review import Review
	from getflix.domainmodel.user import User
	from getflix.domainmodel.watchlist import Watchlist
