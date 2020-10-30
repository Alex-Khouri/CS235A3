class Watchlist:
	def __init__(self, arg_user_code, arg_movies=None, arg_movie_codes="", arg_code=None):
		self.watchlist_user_code = arg_user_code
		self.watchlist_movies = list() if arg_movies is None else arg_movies
		self.watchlist_movie_codes = arg_movie_codes
		self.watchlist_code = str(hash(self.watchlist_user_code)) if arg_code is None else arg_code
		self.iterIndex = 0

	def __repr__(self):
		return str(self.watchlist_movies)

	def __iter__(self):
		return self

	def __next__(self):
		if self.iterIndex >= len(self.watchlist_movies):
			self.iterIndex = 0
			raise StopIteration
		iterValue = self.watchlist_movies[self.iterIndex]
		self.iterIndex += 1
		return iterValue

	@property
	def user_code(self):
		return self.watchlist_user_code

	@property
	def movies(self):
		return self.watchlist_movies

	@property
	def movie_codes(self):
		return self.watchlist_movie_codes

	@property
	def code(self):
		return self.watchlist_code

	@user_code.setter
	def user_code(self, new):
		print("WARNING: Codes cannot be manually reassigned")

	@movies.setter
	def movies(self, newMovieList):
		if isinstance(newMovieList, list):
			self.watchlist_movies = newMovieList

	@movie_codes.setter
	def movie_codes(self, new):
		print("WARNING: Codes cannot be manually reassigned")

	@code.setter
	def code(self, new):
		print("WARNING: Codes cannot be manually reassigned")

	def add_movie(self, movie):
		if movie not in self.watchlist_movies:
			self.watchlist_movies.append(movie)
			self.watchlist_movie_codes = ",".join([movie.code for movie in self.watchlist_movies])

	def remove_movie(self, movie):
		if movie in self.watchlist_movies:
			self.watchlist_movies.remove(movie)
			self.watchlist_movie_codes = ",".join([movie.code for movie in self.watchlist_movies])

	def select_movie_to_watch(self, index):
		if index in range(len(self.watchlist_movies)):
			return self.watchlist_movies[index]
		else:
			return None

	def size(self):
		return len(self.watchlist_movies)

	def first_movie_in_watchlist(self):
		if len(self.watchlist_movies) > 0:
			return self.watchlist_movies[0]
		else:
			return None


if __name__ == "__main__":
	from getflix.domainmodel.actor import Actor
	from getflix.domainmodel.director import Director
	from getflix.domainmodel.genre import Genre
	from getflix.domainmodel.movie import Movie
	from getflix.domainmodel.review import Review
	from getflix.domainmodel.user import User