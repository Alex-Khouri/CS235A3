import csv

from getflix.domainmodel.actor import Actor
from getflix.domainmodel.director import Director
from getflix.domainmodel.genre import Genre
from getflix.domainmodel.movie import Movie


class MovieFileCSVReader:
	def __init__(self, file_name):
		self.file_name = file_name if isinstance(file_name, str) else None
		self.movies = list()
		self.actors = set()
		self.directors = set()
		self.genres = set()

	@property
	def dataset_of_movies(self):
		return self.movies

	@property
	def dataset_of_actors(self):
		return self.actors

	@property
	def dataset_of_directors(self):
		return self.directors

	@property
	def dataset_of_genres(self):
		return self.genres

	@dataset_of_movies.setter
	def dataset_of_movies(self, newMovies):
		if isinstance(newMovies, list):
			self.movies = newMovies

	@dataset_of_actors.setter
	def dataset_of_actors(self, newActors):
		if isinstance(newActors, set):
			self.actors = newActors

	@dataset_of_directors.setter
	def dataset_of_directors(self, newDirectors):
		if isinstance(newDirectors, set):
			self.directors = newDirectors

	@dataset_of_genres.setter
	def dataset_of_genres(self, newGenres):
		if isinstance(newGenres, set):
			self.genres = newGenres

	def read_csv_file(self):
		try:
			csvfile = open(self.file_name, encoding='utf-8-sig', newline='')
			reader = csv.DictReader(csvfile)
			for row in reader:
				try:
					movie = Movie(row['Title'].strip(), int(row['Year'].strip()))
					movie.description = row['Description']
					director = Director(row['Director'].strip())
					movie.director = director
					director.add_movie(movie)
					actors = {Actor(actor.strip()) for actor in row['Actors'].split(",")}
					for actor in actors:
						movie.add_actor(actor)
						actor.add_movie(movie)
					genres = {Genre(genre.strip()) for genre in row['Genre'].split(",")}
					for genre in genres:
						movie.add_genre(genre)
						genre.add_movie(movie)
					movie.runtime_minutes = int(row['Runtime (Minutes)'])
					movie.rating = float(row['Rating'])
					movie.votes = int(row['Votes'])
					self.movies.append(movie)
					self.actors.update(set(actors))
					self.directors.add(director)
					self.genres.update(set(genres))
				except:
					continue  # Skips movies with invalid formatting
			csvfile.close()
		except:
			raise Exception("Error while reading CSV file!")


if __name__ == "__main__":
	from getflix.domainmodel.review import Review
	from getflix.domainmodel.user import User
	from getflix.domainmodel.watchlist import Watchlist