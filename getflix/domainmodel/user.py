from getflix.domainmodel.watchlist import Watchlist


class User:
	def __init__(self, arg_username=None, arg_password=None, arg_watched=list(), arg_reviews=list(),
				 arg_review_codes="", arg_timewatching=0, arg_watchlist=None, arg_watchlist_code=None,
				 arg_code=None):
		self.user_username = arg_username.strip().lower() if isinstance(arg_username, str) else None
		self.user_password = arg_password if isinstance(arg_password, str) else None
		self.user_watched = arg_watched
		self.user_reviews = arg_reviews
		self.user_review_codes = arg_review_codes
		self.user_timewatching = arg_timewatching
		self.user_watchlist = Watchlist(self.user_code) if arg_watchlist is None else arg_watchlist
		self.user_watchlist_code = self.user_watchlist.code if arg_watchlist_code is None else arg_watchlist_code
		self.user_code = str(hash(self.user_username)) if arg_code is None else arg_code

	def __repr__(self):
		return f"<User {self.user_username}>"

	def __eq__(self, other):
		return self.user_username == other.username

	def __lt__(self, other):
		return self.user_username < other.username

	def __hash__(self):
		return hash(self.user_username)

	@property
	def username(self):
		return self.user_username

	@property
	def password(self):
		return self.user_password

	@property
	def watched_movies(self):
		return self.user_watched

	@property
	def reviews(self):
		return self.user_reviews

	@property
	def review_codes(self):
		return self.user_review_codes

	@property
	def time_spent_watching_movies_minutes(self):
		return self.user_timewatching

	@property
	def watchlist(self):
		return self.user_watchlist

	@property
	def watchlist_code(self):
		return self.user_watchlist_code

	@property
	def code(self):
		return self.user_code

	@username.setter
	def username(self, newName):
		if isinstance(newName, str):
			self.user_username = newName.strip().lower()

	@password.setter
	def password(self, newPassword):
		if isinstance(newPassword, str):
			self.user_password = newPassword

	@watched_movies.setter
	def watched_movies(self, newWatched):
		if isinstance(newWatched, list):
			self.user_watched = newWatched

	@reviews.setter
	def reviews(self, newReviews):
		if isinstance(newReviews, list):
			self.user_reviews = newReviews

	@review_codes.setter
	def review_codes(self, new):
		print("WARNING: Codes cannot be manually reassigned")

	@time_spent_watching_movies_minutes.setter
	def time_spent_watching_movies_minutes(self, newTimeWatching):
		if isinstance(newTimeWatching, int):
			self.user_timewatching = newTimeWatching

	@watchlist.setter
	def watchlist(self, newWatchlist):
		self.user_watchlist = newWatchlist
		self.user_watchlist_code = self.user_watchlist.code

	@watchlist_code.setter
	def watchlist_code(self, new):
		print("WARNING: Codes cannot be manually reassigned")

	@code.setter
	def code(self, new):
		print("WARNING: Codes cannot be manually reassigned")

	def watch_movie(self, movie):
		if not movie in self.user_watched:
			self.user_watched.append(movie)
		self.user_timewatching += movie.runtime_minutes
		if movie in self.user_watchlist:
			self.user_watchlist.remove_movie(movie)

	def add_review(self, review):
		self.user_reviews.append(review)
		self.user_review_codes = ",".join([review.code for review in self.user_reviews])

	def remove_review(self, review):
		self.user_reviews.remove(review)
		self.user_review_codes = ",".join([review.code for review in self.user_reviews])


if __name__ == "__main__":
	from getflix.domainmodel.actor import Actor
	from getflix.domainmodel.director import Director
	from getflix.domainmodel.genre import Genre
	from getflix.domainmodel.movie import Movie
	from getflix.domainmodel.review import Review