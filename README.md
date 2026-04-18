# Hybrid Recommender System

This project implements a hybrid recommendation system that combines collaborative filtering and content-based filtering to improve recommendation quality while reducing popularity bias.

## Overview

Recommendation systems often over-index on popular items or fail to capture meaningful similarity between items. This system is designed to balance:

- User behavior (collaborative filtering)
- Item similarity (content-based filtering using genres)
- Popularity normalization to prevent dominance of highly-rated items

## Features

- Hybrid recommendation model (collaborative + content-based)
- Fuzzy search for flexible user input
- Genre-based filtering to enforce relevance
- Non-linear ranking function for improved scoring
- Popularity-adjusted scoring using log normalization

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

## How to Run

```bash
pip install -r requirements.txt
python3 recommender.py
