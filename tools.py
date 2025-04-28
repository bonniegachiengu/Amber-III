from data import movies, watchlists


def rank_directors(movies: list) -> list[tuple[str, int]]:
    """
    Rank movie directors based on the ranks of their movies
    :param movies: list of movies
    :return: list of tuples (director, average_rank) sorted by average rank in descending order
    """
    directors = {}
    for movie in movies:
        for director in movie["directors"]:
            if director not in directors:
                directors[director] = []
            directors[director].append(movie["ranking"])
    ranked_directors = {k: round(sum(v) / len(v)) for k, v in directors.items()}
    return sorted(ranked_directors.items(), key=lambda x: x[1], reverse=True)


def similar_movies(genres: list, movies: list) -> list[dict]:
    """
    6 films with two or more genres as a given film's genre in decending order say starting with the most similar
    :param genres: list of genres
    :param movies: list of movies
    :return: list of movies with the same genres as the given movie
    """
    similar = []
    for movie in movies:
        if len(set(movie["genres"]) & set(genres)) >= 2:
            similar.append(movie)
    return sorted(similar, key=lambda x: x["ranking"], reverse=True)


def similar_watchlists(genres: list, watchlists: list) -> list[dict]:
    """_summary_

    Args:
        genres (list): genres for the watchlist in question
        watchlists (list): list of all watchlists

    Returns:
        list[dict]: a filtered list of watchlists with similar genres
    """
    similar = []
    for watchlist in watchlists:
        if len(set(watchlist["genres"]) & set(genres)) >= 2:
            similar.append(watchlist)
    return sorted(similar, key=lambda x: x["id"], reverse=True)


def get_watchlists(movie: dict, watchlists: list) -> list[dict]:
    """
    Get the watchlists in the movies album_id field with a list of watchlist ids

    Args:
        movie (dict): movie dictionary containing movie details
        watchlists (list): list of watchlists containing watchlist details

    Returns:
        list[dict]: a list of watchlists with the same album_id as the given movie
    """
    return [watchlist for watchlist in watchlists if watchlist["id"] in movie["album_ids"]]


def get_album_movies(watchlist: dict, movies: list) -> list[dict]:
    """
    Get the movies in the watchlists album_id field with a list of movie ids.

    Args:
        watchlist (dict): watchlist dictionary containing watchlist details
        movies (list): list of movies containing movie details

    Returns:
        list[dict]: a list of movies with the same album_id as the given watchlist
    """
    return [movie for movie in movies if movie["id"] in watchlist["film_ids"]]


def get_actor_films(actor: dict, movies: list) -> list[dict]:
    """
    Get the movies in the actor movies field with a list of movie ids.

    :param actor: actor dictionary containing actor details
    :param movies: list of movies containing movie details
    :return: list of movies with the same actor in the actor films field
    """
    return [movie for movie in movies if movie["id"] in actor["movies"]]


def get_actor_watchlists(actor: dict, watchlists: list) -> list[dict]:
    """
    Get the watchlists in the actor watchlists field with a list of watchlist ids.

    :param actor: actor dictionary containing actor details
    :param watchlists: list of watchlists containing watchlist details
    :return: list of watchlists with the same actor in the actor watchlists field
    """
    return [watchlist for watchlist in watchlists if watchlist["id"] in actor["watchlists"]]


if __name__ == "__main__":
    # print(rank_directors(movies))
    # print(get_watchlists(movies[0], watchlists))
    print(get_watchlists())
