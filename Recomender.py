import streamlit as st
import pickle
import pandas as pd
import requests 
# streamlit run Recomender.py

def fetch(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=a79d083ab9e9fc24937a21bb8adb281f&language=en-US'.format(movie_id))
    # print(response)
    data=response.json()
    poster_path = data['poster_path']
    return "https://image.tmdb.org/t/p/w500/"+ poster_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters
        
    # return recomended_movies,recomended_poster


movies_dict=pickle.load(open('movie_dict.pkl',('rb')))
similarity=pickle.load(open('similarity','rb'))
movies=pd.DataFrame(movies_dict)
st.title("Movie Recomender System")

option=st.selectbox(
    'Select the Movie'
    ,movies['title'].values)

if st.button('Recomend'):
    recomendation,poster=recommend(option)
    col = st.columns(5)
    for i in range(5):
        with col[i]:
            st.text(recomendation[i])
            st.image(poster[i])

