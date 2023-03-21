# File: objecttier.py
#
# objecttier
#
# Builds Movie-related objects from data retrieved through 
# the data tier.
#
# Original author:
#   Prof. Joe Hummel
#   U. of Illinois, Chicago
#   CS 341, Spring 2022
#   Project #02
#
# Modified by:
#   Becca Nika
#   UIN: 670872082
#   NetID: rnika3
#
import datatier


##################################################################
#
# Movie:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#
class Movie:

  def __init__ (self, id, title, year):
    self._Movie_ID = id
    self._Title = title
    self._Release_Year = year
  
  @property
  def Movie_ID(self):
    return self._Movie_ID

  @property
  def Title(self):
    return self._Title

  @property
  def Release_Year(self):
    return self._Release_Year

  


##################################################################
#
# MovieRating:
#
# Child class of Movie
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#   Num_Reviews: int
#   Avg_Rating: float
#
class MovieRating(Movie):

  def __init__(self, id, title, year, reviews, ratings):
    super().__init__(id, title, year)
    self._Num_Reviews = reviews
    self._Avg_Rating = ratings

  @property
  def Num_Reviews(self):
    return self._Num_Reviews

  @property
  def Avg_Rating(self):
    return self._Avg_Rating
  

##################################################################
#
# MovieDetails:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Date: string, date only (no time)
#   Runtime: int (minutes)
#   Original_Language: string
#   Budget: int (USD)
#   Revenue: int (USD)
#   Num_Reviews: int
#   Avg_Rating: float
#   Tagline: string
#   Genres: list of string
#   Production_Companies: list of string
#
class MovieDetails:

  def __init__(self, id, title, date, runtime, og_lan, budget, rev, reviews, ratings, tagline, genres, comp):
    self._Movie_ID = id
    self._Title = title
    self._Release_Date = date
    self._Runtime = runtime
    self._Original_Language = og_lan
    self._Budget = budget
    self._Revenue = rev
    self._Num_Reviews = reviews
    self._Avg_Ratings = ratings
    self._Tagline = tagline
    self._Genres = genres
    self._Production_Companies = comp

  @property
  def Movie_ID(self):
    return self._Movie_ID

  @property
  def Title(self):
    return self._Title

  @property
  def Release_Date(self):
    return self._Release_Date

  @property
  def Runtime(self):
    return self._Runtime

  @property
  def Original_Language(self):
    return self._Original_Language

  @property
  def Budget(self):
    return self._Budget

  @property
  def Revenue(self):
    return self._Revenue

  @property
  def Num_Reviews(self):
    return self._Num_Reviews

  @property
  def Avg_Rating(self):
    return self._Avg_Ratings

  @property
  def Tagline(self):
    return self._Tagline

  @property
  def Genres(self):
    return self._Genres

  @property
  def Production_Companies(self):
    return self._Production_Companies


##################################################################
# 
# num_movies:
#
# Returns: # of movies in the database; if an error returns -1
#
def num_movies(dbConn):

  try: 
    query = "SELECT COUNT(Movie_ID) FROM Movies;"
    num = datatier.select_one_row(dbConn, query)
    return num[0]   
  except Exception as err:
    print("num_movies error: ", err)
    return -1
  finally:
    pass


##################################################################
# 
# num_reviews:
#
# Returns: # of reviews in the database; if an error returns -1
#
def num_reviews(dbConn):

  try: 
    query = "SELECT COUNT(Rating) FROM Ratings;"
    num = datatier.select_one_row(dbConn, query)
    return num[0]
  except Exception as err:
    print("num_reviews error: ", err)
    return -1
  finally:
    pass

