import csv

from getflix.domainmodel.actor import Actor
from getflix.domainmodel.director import Director
from getflix.domainmodel.genre import Genre
from getflix.domainmodel.movie import Movie


class MovieFileCSVReader:
	def __init__(self, file_name):
		self.file_name = file_name if isinstance(file_name, str) else None
		self.reader_movies = list()
		self.reader_actors = set()
		self.reader_directors = set()
		self.reader_genres = set()

	@property
	def dataset_of_movies(self):
		return self.reader_movies

	@property
	def dataset_of_actors(self):
		return self.reader_actors

	@property
	def dataset_of_directors(self):
		return self.reader_directors

	@property
	def dataset_of_genres(self):
		return self.reader_genres

	@dataset_of_movies.setter
	def dataset_of_movies(self, newMovies):
		if isinstance(newMovies, list):
			self.reader_movies = newMovies

	@dataset_of_actors.setter
	def dataset_of_actors(self, newActors):
		if isinstance(newActors, set):
			self.reader_actors = newActors

	@dataset_of_directors.setter
	def dataset_of_directors(self, newDirectors):
		if isinstance(newDirectors, set):
			self.reader_directors = newDirectors

	@dataset_of_genres.setter
	def dataset_of_genres(self, newGenres):
		if isinstance(newGenres, set):
			self.reader_genres = newGenres

	def get_actor(self, name):
		for actor in self.reader_actors:
			if actor.actor_full_name == name:
				return actor
		return Actor(arg_name=name)

	def get_director(self, name):
		for director in self.reader_directors:
			if director.director_full_name == name:
				return director
		return Director(arg_name=name)

	def get_genre(self, name):
		for genre in self.reader_genres:
			if genre.name == name:
				return genre
		return Genre(arg_name=name)

	def read_csv_file(self):
		try:
			print("PROCESSING CSV FILE...")
			csvfile = open(self.file_name, encoding='utf-8-sig', newline='')
			reader = csv.DictReader(csvfile)
			for row in reader:
				# STEP ONE: Create and store isolated object references
				movie = Movie(arg_title=row['Title'].strip(), arg_year=int(row['Year'].strip()),
							  arg_description=row['Description'].replace("\"", "'"),
							  arg_runtime_minutes=int(row['Runtime (Minutes)']),
							  arg_rating=float(row['Rating']), arg_votes=int(row['Votes']))
				director = self.get_director(row['Director'].strip())
				actors = [self.get_actor(actor.strip()) for actor in row['Actors'].split(",")]
				genres = [self.get_genre(genre.strip()) for genre in row['Genre'].split(",")]

				# STEP TWO: Populate object relationships
				director.add_movie(movie)
				movie.add_director(director)
				for actor in actors:
					actor.add_movie(movie)
					movie.add_actor(actor)
					for other_actor in actors:
						if other_actor is not actor:
							actor.add_actor_colleague(other_actor)
				for genre in genres:
					genre.add_movie(movie)
					movie.add_genre(genre)

				self.reader_movies.append(movie)
				self.reader_directors.add(director)
				self.reader_actors.update(set(actors))
				self.reader_genres.update(set(genres))

				if int(row['Rank']) < 5:  # DEBUGGING
					print(f"\nLine: {row['Rank']}\nDirector: {director.director_full_name}\n"
						  f"Movies: {director.movies}")
					for mov in self.reader_movies:
						print(f"Movie: {mov.title}\nDirector: {mov.director.director_full_name}\nActors: {mov.actors}\nGenres: {mov.genres}")
						print("---")
					print("----------")

			csvfile.close()
			print("CSV FILE PROCESSED")
		except Exception as err:
			raise Exception(f"Error while reading CSV file:\n{err}")


if __name__ == "__main__":
	from getflix.domainmodel.review import Review
	from getflix.domainmodel.user import User
	from getflix.domainmodel.watchlist import Watchlist