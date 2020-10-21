

class Movie:
	def __init__(self, movTitle, movYear):
		self.movie_title = None
		if isinstance(movTitle, str) and len(movTitle) > 0:
			self.movie_title = movTitle.strip()
		self.movie_year = None
		if isinstance(movYear, int) and movYear >= 1900:
			self.movie_year = movYear
		self.movie_description = None
		self.movie_director = None
		self.movie_director_code = ""
		self.movie_actors = list()
		self.movie_actor_codes = ""
		self.movie_genres = list()
		self.movie_genre_codes = ""
		self.movie_runtime_minutes = 0
		self.movie_reviews = list()
		self.movie_review_count = 0
		self.movie_rating = None
		self.movie_votes = 0
		self.movie_code = "".join([c for c in (self.movie_title + str(self.movie_year)) if c.isalnum()])
	
	def __repr__(self):
		return f"<Movie {self.movie_title}, {self.movie_year}>"
	
	def __eq__(self, other):
		return self.__class__ == other.__class__ and self.movie_title == other.movie_title and self.movie_year == other.movie_year
	
	def __lt__(self, other):
		if self.movie_title == other.movie_title:
			return self.movie_year < other.movie_year
		else:
			return self.movie_title < other.movie_title
	
	def __hash__(self):
		return hash(self.movie_title + str(self.movie_year))
		
	@property
	def title(self):
		return self.movie_title

	@property
	def year(self):
		return self.movie_year
	
	@property
	def description(self):
		return self.movie_description
		
	@property
	def director(self):
		return self.movie_director
		
	@property
	def actors(self):
		return self.movie_actors
		
	@property
	def genres(self):
		return self.movie_genres
		
	@property
	def runtime_minutes(self):
		return self.movie_runtime_minutes

	@property
	def reviews(self):
		return self.movie_reviews

	@property
	def rating(self):
		return round(self.movie_rating, 1)

	@property
	def votes(self):
		return self.movie_votes

	@property
	def code(self):
		return self.movie_code

	@property
	def review_count(self):
		return self.movie_review_count

	@property
	def actor_codes(self):
		return self.movie_actor_codes

	@property
	def genre_codes(self):
		return self.movie_genre_codes

	@property
	def director_code(self):
		return self.movie_director_code

	@title.setter
	def title(self, newTitle):
		if isinstance(newTitle, str) and len(newTitle) > 0:
			self.movie_title = newTitle.strip()
			self.movie_code = "".join([c for c in (self.movie_title + str(self.movie_year)) if c.isalnum()])

	@year.setter
	def year(self, newYear):
		if isinstance(newYear, int) and newYear >= 1900:
			self.movie_year = newYear
			self.movie_code = "".join([c for c in (self.movie_title + str(self.movie_year)) if c.isalnum()])

	@description.setter
	def description(self, newDescrip):
		if isinstance(newDescrip, str) and len(newDescrip) > 0:
			self.movie_description = newDescrip.strip()
	
	@director.setter
	def director(self, newDirector):
		self.movie_director = newDirector
		self.movie_director_code = self.movie_director.code
			
	@actors.setter
	def actors(self, newActors):
		if isinstance(newActors, list):
			self.movie_actors = newActors
			self.movie_actor_codes = ",".join([actor.code for actor in self.movie_actors])
			
	@genres.setter
	def genres(self, newGenres):
		if isinstance(newGenres, list):
			self.movie_genres = newGenres
			self.movie_genre_codes = ",".join([genre.code for genre in self.movie_genres])
			
	@runtime_minutes.setter
	def runtime_minutes(self, newRuntime):
		if isinstance(newRuntime, int):
			if newRuntime >= 0:
				self.movie_runtime_minutes = newRuntime
			else:
				raise ValueError('ValueError: Negative runtime value!')

	@reviews.setter
	def reviews(self, newReviews):
		if isinstance(newReviews, list):
			self.movie_reviews = newReviews

	@rating.setter
	def rating(self, newRating):
		if isinstance(newRating, float):
			self.movie_rating = newRating

	@votes.setter
	def votes(self, newVotes):
		if isinstance(newVotes, int):
			self.movie_votes = newVotes

	@code.setter
	def code(self, new):
		print("WARNING: Codes cannot be manually reassigned")

	@review_count.setter
	def review_count(self, new):
		print("WARNING: Movie review counts cannot be manually reassigned")

	@actor_codes.setter
	def actor_codes(self, new):
		print("WARNING: actor_codes cannot be manually reassigned")

	@genre_codes.setter
	def genre_codes(self, new):
		print("WARNING: genre_codes cannot be manually reassigned")

	@director_code.setter
	def director_code(self, new):
		print("WARNING: director_code cannot be manually reassigned")

	def add_actor(self, newActor):
		if not newActor in self.movie_actors:
			self.movie_actors.append(newActor)
			self.movie_actor_codes = ",".join([actor.code for actor in self.movie_actors])
			return True
		else:
			return False
			
	def add_genre(self, newGenre):
		if not newGenre in self.movie_genres:
			self.movie_genres.append(newGenre)
			self.movie_genre_codes = ",".join([genre.code for genre in self.movie_genres])
			return True
		else:
			return False

	def add_review(self, newReview):
		self.movie_reviews.append(newReview)
		self.movie_review_count += 1
		self.movie_votes += 1
		v = self.movie_votes
		if self.movie_rating is None:
			self.movie_rating = newReview.rating
		else:
			self.movie_rating = self.movie_rating*((v-1)/v) + newReview.rating*(1/v)
			
	def remove_actor(self, remActor):
		if remActor in self.movie_actors:
			self.movie_actors.remove(remActor)
			self.movie_actor_codes = ",".join([actor.code for actor in self.movie_actors])
			return True
		elif isinstance(remActor, str):
			for actor in self.movie_actors:
				if actor.actor_full_name == remActor:
					self.movie_actors.remove(actor)
					self.movie_actor_codes = ",".join([actor.code for actor in self.movie_actors])
					return True
		else:
			return False
			
	def remove_genre(self, remGenre):
		if remGenre in self.movie_genres:
			self.movie_genres.remove(remGenre)
			self.movie_genre_codes = ",".join([genre.code for genre in self.movie_genres])
			return True
		elif isinstance(remGenre, str):
			for genre in self.movie_genres:
				if genre.name == remGenre:
					self.movie_genres.remove(genre)
					self.movie_genre_codes = ",".join([genre.code for genre in self.movie_genres])
					return True
		else:
			return False

	def remove_review(self, remReview):
		if remReview in self.movie_reviews:
			self.movie_reviews.remove(remReview)
			self.movie_votes -= 1
			v = self.movie_votes
			if self.movie_votes == 0:
				self.movie_rating = None
			else:
				self.movie_rating = self.movie_rating*((v+1)/v) - remReview.rating*(1/v)
			return True
		else:
			return False

	def get_actors_string(self):
		return ", ".join([actor.actor_full_name for actor in self.movie_actors])

	def get_genres_string(self):
		return ", ".join([genre.name for genre in self.movie_genres])


if __name__ == "__main__":
	from getflix.domainmodel.actor import Actor
	from getflix.domainmodel.director import Director
	from getflix.domainmodel.genre import Genre
	from getflix.domainmodel.review import Review
	from getflix.domainmodel.user import User
	from getflix.domainmodel.watchlist import Watchlist