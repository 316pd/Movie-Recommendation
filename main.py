import streamlit as st
import pickle
import pandas as pd
import requests
from itertools import cycle
import helper


df1 = pd.read_csv('tmdb_5000_movies.csv')
df2 = pd.read_csv('tmdb_5000_credits.csv')

user_menu = st.sidebar.radio(
    'Select option',
    ('Recommender System','Top 10\'s')
)

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']

def recommend_movie(movie):
  movie_index = movies[movies['title'] == movie].index[0]
  distances = movie_similarity[movie_index]
  movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:9]
  recommend_list = []
  recommend_posters = []
  for i in movies_list:
    movie_id = movies.iloc[i[0]].movie_id
    recommend_list.append(movies.iloc[i[0]].title)
    recommend_posters.append(fetch_poster(movie_id))
  return recommend_list, recommend_posters

movies_dict = pickle.load(open('movies_dict.pkl',"rb"))
movie_similarity = pickle.load(open('movie_similarity.pkl',"rb"))
movies = pd.DataFrame(movies_dict)

movies_list = movies['title'].values

if user_menu == 'Recommender System':
  helper.add_bg_from_url()
  new_title = '<p style="font-family:sans-serif; color:White; font-size: 40px;">Movie Recommendation System</p>'
  st.markdown(new_title, unsafe_allow_html=True)
  # st.title('Movie Recommendation System')
  select_movie_name = st.selectbox('',movies_list)

  if st.button('Recommend'):
      names, posters = recommend_movie(select_movie_name)
      cols = cycle(st.columns(4)) # st.columns here since it is out of beta at the time I'm writing this
      for idx, filteredImage in enumerate(posters):
          next(cols).image(filteredImage, width=150, caption=names[idx])

if user_menu == 'Top 10\'s':
  option = ['Top 10 Most Popular', 'Top 10 Highest Vote']
  select = st.selectbox('Filter', option)
  if select == 'Top 10 Popular':
    helper.add_bg_from_url()
    new_title = '<p style="font-family:sans-serif; color:White; font-size: 40px;">Top 10 Movies based on Popularity</p>'
    st.markdown(new_title, unsafe_allow_html=True)
    df = helper.top_10_popularity(df1, df2)
    names, posters = helper.recommend_movie(df)
    cols = cycle(st.columns(4)) # st.columns here since it is out of beta at the time I'm writing this
    for idx, filteredImage in enumerate(posters):
        next(cols).image(filteredImage, width=150, caption=names[idx])
  if select == 'Top 10 Votes':
    helper.add_bg_from_url()
    new_title = '<p style="font-family:sans-serif; color:White; font-size: 40px;">Top 10 Movies based on Votes</p>'
    st.markdown(new_title, unsafe_allow_html=True)
    df = helper.top_10_voting(df1, df2)
    names, posters = helper.recommend_movie(df)
    cols = cycle(st.columns(4)) # st.columns here since it is out of beta at the time I'm writing this
    for idx, filteredImage in enumerate(posters):
        next(cols).image(filteredImage, width=150, caption=names[idx])