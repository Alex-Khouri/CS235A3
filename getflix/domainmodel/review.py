from datetime import datetime


class Review:
	def __init__(self, revUser, revMovie, revText, revRating):
		self.review_user = revUser
		self.review_movie = revMovie
		self.review_text = revText.strip() if isinstance(revText, str) else None
		self.review_rating = revRating if (isinstance(revRating, int) and (revRating in range(1, 11))) else None
		self.review_timestamp = datetime.now()
		self.review_date = str(self.review_timestamp).split(' ')[0]

	def __repr__(self):
		return f"<Review {self.review_movie}, {self.review_rating}, {self.review_timestamp}, '{self.review_text}'>"

	def __eq__(self, other):
		return self.review_movie == other.revMovie and self.review_text == other.revText and self.review_rating == other.revRating and self.review_timestamp == other.revTimestamp

	@property
	def movie(self):
		return self.review_movie

	@property
	def text(self):
		return self.review_text

	@property
	def rating(self):
		return self.review_rating

	@property
	def timestamp(self):
		return self.review_timestamp

	@property
	def user(self):
		return self.review_user

	@property
	def date(self):
		return self.review_date

	@movie.setter
	def movie(self, newMovie):
		self.review_movie = newMovie
	
	@text.setter
	def text(self, newText):
		if isinstance(newText, str):
			self.review_text = newText.strip()

	@rating.setter
	def rating(self, newRating):
		if isinstance(newRating, int) and newRating in range(1, 11):
			self.review_text = newRating

	@timestamp.setter
	def timestamp(self, newTimestamp):
		if isinstance(newTimestamp, datetime.datetime):
			self.review_timestamp = newTimestamp

	@user.setter
	def user(self, newUser):
		self.review_user = newUser

	@date.setter
	def date(self, newDate):
		self.review_date = self.review_date  # This value should never be manually changed
		print("WARNING: Review dates cannot be manually reassigned")


if __name__ == "__main__":
	from getflix.domainmodel.actor import Actor
	from getflix.domainmodel.director import Director
	from getflix.domainmodel.genre import Genre
	from getflix.domainmodel.movie import Movie
	from getflix.domainmodel.user import User
	from getflix.domainmodel.watchlist import Watchlist