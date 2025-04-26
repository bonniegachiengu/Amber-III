from data import movies, watchlists


# rank movie directors based on the ranks of their movies
# since directors is a list of director names in each movie, we need to flatten it
# and then rank the directors based on the ranks of their movies as per stated in ranking key in the movie dict
def rank_directors(movies):
    directors = {}
    for movie in movies:
        for director in movie["directors"]:
            if director not in directors:
                directors[director] = []
            directors[director].append(movie["ranking"])
    ranked_directors = {k: round(sum(v) / len(v)) for k, v in directors.items()}
    return sorted(ranked_directors.items(), key=lambda x: x[1], reverse=True)



if __name__ == "__main__":
    print(rank_directors(movies))