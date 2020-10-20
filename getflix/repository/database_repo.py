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

	def reset_session(self):
		self.close_current_session()
		self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

	def close_current_session(self):
		if not self.__session is None:
			self.__session.close()


class DatabaseRepo:

	def __init__(self, file_name, session_factory):
		csvReader = MovieFileCSVReader(file_name)
		csvReader.read_csv_file()
		self.repo_movies = csvReader.dataset_of_movies
		self.repo_actors = csvReader.dataset_of_actors
		self.repo_directors = csvReader.dataset_of_directors
		self.repo_genres = csvReader.dataset_of_genres
		self.repo_users = list()
		self._session_cm = SessionContextManager(session_factory)

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


# >> NEW DATABASE CODE (START)
def article_record_generator(filename: str):
	with open(filename, mode='r', encoding='utf-8-sig') as infile:
		reader = csv.reader(infile)

	# Read first line of the CSV file.
	headers = next(reader)

	# Read remaining rows from the CSV file.
	for row in reader:

		article_data = row
		article_key = article_data[0]

		# Strip any leading/trailing white space from data read.
		article_data = [item.strip() for item in article_data]

		number_of_tags = len(article_data) - 6
		article_tags = article_data[-number_of_tags:]

		# Add any new tags; associate the current article with tags.
		for tag in article_tags:
			if tag not in tags.keys():
				tags[tag] = list()
			tags[tag].append(article_key)

		del article_data[-number_of_tags:]

		yield article_data


def get_tag_records():
	tag_records = list()
	tag_key = 0

	for tag in tags.keys():
		tag_key = tag_key + 1
		tag_records.append((tag_key, tag))
	return tag_records


def article_tags_generator():
	article_tags_key = 0
	tag_key = 0

	for tag in tags.keys():
		tag_key = tag_key + 1
		for article_key in tags[tag]:
			article_tags_key = article_tags_key + 1
			yield article_tags_key, article_key, tag_key


def generic_generator(filename, post_process=None):
	with open(filename) as infile:
		reader = csv.reader(infile)

		# Read first line of the CSV file.
		next(reader)

		# Read remaining rows from the CSV file.
		for row in reader:
			# Strip any leading/trailing white space from data read.
			row = [item.strip() for item in row]

			if post_process is not None:
				row = post_process(row)
			yield row


def process_user(user_row):
	user_row[2] = generate_password_hash(user_row[2])
	return user_row


def populate(engine, data_path):
	conn = engine.raw_connection()
	cursor = conn.cursor()

	global tags
	tags = dict()

	insert_articles = """
		INSERT INTO articles (
		id, date, title, first_para, hyperlink, image_hyperlink)
		VALUES (?, ?, ?, ?, ?, ?)"""
	cursor.executemany(insert_articles, article_record_generator(data_path))

	insert_tags = """
		INSERT INTO tags (
		id, name)
		VALUES (?, ?)"""
	cursor.executemany(insert_tags, get_tag_records())

	insert_article_tags = """
		INSERT INTO article_tags (
		id, article_id, tag_id)
		VALUES (?, ?, ?)"""
	cursor.executemany(insert_article_tags, article_tags_generator())

	insert_users = """
		INSERT INTO users (
		id, username, password)
		VALUES (?, ?, ?)"""
	cursor.executemany(insert_users, generic_generator(os.path.join(data_path, 'users.csv'), process_user))

	insert_comments = """
		INSERT INTO comments (
		id, user_id, article_id, comment, timestamp)
		VALUES (?, ?, ?, ?, ?)"""
	cursor.executemany(insert_comments, generic_generator(os.path.join(data_path, 'comments.csv')))

	conn.commit()
	conn.close()


# << NEW DATABASE CODE (END)


if __name__ == "__main__":
	from getflix.domainmodel.actor import Actor
	from getflix.domainmodel.director import Director
	from getflix.domainmodel.genre import Genre
	from getflix.domainmodel.movie import Movie
	from getflix.domainmodel.review import Review
	from getflix.domainmodel.user import User
	from getflix.domainmodel.watchlist import Watchlist