##################################################################
#
# get_movies:
#
# gets and returns all movies whose name are "like"
# the pattern. Patterns are based on SQL, which allow
# the _ and % wildcards. Pass "%" to get all stations.
#
# Returns: list of movies in ascending order by movie_id; 
#          an empty list means the query did not retrieve
#          any data (or an internal error occurred, in
#          which case an error msg is already output).
#
def get_movies(dbConn, pattern):

  try: 
    # selects id, title, and release year from a movie with a title
    # similar to the inputed pattern
    query = f"SELECT Movie_ID, Title, strftime('%Y',Release_Date) FROM Movies WHERE Title LIKE '{pattern}' GROUP BY Movie_ID ORDER BY Movie_ID ASC;"
    rows = datatier.select_n_rows(dbConn, query)
    movies = []
    
    # if there does NOT exist a movie like the pattern
    if rows == None:
      return movies
    # if there DOES exist a movie like the pattern
    for r in rows:
      movies.append(Movie(r[0],r[1],r[2]))
    return movies
  except Exception as err:
    print("get_movies error: ", err)
    return None
  finally:
    pass


##################################################################
#
# get_movie_details:
#
# gets and returns details about the given movie; you pass
# the movie id, function returns a MovieDetails object. Returns
# None if no movie was found with this id.
#
# Returns: if the search was successful, a MovieDetails obj
#          is returned. If the search did not find a matching
#          movie, None is returned; note that None is also 
#          returned if an internal error occurred (in which
#          case an error msg is already output).
#
def get_movie_details(dbConn, movie_id):
  
  try: 
    # selects the id, title, release date, runtime, original language,
    # budget, and revenue of a movie with the inputed id
    q1 = f"SELECT Movies.Movie_ID, Movies.Title, strftime('%Y-%m-%d',Movies.Release_Date), Movies.Runtime, Movies.Original_Language, Movies.Budget, Movies.Revenue FROM Movies WHERE Movie_ID = {movie_id};"
    # gets the average rating of the movie with the inputed id
    q2 = f"SELECT AVG(Rating) FROM Ratings WHERE Movie_ID = {movie_id};"
    # gets the tagline of the movie with the inputed id
    q3 = f"SELECT Tagline FROM Movie_Taglines WHERE Movie_ID = {movie_id};"
    # gets the genres of the movie with the inputed id
    q4 = f"SELECT Genres.Genre_Name FROM Genres INNER JOIN Movie_Genres ON Genres.Genre_ID = Movie_Genres.Genre_ID WHERE Movie_Genres.Movie_ID = {movie_id} GROUP BY Genre_Name ORDER BY Genre_Name ASC;"
    # gets the production companies of the movie with the inputed id
    q5 = f"SELECT Company_Name FROM Companies INNER JOIN Movie_Production_Companies ON Companies.Company_ID = Movie_Production_Companies.Company_ID WHERE Movie_Production_Companies.Movie_ID = {movie_id} GROUP BY Company_Name ORDER BY Company_Name ASC;"
    # gets the total number of ratings of the movie with the inputed id
    q6 = f"SELECT COUNT(Rating) FROM Ratings WHERE Movie_ID = {movie_id};"
    
    details = datatier.select_n_rows(dbConn, q1)
    # if movie does not exist
    if len(details) == 0:
      return None
      
    avg_ratings = datatier.select_one_row(dbConn, q2) 
    # if there are no ratings
    if avg_ratings[0] == None:
      avg_ratings = (0,)
    
    tagline = datatier.select_one_row(dbConn, q3)
    # if movie does not have a tagline
    if len(tagline) == 0:
      tagline = ("",)

    genres = []
    companies = []
    
    gens = datatier.select_n_rows(dbConn, q4)
    
    comps = datatier.select_n_rows(dbConn, q5)
    
    count_ratings = datatier.select_one_row(dbConn, q6)


    # creating genres list
    for g in gens:
      genres.append(g[0])

    # creating production companies list
    for c in comps:
      companies.append(c[0])

    # creating MovieDetails object
    for d in details:
      movie_details_obj = MovieDetails(d[0], d[1], d[2], d[3], d[4], d[5], d[6], count_ratings[0], avg_ratings[0], tagline[0], genres, companies)
      
    return movie_details_obj      
  except Exception as err:
    print("get_movie_details error: ", err)
    return None
  finally:
    pass
         

