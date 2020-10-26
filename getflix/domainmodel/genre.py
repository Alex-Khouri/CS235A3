
class Genre:
	def __init__(self, name=None):
		if (isinstance(name, str) and len(name) > 0):
			self.genre_name = name
		else:
			self.genre_name = None
		self.genre_movies = list()
		self.genre_movie_codes = ""
		self.genre_code = str(hash(self.genre_name))
	
	def __repr__(self):
		return f"<Genre {self.genre_name}>"
	
	def __eq__(self, other):
		return (self.__class__ == other.__class__ and self.genre_name == other.genre_name)
	
	def __lt__(self, other):
		return (self.genre_name < other.genre_name)
	
	def __hash__(self):
		return hash(self.genre_name)
	
	@property
	def name(self):
		return self.genre_name

	@property
	def movies(self):
		return self.genre_movies

	@property
	def code(self):
		return self.genre_code

	@property
	def movie_codes(self):
		return self.genre_movie_codes
	
	@name.setter
	def name(self, newName):
		self.genre_name = newName
		self.genre_code = str(hash(self.genre_name))

	@movies.setter
	def movies(self, newMovies):
		if isinstance(newMovies, list):
			self.genre_movies = newMovies

	@code.setter
	def code(self, new):
		print("WARNING: Codes cannot be manually reassigned")

	@movie_codes.setter
	def movie_codes(self, new):
		print("WARNING: movie_codes cannot be manually reassigned")

	def add_movie(self, newMovie):
		if not newMovie in self.genre_movies:
			self.genre_movies.append(newMovie)
			self.genre_movie_codes = ",".join([movie.code for movie in self.genre_movies])
			newMovie.add_genre(self)
			return True
		else:
			return False

	def remove_movie(self, remMovie):
		if remMovie in self.genre_movies:
			self.genre_movies.remove(remMovie)
			self.genre_movie_codes = ",".join([movie.code for movie in self.genre_movies])
			remMovie.remove_genre(self)
			return True
		else:
			return False


if __name__ == "__main__":
	from getflix.domainmodel.movie import Movie