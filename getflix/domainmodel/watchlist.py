

class Watchlist:
	def __init__(self, arg_user_code, arg_movie_list=list(), arg_code=None):
		self.watchlist_user_code = arg_user_code
		self.watchlist_movie_list = arg_movie_list
		self.watchlist_code = str(hash(self.watchlist_user_code)) if arg_code is None else arg_code
		self.iterIndex = 0

	def __repr__(self):
		return str(self.watchlist_movie_list)

	def __iter__(self):
		return self

	def __next__(self):
		if self.iterIndex >= len(self.watchlist_movie_list):
			self.iterIndex = 0
			raise StopIteration
		iterValue = self.watchlist_movie_list[self.iterIndex]
		self.iterIndex += 1
		return iterValue

	@property
	def movie_list(self):
		return self.watchlist_movie_list

	@property
	def user_code(self):
		return self.watchlist_user_code

	@property
	def code(self):
		return self.watchlist_code

	@movie_list.setter
	def movie_list(self, newMovieList):
		if isinstance(newMovieList, list):
			self.watchlist_movie_list = newMovieList

	@user_code.setter
	def user_code(self, new):
		print("WARNING: Codes cannot be manually reassigned")

	@code.setter
	def code(self, new):
		print("WARNING: Codes cannot be manually reassigned")

	def add_movie(self, movie):
		if movie not in self.watchlist_movie_list:
			self.watchlist_movie_list.append(movie)
			return True
		else:
			return False

	def remove_movie(self, movie):
		if movie in self.watchlist_movie_list:
			self.watchlist_movie_list.remove(movie)
			return True
		else:
			return False

	def select_movie_to_watch(self, index):
		if index in range(len(self.watchlist_movie_list)):
			return self.watchlist_movie_list[index]
		else:
			return None

	def size(self):
		return len(self.watchlist_movie_list)

	def first_movie_in_watchlist(self):
		if len(self.watchlist_movie_list) > 0:
			return self.watchlist_movie_list[0]
		else:
			return None


if __name__ == "__main__":
	from getflix.domainmodel.actor import Actor
	from getflix.domainmodel.director import Director
	from getflix.domainmodel.genre import Genre
	from getflix.domainmodel.movie import Movie
	from getflix.domainmodel.review import Review
	from getflix.domainmodel.user import User