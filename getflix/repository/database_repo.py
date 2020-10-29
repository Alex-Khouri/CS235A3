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
		self.repo_actors = set()
		self.repo_directors = set()
		self.repo_genres = set()
		self.repo_movies = list()
		self.repo_reviews = list()
		self.repo_users = list()
		self.repo_watchlists = list()

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
	def movies(self):
		return self.repo_movies

	@property
	def reviews(self):
		return self.repo_reviews

	@property
	def users(self):
		return self.repo_users

	@property
	def watchlists(self):
		return self.repo_watchlists

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

	@movies.setter
	def movies(self, newMovies):
		if isinstance(newMovies, list):
			self.repo_movies = newMovies

	@reviews.setter
	def reviews(self, newReviews):
		if isinstance(newReviews, list):
			self.repo_reviews = newReviews

	@users.setter
	def users(self, newUsers):
		if isinstance(newUsers, list):
			self.repo_users = newUsers

	@watchlists.setter
	def watchlists(self, newWatchlists):
		if isinstance(newWatchlists, list):
			self.repo_watchlists = newWatchlists

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

		empty_codes = 0  # DEBUGGING
		for actor in self.repo_actors:
			if len(actor.movie_codes) == 0 and len(actor.movies) > 0:  # DEBUGGING
				empty_codes += 1  # DEBUGGING
			cursor.execute(f"""INSERT INTO actors (name, movie_codes, colleague_codes, code)
							VALUES ("{actor.actor_full_name}", "{actor.movie_codes}",
									"{actor.colleague_codes}", "{actor.code}")""")
		print(f"*** ERROR: {empty_codes} actors have empty movie codes!")  # DEBUGGING

		for director in self.repo_directors:
			cursor.execute(f"""INSERT INTO directors (name, movie_codes, code)
							VALUES ("{director.director_full_name}", "{director.movie_codes}",
									"{director.code}")""")
		for movie in self.repo_movies:
			movie_description = movie.description.replace("\"", "'")
			cursor.execute(f"""INSERT INTO movies (title, year, description, director_code, actor_codes,
							genre_codes, runtime_minutes, review_codes, review_count, rating, votes, code)
							VALUES ("{movie.title}", {movie.year}, "{movie_description}",
									"{movie.director_code}", "{movie.actor_codes}", "{movie.genre_codes}",
									{movie.runtime_minutes}, "{movie.review_codes}", {movie.review_count},
									"{movie.rating}", {movie.votes}, "{movie.code}")""")
		conn.commit()
		conn.close()

	def load(self, engine):
		conn = engine.raw_connection()
		cursor = conn.cursor()
		# STEP ONE: Retrieve entries from database
		cursor.execute("""SELECT * FROM actors""")
		actors = cursor.fetchall()
		cursor.execute("""SELECT * FROM directors""")
		directors = cursor.fetchall()
		cursor.execute("""SELECT * FROM genres""")
		genres = cursor.fetchall()
		cursor.execute("""SELECT * FROM movies""")
		movies = cursor.fetchall()
		cursor.execute("""SELECT * FROM reviews""")
		reviews = cursor.fetchall()
		cursor.execute("""SELECT * FROM users""")
		users = cursor.fetchall()
		cursor.execute("""SELECT * FROM watchlists""")
		watchlists = cursor.fetchall()

		#  STEP TWO: Convert entries into isolated object references
		for row in actors:
			actor = Actor(row[1], list(), row[2], list(), row[3], row[4])
			self.repo_actors.add(actor)
		for row in directors:
			director = Director(row[1], list(), row[2], row[3])
			self.repo_directors.add(director)
		for row in genres:
			genre = Genre(row[1], list(), row[2], row[3])
			self.repo_genres.add(genre)
		for row in movies:
			movie = Movie(row[1], row[2], row[3], None, row[4], list(), row[5], list(), row[6], row[7],
						  list(), row[8], row[9], row[10], row[11], row[12])
			self.repo_movies.append(movie)
		for row in reviews:
			review = Review(None, row[1], None, row[2], row[3], row[4], row[5], row[6], row[7])
			self.repo_reviews.append(review)
		for row in users:
			user = User(row[1], row[2], list(), row[3], list(), row[4], row[5], None, row[6], row[7])
			self.repo_users.append(user)
		for row in watchlists:
			watchlist = Watchlist(row[1], list(), row[2], row[3])
			self.repo_watchlists.append(watchlist)

		# STEP THREE: Populate object relationships
		for actor in self.repo_actors:
			for code in actor.movie_codes:
				actor.add_movie(self.find_movie(code))
			for code in actor.colleague_codes:
				actor.add_actor_colleague(self.find_actor(code))
		for director in self.repo_directors:
			for code in director.movie_codes:
				director.add_movie(self.find_movie(code))
		for genre in self.repo_genres:
			for code in genre.movie_codes:
				genre.add_movie(self.find_movie(code))
		for movie in self.repo_movies:
			movie.director = self.find_director(movie.director_code)
			for code in movie.actor_codes:
				movie.add_actor(self.find_actor(code))
			for code in movie.genre_codes:
				movie.add_genre(self.find_genre(code))
			for code in movie.review_codes:
				movie.add_review(self.find_review(code))
		for review in self.repo_reviews:
			review.user = self.find_user(review.user_code)
			review.movie = self.find_movie(review.movie_code)
		for user in self.repo_users:
			for code in user.watched_movie_codes:
				user.watched_movies.append(self.find_movie(code))  # Can't use watch_movie() for this
			for code in user.review_codes:
				user.add_review(self.find_review(code))
			user.watchlist = self.find_watchlist(user.watchlist_code)
		for watchlist in self.repo_watchlists:
			for code in watchlist.movie_codes:
				watchlist.add_movie(self.find_movie(code))
		conn.commit()
		conn.close()

	def add_user(self, newUser, engine):
		if newUser not in self.repo_users and newUser.username not in [user.username for user in self.repo_users]:
			self.repo_users.append(newUser)
			conn = engine.raw_connection()
			cursor = conn.cursor()
			cursor.execute(f"""INSERT INTO users (username, password, watched_codes, review_codes,
							timewatching, watchlist_code, code) VALUES ("{newUser.username}",
							"{newUser.password}", "", "", 0, "{newUser.watchlist.code}", "{newUser.code}")""")
			cursor.execute(f"""INSERT INTO watchlists (user_code, movie_codes, code)
							VALUES ("{newUser.code}", "", "{newUser.watchlist.code}")""")
			cursor.commit()
			conn.close()
			return True
		else:
			return False

	def remove_user(self, remUser, engine):
		if remUser in self.repo_users:
			self.repo_users.remove(remUser)
			conn = engine.raw_connection()
			cursor = conn.cursor()
			cursor.execute(f"""DELETE FROM users WHERE username == "{remUser.username}" """)
			cursor.execute(f"""DELETE FROM watchlists WHERE user_code = "{remUser.code}" """)
			cursor.commit()
			conn.close()
			return True
		else:
			return False

	def add_to_watchlist(self, user, newMovie, engine):
		conn = engine.raw_connection()
		cursor = conn.cursor()
		cursor.execute(f"""UPDATE watchlists
						SET movie_codes = "{user.watchlist.movie_codes + ',' + newMovie.code}"
						WHERE code = "{user.watchlist.code}" """)
		cursor.commit()
		conn.close()

	def remove_from_watchlist(self, user, remMovie, engine):
		conn = engine.raw_connection()
		cursor = conn.cursor()
		new_movie_codes = user.watchlist.movie_codes.split(",")
		new_movie_codes.remove(remMovie.code)
		cursor.execute(f"""UPDATE watchlists
						SET movie_codes = "{",".join(new_movie_codes)}"
						WHERE code = "{user.watchlist.code}" """)
		cursor.commit()
		conn.close()

	def add_review(self, review, user, movie, engine):
		conn = engine.raw_connection()
		cursor = conn.cursor()
		cursor.execute(f"""INSERT INTO reviews (user_code, movie_code, text, rating, timestamp, date, code)
						VALUES ("{review.user_code}", "{review.movie_code}", "{review.text}",
						"{review.rating}", "{review.timestamp}", "{review.date}", "{review.code}")""")
		cursor.execute(f"""UPDATE movies SET review_codes = "{movie.review_codes}",
										SET review_count = "{movie.review_count}",
										SET rating = "{movie.rating}",
										SET votes = "{movie.votes}"
						WHERE code = "{movie.code}" """)
		cursor.execute(f"""UPDATE users SET review_codes = "{user.review_codes + "," + review.code}" 
						WHERE code = "{user.code}" """)
		cursor.commit()
		conn.close()


	def get_user(self, username):
		if username is not None:
			for user in self.repo_users:
				if user.username.strip().lower() == username.strip().lower():
					return user
		return None

	def get_movie(self, title):
		if title is not None:
			for movie in self.repo_movies:
				if movie.title.strip().lower() == title.strip().lower():
					return movie
		return None

	def get_watchlist(self, username):
		if username is not None:
			user = self.get_user(username)
			if user is not None:
				return user.watchlist
		return None

	# `Find` functions retrieve objects using codes
	def find_actor(self, code):
		for actor in self.repo_actors:
			if actor.code == code:
				return actor
		return None

	def find_director(self, code):
		for director in self.repo_directors:
			if director.code == code:
				return director
		return None

	def find_genre(self, code):
		for genre in self.repo_genres:
			if genre.code == code:
				return genre
		return None

	def find_movie(self, code):
		for movie in self.repo_movies:
			if movie.code == code:
				return movie
		return None

	def find_review(self, code):
		for review in self.repo_reviews:
			if review.code == code:
				return review
		return None

	def find_user(self, code):
		for user in self.repo_users:
			if user.code == code:
				return user
		return None

	def find_watchlist(self, code):
		for watchlist in self.repo_watchlists:
			if watchlist.code == code:
				return watchlist
		return None


if __name__ == "__main__":
	from getflix.domainmodel.actor import Actor
	from getflix.domainmodel.director import Director
	from getflix.domainmodel.genre import Genre
	from getflix.domainmodel.movie import Movie
	from getflix.domainmodel.review import Review
	from getflix.domainmodel.user import User
	from getflix.domainmodel.watchlist import Watchlist
