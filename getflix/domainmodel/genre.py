
class Genre:
	def __init__(self, name=None):
		if (isinstance(name, str) and len(name) > 0):
			self.genre_name = name
		else:
			self.genre_name = None
		self.genre_movies = list()
	
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
	
	@name.setter
	def name(self, newName):
		self.genre_name = newName

	@movies.setter
	def movies(self, newMovies):
		if isinstance(newMovies, list):
			self.genre_movies = newMovies

	def add_movie(self, newMovie):
		if not newMovie in self.genre_movies:
			self.genre_movies.append(newMovie)
			newMovie.add_genre(self)
			return True
		else:
			return False

	def remove_movie(self, remMovie):
		if remMovie in self.genre_movies:
			self.genre_movies.remove(remMovie)
			remMovie.remove_genre(self)
			return True
		else:
			return False


if __name__ == "__main__":
	from getflix.domainmodel.movie import Movie