##################################################################
#
# get_top_N_movies:
#
# gets and returns the top N movies based on their average 
# rating, where each movie has at least the specified # of
# reviews. Example: pass (10, 100) to get the top 10 movies
# with at least 100 reviews.
#
# Returns: returns a list of 0 or more MovieRating objects;
#          the list could be empty if the min # of reviews
#          is too high. An empty list is also returned if
#          an internal error occurs (in which case an error 
#          msg is already output).
#
def get_top_N_movies(dbConn, N, min_num_reviews):

  try:
    # selects the id, title, release year, total ratings, and average rating of
    # N movies with a min_num_reviews amount of reviews or more
    query = f"SELECT Movies.Movie_ID, Movies.Title, strftime('%Y',Movies.Release_Date), COUNT(Ratings.Rating) as total_ratings, AVG(Ratings.Rating) as avg_rating FROM Movies INNER JOIN Ratings ON Movies.Movie_ID = Ratings.Movie_ID GROUP BY Movies.Movie_ID HAVING total_ratings >= {min_num_reviews} ORDER BY avg_rating DESC LIMIT {N};"

    info = datatier.select_n_rows(dbConn, query)
    top_movies = []
    
    # if there does NOT exist movies with reviews >= min_num_reviews
    if info == None:
      return top_movies
      
    # creating list of MovieRating objects
    for i in info:
      top_movies.append(MovieRating(i[0],i[1],i[2],i[3],i[4]))
      
    return top_movies
  except Exception as err:
    print("get_top_N_movies error: ", err)
    return None
  finally:
    pass


##################################################################
#
# add_review:
#
# Inserts the given review --- a rating value 0..10 --- into
# the database for the given movie. It is considered an error
# if the movie does not exist (see below), and the review is
# not inserted.
#
# Returns: 1 if the review was successfully added, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def add_review(dbConn, movie_id, rating):

  try: 
    # for checking if movie exists
    q = f"SELECT Movie_ID FROM Movies WHERE Movie_ID ={movie_id};"
    valid = datatier.select_one_row(dbConn, q)
    #for inserting review if movie id is valid
    query = f"INSERT INTO Ratings(Movie_ID, Rating) VALUES({movie_id}, {rating});"
    #if movie is valid
    if len(valid) != 0:
      datatier.perform_action(dbConn, query)
      return 1
    else:
      return 0
  except Exception as err:
    print("add_reviews error: ", err)
    return 0
  finally:
    pass


##################################################################
#
# set_tagline:
#
# Sets the tagline --- summary --- for the given movie. If
# the movie already has a tagline, it will be replaced by
# this new value. Passing a tagline of "" effectively 
# deletes the existing tagline. It is considered an error
# if the movie does not exist (see below), and the tagline
# is not set.
#
# Returns: 1 if the tagline was successfully set, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def set_tagline(dbConn, movie_id, tagline):

  try: 
    # to check if tagline exists
    q1 = f"SELECT Tagline FROM Movie_Taglines WHERE Movie_ID = {movie_id}"
    # to check if movie exists
    q2 = f"SELECT Movie_ID FROM Movies WHERE Movie_ID = {movie_id}"
    # to insert tagline if movie does NOT have one
    q3 = f"INSERT INTO Movie_Taglines(Movie_ID, Tagline) VALUES({movie_id}, '{tagline}');"
    # to update tagline if movie DOES have one
    q4 = f"UPDATE Movie_Taglines SET Tagline = '{tagline}' WHERE Movie_ID = {movie_id};"
    
    tag = datatier.select_one_row(dbConn, q1)
    valid = datatier.select_one_row(dbConn, q2)

    # peform insert if tagline does not exist
    if len(tag) == 0 and len(valid) != 0:
      datatier.perform_action(dbConn, q3)
      return 1
    # perform update if tagline does exist
    elif len(tag) == 1 and len(valid) != 0:
      datatier.perform_action(dbConn, q4)
      return 1
    else:
      return 0
  except Exception as err:
    print("set_tagline error: ", err)
    return 0
  finally:
    pass
