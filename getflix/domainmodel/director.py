
class Director:
	def __init__(self, name):
		if (isinstance(name, str) and len(name) > 0):
			self.director_name = name
		else:
			self.director_name = None
		self.director_movies = list()
		self.director_movie_codes = ""
		self.director_code = "".join([c for c in self.director_name if c.isalnum()])
	
	def __repr__(self):
		return f"<Director {self.director_name}>"
	
	def __eq__(self, other):
		return self.__class__ == other.__class__ and self.director_name == other.director_full_name
	
	def __lt__(self, other):
		return self.director_name < other.director_full_name
	
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

	@property
	def movie_codes(self):
		return self.director_movie_codes
	
	@director_full_name.setter
	def director_full_name(self, newName):
		self.director_name = newName
		self.director_code = "".join([c for c in self.director_name if c.isalnum()])

	@movies.setter
	def movies(self, newMovies):
		if isinstance(newMovies, list):
			self.director_movies = newMovies

	@code.setter
	def code(self, new):
		print("WARNING: Codes cannot be manually reassigned")

	@movie_codes.setter
	def movie_codes(self, new):
		print("WARNING: movie_codes cannot be manually reassigned")

	def add_movie(self, newMovie):
		if not newMovie in self.director_movies:
			self.director_movies.append(newMovie)
			self.director_movie_codes = ",".join([movie.code for movie in self.director_movies])
			return True
		else:
			return False

	def remove_movie(self, remMovie):
		if remMovie in self.director_movies:
			self.director_movies.remove(remMovie)
			self.director_movie_codes = ",".join([movie.code for movie in self.director_movies])
			return True
		else:
			return False


if __name__ == "__main__":
	from getflix.domainmodel.movie import Movie