import streamlit as st
from recommender import recommend

st.set_page_config(page_title="Movie Recommender", layout="centered")

st.title("🎬 Hybrid Movie Recommender")

st.write(
    "Get movie recommendations using a hybrid system combining collaborative filtering and content-based filtering."
)

movie_name = st.text_input("Enter a movie name")

def clean_title(title):
    return title.rsplit("(", 1)[0].strip()

def make_imdb_url(title):
    clean = clean_title(title)
    query = clean.replace(" ", "+")
    return f"https://www.imdb.com/find?q={query}"

if movie_name:
    recs = recommend(movie_name)

    if recs is not None and not recs.empty:
        st.subheader("Top Recommendations")
        st.caption("Click a title to search on IMDb")

        for title, row in recs.iterrows():
            clean = clean_title(title)
            imdb_url = make_imdb_url(title)

            st.markdown(f"[{clean}]({imdb_url})  \nScore: {row['score']:.3f}")
    else:
        st.write("No recommendations found.")