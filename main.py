import pickle
import streamlit as st
import pandas as pd
import requests

# Function to fetch movie posters
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=b0ff212b4d9ea564bce25634e5898a6c&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/original"+data['poster_path']

# Load the movie dataset
movies_df = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

# Function to recommend movies
def recommend(movie):
    movie_index = movies_df[movies_df['title']==movie].index[0]
    distance = list(enumerate(similarity[movie_index]))
    sorted_dist = sorted(distance,reverse=True,key=lambda x: x[1])[:10]

    recommended_movies = []
    recommended_movies_poster = []
    for i in sorted_dist:
        movie_id = movies_df.iloc[i[0]]['id']
        recommended_movies.append(movies_df.iloc[i[0]]['title'])
        # Fetch poster from API
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster

# Extract movie titles from the dataset
movies_list = movies_df['title'].values

# Custom CSS for styling with a black and dark orange background
st.markdown(
    """
    <style>
    body {
        background-color: #1E1E1E; /* Black background */
        color: #FF5733; /* Dark orange text color */
    }
    .title {
        font-size: 36px;
        text-align: center;
        color: #FF5733;
    }
    .header {
        font-size: 24px;
        color: #3333FF;
    }
    .recommend-button {
        background-color: #FF5733; /* Dark orange button color */
        color: white;
        font-size: 18px;
        border-radius: 8px;
    }
    .movie-title {
        font-size: 18px;
        font-weight: bold;
        color: #FF5733;
    }
    .movie-image {
        width: 150px;
        height: auto;
        margin: 10px;
        border-radius: 5px;
    }
    .footer {
        text-align: center;
        font-size: 14px;
        color: #FF5733; /* Dark orange footer text color */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Movie Recommendation System")
st.text("This recommendation engine is made by")
st.header("Shaik Firoz")

selected_movie_names = st.selectbox('Select a Movie', movies_list)

if st.button('Recommend', key='recommend-button'):
    recommended, poster = recommend(selected_movie_names)

    # Move the selected movie to the front of the recommended list
    recommended.insert(0, selected_movie_names)
    poster.insert(0, fetch_poster(movies_df[movies_df['title']==selected_movie_names]['id'].values[0]))

    rows = 2
    cols = 5
    for row in range(rows):
        start_idx = row * cols
        end_idx = start_idx + cols
        row_recommended = recommended[start_idx:end_idx]
        row_poster = poster[start_idx:end_idx]

        col_list = st.columns(cols)
        for col, movie, img_url in zip(col_list, row_recommended, row_poster):
            with col:
                st.markdown(f"<p class='movie-title'>{movie}</p>", unsafe_allow_html=True)
                st.image(img_url, use_column_width=True, caption='')
                st.markdown("<hr>", unsafe_allow_html=True)

# Adding a footer
st.markdown("<p class='footer'>Built with ❤️ by Shaik Firoz</p>", unsafe_allow_html=True)
