import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pyperclip
import webbrowser
import random

st.set_page_config(page_title="Grok Playlist", page_icon="🎵")

st.title("🎵 Grok Playlist Creator")
st.write("Músicas de melhor qualidade")

CLIENT_ID = "8a48218f1d5948e3b4e32f2461574df0"
CLIENT_SECRET = "ba27eb8411de4a6e89f327cea6cb1e88"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
))

genero = st.text_input("Gênero musical", value="trap")
quantidade = st.slider("Quantidade de músicas", 5, 40, 20)

if st.button("🔥 Gerar Playlist de Qualidade", type="primary"):
    with st.spinner(f"Buscando boas músicas de {genero}..."):
        try:
            # Busca com filtro de popularidade
            offset = random.randint(0, 50)
            results = sp.search(
                q=f"genre:{genero}", 
                type="track", 
                limit=quantidade + 20, 
                offset=offset
            )
            
            tracks = results['tracks']['items']
            good_tracks = []
            
            for track in tracks:
                if track['popularity'] >= 40:   # Filtra músicas mais populares
                    good_tracks.append(track)
                if len(good_tracks) >= quantidade:
                    break
            
            if good_tracks:
                st.success(f"Encontrei {len(good_tracks)} músicas boas!")
                
                links = []
                for i, track in enumerate(good_tracks, 1):
                    nome = track['name']
                    artista = track['artists'][0]['name']
                    pop = track['popularity']
                    link = track['external_urls']['spotify']
                    links.append(link)
                    st.write(f"**{i}.** {nome} - {artista} (Popularidade: {pop})")
                
                pyperclip.copy("\n".join(links))
                st.success("✅ Links copiados!")
                
                if st.button("🚀 Abrir Spotify"):
                    webbrowser.open(f"https://open.spotify.com/search/{genero}")
                
                st.info("Abra o Spotify → Crie uma playlist nova → Cole os links")
            else:
                st.error("Não encontrei músicas boas. Tente outro gênero.")
        except Exception as e:
            st.error("Erro na busca. Tente outro gênero.")

st.caption("Feito pelo Grok • Filtro de qualidade")