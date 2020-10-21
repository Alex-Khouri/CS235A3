
class Actor:
	def __init__(self, name=None):
		if isinstance(name, str) and len(name) > 0:
			self.actor_name = name
		else:
			self.actor_name = None
		self.actor_movies = list()
		self.actor_colleagues = list()
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

	@code.setter
	def code(self, newCode):
		self.actor_code = self.actor_code  # This value should never be manually changed
		print("WARNING: Codes cannot be manually reassigned")
		
	def add_actor_colleague(self, colleague):
		self.actor_colleagues.append(colleague)
		colleague.colleagues.append(self)

	def add_movie(self, newMovie):
		if newMovie not in self.actor_movies:
			self.actor_movies.append(newMovie)
			return True
		else:
			return False
		
	def check_if_this_actor_worked_with(self, colleague):
		return colleague in self.actor_colleagues

	def remove_movie(self, remMovie):
		if remMovie in self.actor_movies:
			self.actor_movies.remove(remMovie)
			return True
		else:
			return False


if __name__ == "__main__":
	from getflix.domainmodel.movie import Movie