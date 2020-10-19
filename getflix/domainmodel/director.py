
class Director:
	def __init__(self, name):
		if (isinstance(name, str) and len(name) > 0):
			self.name = name
		else:
			self.name = None
		self.director_movies = list()
	
	def __repr__(self):
		return f"<Director {self.name}>"
	
	def __eq__(self, other):
		return (self.__class__ == other.__class__ and self.name == other.name)
	
	def __lt__(self, other):
		return (self.name < other.name)
	
	def __hash__(self):
		return hash(self.name)
	
	@property
	def director_full_name(self):
		return self.name

	@property
	def movies(self):
		return self.director_movies
	
	@director_full_name.setter
	def director_full_name(self, newName):
		self.name = newName

	@movies.setter
	def movies(self, newMovies):
		if isinstance(newMovies, list):
			self.director_movies = newMovies

	def add_movie(self, newMovie):
		if not newMovie in self.director_movies:
			self.director_movies.append(newMovie)
			return True
		else:
			return False

	def remove_movie(self, remMovie):
		if remMovie in self.director_movies:
			self.director_movies.remove(remMovie)
			return True
		else:
			return False


class TestDirectorMethods:

	def test_init(self):
		director1 = Director("Taika Waititi")
		assert repr(director1) == "<Director Taika Waititi>"
		director2 = Director("")
		assert director2.director_full_name is None
		director3 = Director(42)
		assert director3.director_full_name is None


if __name__ == "__main__":
	from getflix.domainmodel.movie import Movie