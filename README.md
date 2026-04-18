# Hybrid Recommender System

This project implements a hybrid recommendation system that combines collaborative filtering and content-based filtering to improve recommendation quality while reducing popularity bias.

## Overview

Recommendation systems often over-index on popular items or fail to capture meaningful similarity between items. This system is designed to balance:

- User behavior (collaborative filtering)
- Item similarity (content-based filtering using genres)
- Popularity normalization to prevent dominance of highly-rated items

## Model Design

The system combines:

- **Collaborative Filtering**: Pearson correlation between user rating vectors
- **Content-Based Filtering**: Cosine similarity over genre vectors
- **Hybrid Scoring**: Nonlinear combination of both signals
- **Popularity Adjustment**: Log-scaled weighting to reduce popularity bias

Final score:

score = collab^0.8 × content^0.6 × popularity_weight

## Example

Input: Toy Story

Output:
- Lion King
- Aladdin
- Beauty and the Beast

## Key Design Decisions

- Combined collaborative and content signals to address cold-start and sparsity issues  
- Applied genre constraints to improve recommendation relevance  
- Introduced popularity normalization to reduce bias toward widely rated items  
- Used non-linear scoring to better balance competing signals 

## Evaluation

We evaluate the recommender using Precision@10.

- Relevant items are movies rated ≥ 4 by the user
- For each user, one liked movie is held out
- The model is tested on its ability to recover other liked items

**Result:**
Precision@10 = 0.358

## Interpretation

- This score indicates strong alignment between recommendations and user preferences
- The hybrid model effectively balances collaborative filtering (user behavior) and content-based filtering (genre similarity)
- Popularity normalization helps reduce bias toward frequently rated movies

## How to Run

```bash
pip install -r requirements.txt
python3 recommender.py

## Live Demo

https://hybrid-recommender-system-us3dqb3qqk8icz63ecykwh.streamlit.app/
