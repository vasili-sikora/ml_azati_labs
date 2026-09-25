def wins_correlation() -> str:
    """
    Return column with maximum correlation with number of wins
    """


def imdb_rating_by_time() -> tuple[str, int]:
    """
    Return tuple with trend ("ascending" or "descending") and start of 10 year period with maximum mean rating.
    """


def genre_ratings() -> tuple[str, str]:
    """
    Return tuple with 2 genres: genre with maximum median rating and genre with broadest IQR.
    """


def number_of_words_mode() -> int:
    """
    Return mode for number of words in movie title (as integer)
    """


def short_movie_year() -> int:
    """
    Return start of 10 year period with maximum share of short movies (< 1 hour)
    """


def movie_reviews() -> str:
    """
    Return most popular genre by user reviews. Think about the correct metric.
    """


if __name__ == "__main__":
    headers = "fn,tid,title,wordsInTitle,url,imdbRating,ratingCount,duration,year,type,nrOfWins,nrOfNominations,nrOfPhotos,nrOfNewsArticles,nrOfUserReviews,nrOfGenre,Action,Adult,Adventure,Animation,Biography,Comedy,Crime,Documentary,Drama,Family,Fantasy,FilmNoir,GameShow,History,Horror,Music,Musical,Mystery,News,RealityTV,Romance,SciFi,Short,Sport,TalkShow,Thriller,War,Western".split(
        ","
    )
    val = "titles01/tt0012349,tt0012349,Der Vagabund und das Kind (1921),der vagabund und das kind,http://www.imdb.com/title/tt0012349/,8.4,40550,3240,1921,video.movie,1,0,19,96,85,3,0,0,0,0,0,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0".split(
        ","
    )
    print(f"{len(headers) = },{len(val) = }", sep="\n")
