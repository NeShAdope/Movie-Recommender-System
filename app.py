import streamlit as st
import pickle
import pandas as pd
import requests
import gdown
import os

# Google Drive file IDs (from share links)
SIMILARITY_PKL_ID = "1AeBUX_70AocYjhg7qyV3lcktmGsqlFAd"
TMDB_CSV_ID = "1NS5Hr7nhTI1KxAPWhhxHIDdF1pVuhMPv"

def get_drive_file(file_id, dest_path):
    """Download file from Google Drive if not already present."""
    if not os.path.exists(dest_path):
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, dest_path, quiet=False)
    return dest_path

def poster(movie_id):
    response=requests.get('https://api.themoviedb.org/3/movie/{}?api_key=20e863b021e2f5f89f0f46d621aa9716&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/pdata"+data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances= similarity[movie_index]
    movies_list=sorted(list(enumerate(distances)),reverse=True,key= lambda x: x[1])[1:6]
    
    reco_list=[]
    reco_poster=[]
    for i in movies_list:
        reco_list.append(movies.iloc[i[0]].title)
        reco_poster.append(poster(movies.iloc[i[0]].id))
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
