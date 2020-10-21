
class Director:
	def __init__(self, name):
		if (isinstance(name, str) and len(name) > 0):
			self.director_name = name
		else:
			self.director_name = None
		self.director_movies = list()
		self.director_code = "".join([c for c in self.director_name if c.isalnum()])
	
	def __repr__(self):
		return f"<Director {self.director_name}>"
	
	def __eq__(self, other):
		return (self.__class__ == other.__class__ and self.director_name == other.name)
	
	def __lt__(self, other):
		return (self.director_name < other.name)
	
	def __hash__(self):
		return hash(self.director_name)
	
	@property
	def director_full_name(self):
		return self.director_name

	@property
	def movies(self):
		return self.director_movies

	@property
	def code(self):
		return self.director_code
	
	@director_full_name.setter
	def director_full_name(self, newName):
		self.director_name = newName

	@movies.setter
	def movies(self, newMovies):
		if isinstance(newMovies, list):
			self.director_movies = newMovies

	@code.setter
	def code(self, newCode):
		self.director_code = self.director_code  # This value should never be manually changed
		print("WARNING: Codes cannot be manually reassigned")

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

	def get_csv_movies(self):
		return ",".join([movie.code for movie in self.director_movies])


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