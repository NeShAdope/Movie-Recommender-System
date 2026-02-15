import streamlit as st
import pickle
import pandas as pd
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import gdown
import os
import time

# Google Drive file IDs (from share links)
SIMILARITY_PKL_ID = "1AeBUX_70AocYjhg7qyV3lcktmGsqlFAd"
TMDB_CSV_ID = "1NS5Hr7nhTI1KxAPWhhxHIDdF1pVuhMPv"

# Placeholder when TMDB is unreachable
NO_POSTER_URL = "https://via.placeholder.com/500x750?text=No+Poster"

def get_drive_file(file_id, dest_path):
    """Download file from Google Drive if not already present."""
    if not os.path.exists(dest_path):
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, dest_path, quiet=False)
    return dest_path

def _session_with_retries():
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503])
    session.mount("https://", HTTPAdapter(max_retries=retry))
    return session

def poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=20e863b021e2f5f89f0f46d621aa9716&language=en-US".format(movie_id)
    try:
        response = _session_with_retries().get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        path = data.get("poster_path")
        if path:
            return "https://image.tmdb.org/t/p/w500" + path
    except (requests.RequestException, KeyError):
        pass
    return NO_POSTER_URL


def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances= similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key= lambda x: x[1])[1:6]
    
    reco_list=[]
    reco_poster=[]
    for i in movies_list:
        reco_list.append(movies.iloc[i[0]].title)
        reco_poster.append(poster(movies.iloc[i[0]].id))
        time.sleep(0.2)  # avoid connection resets from rapid requests
    return reco_list,reco_poster

movie_dict=pickle.load(open('movie_dict.pkl','rb'))
movies=pd.DataFrame(movie_dict)

similarity_path = get_drive_file(SIMILARITY_PKL_ID, "similarity.pkl")
similarity=pickle.load(open(similarity_path,'rb'))

st.title('Movie Recommender System')

selected_movie = st.selectbox('Select a movie', movies['title'].values)

if st.button('Recommend'):
    names,posters=recommend(selected_movie)
    import streamlit as st
    col1, col2, col3,col4,col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
