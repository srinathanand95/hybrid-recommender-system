import streamlit as st
from recommender import recommend

st.set_page_config(page_title="Movie Recommender", layout="centered")

st.title("🎬 Hybrid Movie Recommender")

movie_name = st.text_input("Enter a movie name")

if movie_name:
    recs = recommend(movie_name)

    if recs is not None and not recs.empty:
        for title, row in recs.iterrows():
            st.write(f"{title} (score: {row['score']:.3f})")
    else:
        st.write("No recommendations found.")