
class Actor:
	def __init__(self, name=None):
		if isinstance(name, str) and len(name) > 0:
			self.actor_name = name
		else:
			self.actor_name = None
		self.actor_movies = list()
		self.actor_movie_codes = ""
		self.actor_colleagues = list()
		self.actor_colleague_codes = ""
		self.actor_code = "".join([c for c in self.actor_name if c.isalnum()])
	
	def __repr__(self):
		return f"<Actor {self.actor_name}>"
	
	def __eq__(self, other):
		return self.__class__ == other.__class__ and self.actor_name == other.name
	
	def __lt__(self, other):
		return self.actor_name < other.name
	
	def __hash__(self):
		return hash(self.actor_name)
	
	@property
	def actor_full_name(self):
		return self.actor_name

	@property
	def movies(self):
		return self.actor_movies

	@property
	def colleagues(self):
		return self.actor_colleagues

	@property
	def code(self):
		return self.actor_code

	@property
	def movie_codes(self):
		return self.actor_movie_codes

	@property
	def colleague_codes(self):
		return self.actor_colleague_codes
	
	@actor_full_name.setter
	def actor_full_name(self, newName):
		self.actor_name = newName
		self.actor_code = "".join([c for c in self.actor_name if c.isalnum()])

	@movies.setter
	def movies(self, newMovies):
		if isinstance(newMovies, list):
			self.actor_movies = newMovies

	@colleagues.setter
	def colleagues(self, newColleagues):
		if isinstance(newColleagues, list):
			self.actor_colleagues = newColleagues

	@movie_codes.setter
	def movie_codes(self, new):
		print("WARNING: movie_codes cannot be manually reassigned")

	@colleague_codes.setter
	def colleague_codes(self, new):
		print("WARNING: colleague_codes cannot be manually reassigned")

	@code.setter
	def code(self, new):
		print("WARNING: Codes cannot be manually reassigned")
		
	def add_actor_colleague(self, colleague):
		self.actor_colleagues.append(colleague)
		self.actor_colleague_codes = ",".join([actor.code for actor in self.actor_colleagues])
		colleague.colleagues.append(self)

	def add_movie(self, newMovie):
		if newMovie not in self.actor_movies:
			self.actor_movies.append(newMovie)
			self.actor_movie_codes = ",".join([movie.code for movie in self.actor_movies])
			return True
		else:
			return False
		
	def check_if_this_actor_worked_with(self, colleague):
		return colleague in self.actor_colleagues

	def remove_movie(self, remMovie):
		if remMovie in self.actor_movies:
			self.actor_movies.remove(remMovie)
			self.actor_movie_codes = ",".join([movie.code for movie in self.actor_movies])
			return True
		else:
			return False


if __name__ == "__main__":
	from getflix.domainmodel.movie import Movie