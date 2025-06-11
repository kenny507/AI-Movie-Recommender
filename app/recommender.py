import pandas as pd
import warnings

warnings.filterwarnings('ignore', category=RuntimeWarning)

ratings = pd.read_csv("data/ml-latest-small/ratings.csv")
movies = pd.read_csv("data/ml-latest-small/movies.csv")
data = pd.merge(ratings, movies, on="movieId")
movie_matrix = data.pivot_table(index='userId', columns='title', values='rating')

def get_recommendations(movie_title, data, min_ratings=35):
    movie_matrix = data.pivot_table(index='userId', columns='title', values='rating')
    if movie_title not in movie_matrix.columns:
        return []
    movie_ratings = movie_matrix[movie_title]
    similar_movies = movie_matrix.corrwith(movie_ratings)
    corr_df = pd.DataFrame(similar_movies, columns=['correlation'])
    corr_df.dropna(inplace=True)
    rating_counts = data.groupby('title')['rating'].count()
    corr_df = corr_df.join(rating_counts.rename("num_ratings"))
    results = corr_df[corr_df['num_ratings'] > min_ratings].sort_values('correlation', ascending=False)
    return results.head(10).reset_index().to_dict(orient='records')