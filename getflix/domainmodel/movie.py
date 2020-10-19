

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
		self.movie_actors = list()
		self.movie_genres = list()
		self.movie_runtime_minutes = 0
		self.movie_reviews = list()
		self.movie_review_count = 0
		self.movie_rating = None
		self.movie_votes = 0
		self.movie_ID = None
		if self.movie_title is not None and self.movie_year is not None:
			self.movie_ID = self.movie_title.replace(" ", "") + str(self.movie_year)
	
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
	def ID(self):
		return self.movie_ID

	@property
	def review_count(self):
		return self.movie_review_count

	@title.setter
	def title(self, newTitle):
		if isinstance(newTitle, str) and len(newTitle) > 0:
			self.movie_title = newTitle.strip()

	@year.setter
	def year(self, newYear):
		if isinstance(newYear, int) and newYear >= 1900:
			self.movie_year = newYear

	@description.setter
	def description(self, newDescrip):
		if isinstance(newDescrip, str) and len(newDescrip) > 0:
			self.movie_description = newDescrip.strip()
	
	@director.setter
	def director(self, newDirector):
		self.movie_director = newDirector
			
	@actors.setter
	def actors(self, newActors):
		if isinstance(newActors, list):
			self.movie_actors = newActors
			
	@genres.setter
	def genres(self, newGenres):
		if isinstance(newGenres, list):
			self.movie_genres = newGenres
			
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

	@ID.setter
	def ID(self, newID):
		self.movie_ID = self.movie_ID  # This value should never be manually changed
		print("WARNING: Movie IDs cannot be manually reassigned")

	@review_count.setter
	def review_count(self, newCount):
		self.movie_review_count = self.movie_review_count  # This value should never be manually changed
		print("WARNING: Movie review counts cannot be manually reassigned")

	def add_actor(self, newActor):
		if not newActor in self.movie_actors:
			self.movie_actors.append(newActor)
			return True
		else:
			return False
			
	def add_genre(self, newGenre):
		if not newGenre in self.movie_genres:
			self.movie_genres.append(newGenre)
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
			return True
		elif isinstance(remActor, str):
			for actor in self.movie_actors:
				if actor.actor_full_name == remActor:
					self.movie_actors.remove(actor)
					return True
		else:
			return False
			
	def remove_genre(self, remGenre):
		if remGenre in self.movie_genres:
			self.movie_genres.remove(remGenre)
			return True
		elif isinstance(remGenre, str):
			for genre in self.movie_genres:
				if genre.name == remGenre:
					self.movie_genres.remove(genre)
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