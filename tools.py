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


def get_watchlists(movie: dict, watchlists: list) -> list[dict]:
    """
    Get the watchlists in the movies album_id field with a list of watchlist ids

    Args:
        movie (dict): movie dictionary containing movie details
        watchlists (list): list of watchlists containing watchlist details

    Returns:
        list[dict]: _description_
    """
    print(movie)
    return [watchlist for watchlist in watchlists if watchlist["id"] in movie["album_ids"]]


if __name__ == "__main__":
    # print(rank_directors(movies))
    
    print(get_watchlists(movies[0], watchlists))