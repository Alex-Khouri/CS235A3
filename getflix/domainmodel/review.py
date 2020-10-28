from datetime import datetime


class Review:
	def __init__(self, arg_user=None, arg_user_code=None, arg_movie=None, arg_movie_code=None,
				 arg_text=None, arg_rating=None, arg_timestamp=None, arg_date=None, arg_code=None):
		self.review_user = arg_user
		self.review_user_code = self.review_user.code if arg_user_code is None else arg_user_code
		self.review_movie = arg_movie
		self.review_movie_code = self.review_movie.code if arg_movie_code is None else arg_movie_code
		self.review_text = arg_text.strip() if isinstance(arg_text, str) else None
		self.review_rating = arg_rating if (isinstance(arg_rating, int) and (arg_rating in range(1, 11))) else None
		self.review_timestamp = str(datetime.now()) if arg_timestamp is None else arg_timestamp
		self.review_date = self.review_timestamp.split(' ')[0] if arg_date is None else arg_date
		self.review_code = str(hash(self.review_user.username + self.review_movie.title + self.review_timestamp)) if arg_code is None else arg_code

	def __repr__(self):
		return f"<Review {self.review_movie}, {self.review_rating}, {self.review_timestamp}, '{self.review_text}'>"

	def __eq__(self, other):
		return self.review_movie == other.arg_movie and self.review_text == other.arg_text and self.review_rating == other.arg_rating and self.review_timestamp == other.revTimestamp

	@property
	def user(self):
		return self.review_user

	@property
	def user_code(self):
		return self.review_user_code

	@property
	def movie(self):
		return self.review_movie

	@property
	def movie_code(self):
		return self.review_movie_code

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
	def date(self):
		return self.review_date

	@property
	def code(self):
		return self.review_code

	@user.setter
	def user(self, newUser):
		self.review_user = newUser

	@user_code.setter
	def user_code(self, new):
		print("WARNING: Codes cannot be manually reassigned")

	@movie.setter
	def movie(self, newMovie):
		self.review_movie = newMovie

	@movie_code.setter
	def movie_code(self, new):
		print("WARNING: Codes cannot be manually reassigned")
	
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

	@date.setter
	def date(self, new):
		print("WARNING: Review dates cannot be manually reassigned")

	@code.setter
	def code(self, new):
		print("WARNING: Codes cannot be manually reassigned")


if __name__ == "__main__":
	from getflix.domainmodel.actor import Actor
	from getflix.domainmodel.director import Director
	from getflix.domainmodel.genre import Genre
	from getflix.domainmodel.movie import Movie
	from getflix.domainmodel.user import User
	from getflix.domainmodel.watchlist import Watchlist