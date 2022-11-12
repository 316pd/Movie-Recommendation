import streamlit as st
import pickle
import pandas as pd
import requests
from itertools import cycle
import helper

def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://ca-times.brightspotcdn.com/dims4/default/52e32ba/2147483647/strip/true/crop/5600x3733+0+0/resize/1200x800!/quality/80/?url=https%3A%2F%2Fcalifornia-times-brightspot.s3.amazonaws.com%2F3c%2Ffc%2Fb2f4c4764ea7bf98c761ad1a122c%2Fbethollywoodsignday3-1211.jpg");
             background-attachment: scroll;
             background-repeat: no-repeat;
             background-size: 1350px 400px;
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']

def recommend_movie(df):
  recommend_list = []
  recommend_posters = []
  i = 0
  while i < 10:
    movie_id = df['movie_id'][i:i+1].values[0]
    recommend_list.append(df['title'][i:i+1].values[0])
    recommend_posters.append(fetch_poster(movie_id))
    i += 1
  return recommend_list, recommend_posters

def top_10_popularity(df1, df2):
    df = df1.merge(df2, on='title')
    temp = df.sort_values('popularity',ascending=False).reset_index()[0:10]
    return temp

def top_10_voting(df1, df2):
    df = df1.merge(df2, on='title')
    temp = df[(df['vote_average'] >= 7.0) & (df['vote_count'] >= 9000)].sort_values('vote_average',ascending=False).reset_index()[0:10]
    return temp