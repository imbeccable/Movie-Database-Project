# File: main.py
#
# main
#
# Uses objecttier to output information regarding movies from
# the database based on inputed commands
# 
# Author:
#   Becca Nika
#   Project 02
#

import sqlite3
import objecttier

#
# Outputs the total number of movies and reviews in the database
#
def stats(dbConn):
  num_movies = objecttier.num_movies(dbConn)
  num_reviews = objecttier.num_reviews(dbConn)
  print("  # of movies:", f"{num_movies:,}")
  print("  # of reviews:", f"{num_reviews:,}") 
  return

#
# Uses inputed movie name, with or without wildcards, to
# output the associated movie’s ID, title, and year of release.
#
def commandOne(dbConn):
  try:
    # gets an inputed movie name
    movie_name = input("Enter movie name (wildcards _ and % supported): ")
    print()
  
    got_movies = objecttier.get_movies(dbConn, movie_name)
    print("# of movies found:", len(got_movies))
    print()

    # if there are too many movies in the list to display
    if len(got_movies) > 100:
      print("There are too many movies to display, please narrow your search and try again...")
      return

    # if the requested movie does not exist
    if len(got_movies) == 0:
      return

    # prints out the movies retrieved
    for m in got_movies:
        print(m.Movie_ID, ":", m.Title, f"({m.Release_Year})")
  
    return
  except Exception as err:
    print("commandOne error: ", err)
    return None
  finally:
    pass

#
# Uses inputed movie id to output detailed movie information about the 
# associated movie --- tagline, budget, revenue, genres, etc
#
def commandTwo(dbConn):
  try:
    # gets an inputed movie id
    movie_id = input("Enter movie id: ")
    print()
    # creates a MovieDetails object from the inputed movie id
    movie_details = objecttier.get_movie_details(dbConn, movie_id)

    # if the movie id does not exist
    if movie_details == None:
      print("No such movie...")
      return

    # prints out all the information gathered
    print(movie_details.Movie_ID, ":", movie_details.Title)
    print("  Release date:", movie_details.Release_Date)
    print("  Runtime:", movie_details.Runtime, "(mins)")
    print("  Orig language:", movie_details.Original_Language)
    print("  Budget:", f"${movie_details.Budget:,}", "(USD)")
    print("  Revenue:", f"${movie_details.Revenue:,}", "(USD)")
    print("  Num reviews:", movie_details.Num_Reviews)
    print("  Avg rating:", f"{movie_details.Avg_Rating:.2f}", "(0..10)")
    if len(movie_details.Genres) == 0:
      print("  Genres: ")
    else:
      print(f"  Genres: {', '.join(movie_details.Genres)}, ")
    if len(movie_details.Production_Companies) == 0:
      print("  Production companies: ")
    else:
      print(f"  Production companies: {', '.join(movie_details.Production_Companies)}, ")
    print("  Tagline:", movie_details.Tagline)
    
    return
  except Exception as err:
    print("commandTwo: ", err)
    return None
  finally:
    pass

#
# Output the top N movies based on their average rating
# with an inputed minimum number of reviews
#
def commandThree(dbConn):

  try:
    # gets an inputed N
    n = input("N? ")

    # if N is negative
    if int(n) < 1:
      print("Please enter a positive value for N...")
      return    

    # gets an inputed minimum number of reviews
    min = input("min number of reviews? ")

    # if the minimum number of reviews is negative
    if int(min) < 1:
      print("Please enter a positive value for min number of reviews...")
      return

    # gets the top N movies with the inputed N and minimum number of reviews
    movies = objecttier.get_top_N_movies(dbConn, int(n), int(min))
    print()

    # prints out the requested movies
    for m in movies:
      print(m.Movie_ID, ":", m.Title, f"({m.Release_Year}),", "avg rating =", f"{m.Avg_Rating:.2f}", f"({m.Num_Reviews}", "reviews)")
  
    return
  except Exception as err:
    print("commandThree error: ", err)
    return None
  finally:
    pass

#
# Inserts a new review into the database using inputed movie id
#
def commandFour(dbConn):
  try:
    # gets an inputed rating between 0 and 10
    rating = input("Enter rating (0..10): ")

    # if the rating is not valid (<0 or >10)
    if int(rating) < 0 or int(rating) > 10:
      print("Invalid rating...")
      return

    # gets an inputed movie id
    movie_id = input("Enter movie id: ")
    print()

    # adds the review to the specified movie id
    modified = objecttier.add_review(dbConn, movie_id, int(rating))
  
    # if movie does NOT exist
    if modified == 0:
      print("No such movie...")
      return
    # if movie DOES exist
    if modified > 0:
      print("Review successfully inserted")
  
    return
  except Exception as err:
    print("commandFour error: ", err)
    return None
  finally:
    pass

#
# Sets the tagline for a given movie, either by inserting (if not already there)
# or updating (if already there)
#
def commandFive(dbConn):
  try:
    # gets an inputed tagline
    tagline = input("tagline? ")

    # gets an inputed movie id
    movie_id = input("movie id? ")
    print()

    # sets the inputed tagline to the specified movie id
    modified = objecttier.set_tagline(dbConn, movie_id, tagline)

    # if the movie does NOT exist
    if modified == 0:
      print("No such movie...")
      return
    # if the movie DOES exist
    if modified > 0:
      print("Tagline successfully set")
  
    return
  except Exception as err:
    print("commandFive error: ", err)
    return None
  finally:
    pass
    
def main():
  print('** Welcome to the MovieLens app **')

  # connect to the database
  dbConn = sqlite3.connect('MovieLens.db')
  
  print()

  # prints some general stats
  print("General stats:")
  stats(dbConn)

  print()

  # begins command inputs
  cmd = input("Please enter a command (1-5, x to exit): ")

  # while user wants to request information
  while cmd != "x":
    print()
    # outputs movie id, title, and release year based on inputed movie name
    if cmd == "1": 
      commandOne(dbConn)
    # outputs all movie details based on an inputed movie id
    elif cmd == "2":
      commandTwo(dbConn)
    # outputs the top (inputed) N movies based on inputed minimum reviews
    elif cmd == "3":
      commandThree(dbConn)
    # inserts a new review into the system using an inputed movie id
    elif cmd == "4":
      commandFour(dbConn)
    # sets a tagline to an inputed movie id
    elif cmd == "5":
      commandFive(dbConn)
    else:
      print("**Error, unknown command, try again...")

    print()
    cmd = input("Please enter a command (1-5, x to exit): ")
  
  dbConn.close()

if __name__ == '__main__':
  main()