import pandas as pd
import numpy as np
from rapidfuzz import process, fuzz
from sklearn.metrics.pairwise import cosine_similarity

ratings = pd.read_csv(
    "data/ratings.csv",
    sep="\t",
    names=["user_id", "movie_id", "rating", "timestamp"]
)

movies = pd.read_csv(
    "data/movies.csv",
    sep="|",
    encoding="latin-1",
    names=[
        "movie_id", "title", "release_date", "video_release_date", "IMDb_URL",
        "unknown", "Action", "Adventure", "Animation", "Children's", "Comedy",
        "Crime", "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror",
        "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"
    ]
)

df = pd.merge(ratings, movies, on="movie_id")

movie_matrix = df.pivot_table(index="user_id", columns="title", values="rating")

all_titles = movie_matrix.columns.tolist()

genre_cols = movies.columns[5:]
genre_matrix = movies.set_index("title")[genre_cols]

content_sim = cosine_similarity(genre_matrix)
content_sim_df = pd.DataFrame(
    content_sim,
    index=genre_matrix.index,
    columns=genre_matrix.index
)

def find_best_match(query):
    match, score, _ = process.extractOne(query, all_titles, scorer=fuzz.WRatio)
    return match if score > 60 else None

def recommend(movie_name, top_n=10):
    best_match = find_best_match(movie_name)

    if not best_match:
        return None

    movie_ratings = movie_matrix[best_match]
    collab_sim = movie_matrix.corrwith(movie_ratings).dropna()
    collab_df = pd.DataFrame(collab_sim, columns=["collab_score"])

    if best_match in content_sim_df.index:
        content_scores = content_sim_df[best_match]
        content_df = pd.DataFrame(content_scores, columns=["content_score"])
    else:
        content_df = pd.DataFrame()

    combined = collab_df.join(content_df, how="inner")

    ratings_count = df.groupby("title")["rating"].count()
    combined["num_ratings"] = ratings_count

    combined = combined.drop(best_match, errors="ignore")
    combined = combined.fillna(0)

    combined["collab_score"] = (combined["collab_score"] + 1) / 2
    combined["content_score"] = (combined["content_score"] + 1) / 2

    combined = combined[combined["content_score"] > 0.2]

    target_genres = genre_matrix.loc[best_match]
    overlap = genre_matrix.dot(target_genres)
    overlap = overlap[~overlap.index.duplicated(keep="first")]

    combined["genre_overlap"] = combined.index.map(overlap).fillna(0)
    combined = combined[combined["genre_overlap"] > 0]

    combined["score"] = (
        (combined["collab_score"] ** 0.8) *
        (combined["content_score"] ** 0.6)
    )

    combined["popularity"] = np.log1p(combined["num_ratings"])
    combined["score"] *= combined["popularity"] / combined["popularity"].max()

    combined = combined[combined["num_ratings"] > 50]

    recommendations = combined.sort_values(by="score", ascending=False)

    return recommendations.head(top_n)

if __name__ == "__main__":
    while True:
        movie_name = input("\nEnter a movie (or 'exit'): ")

        if movie_name.lower() == "exit":
            break

        recs = recommend(movie_name)

        if recs is not None:
            print("\nTop recommendations:\n")
            for title, row in recs.iterrows():
                print(title)