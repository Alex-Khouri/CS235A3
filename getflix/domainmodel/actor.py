
class Actor:
	def __init__(self, name=None):
		if isinstance(name, str) and len(name) > 0:
			self.actor_name = name
		else:
			self.actor_name = None
		self.actor_movies = list()
		self.actor_csvMovies = ",".join([movie.code for movie in self.actor_movies])
		self.actor_colleagues = list()
		self.actor_csvColleagues = ",".join([actor.code for actor in self.actor_colleagues])
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
	def csvMovies(self):
		return self.actor_csvMovies

	@property
	def csvColleagues(self):
		return self.actor_csvColleagues
	
	@actor_full_name.setter
	def actor_full_name(self, newName):
		self.actor_name = newName

	@movies.setter
	def movies(self, newMovies):
		if isinstance(newMovies, list):
			self.actor_movies = newMovies

	@colleagues.setter
	def colleagues(self, newColleagues):
		if isinstance(newColleagues, list):
			self.actor_colleagues = newColleagues

	@csvMovies.setter
	def csvMovies(self, new):
		print("WARNING: csvMovies cannot be manually reassigned")

	@csvColleagues.setter
	def csvColleagues(self, new):
		print("WARNING: csvColleagues cannot be manually reassigned")

	@code.setter
	def code(self, new):
		print("WARNING: Codes cannot be manually reassigned")
		
	def add_actor_colleague(self, colleague):
		self.actor_colleagues.append(colleague)
		self.actor_csvColleagues = ",".join([actor.code for actor in self.actor_colleagues])
		colleague.colleagues.append(self)

	def add_movie(self, newMovie):
		if newMovie not in self.actor_movies:
			self.actor_movies.append(newMovie)
			self.actor_csvMovies = ",".join([movie.code for movie in self.actor_movies])
			return True
		else:
			return False
		
	def check_if_this_actor_worked_with(self, colleague):
		return colleague in self.actor_colleagues

	def remove_movie(self, remMovie):
		if remMovie in self.actor_movies:
			self.actor_movies.remove(remMovie)
			self.actor_csvMovies = ",".join([movie.code for movie in self.actor_movies])
			return True
		else:
			return False


if __name__ == "__main__":
	from getflix.domainmodel.movie import Movie