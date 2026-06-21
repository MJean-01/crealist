import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pyperclip
import webbrowser

st.set_page_config(page_title="Grok Playlist", page_icon="🎵")

st.title("🎵 Grok Playlist Creator")
st.write("Gera playlists sem complicação")

# ================= CREDENCIAIS =================
CLIENT_ID = "8a48218f1d5948e3b4e32f2461574df0"
CLIENT_SECRET = "ba27eb8411de4a6e89f327cea6cb1e88"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
))

genero = st.text_input("Gênero musical", value="trap")
quantidade = st.slider("Quantidade de músicas", 5, 50, 20)

if st.button("🔥 Gerar Playlist", type="primary"):
    with st.spinner(f"Buscando {quantidade} músicas de {genero}..."):
        results = sp.search(q=genero, type="track", limit=quantidade + 15)
        
        tracks = results['tracks']['items']
        seen = set()
        unique_tracks = []
        
        for track in tracks:
            if track['id'] not in seen:
                seen.add(track['id'])
                unique_tracks.append(track)
            if len(unique_tracks) >= quantidade:
                break
        
        if unique_tracks:
            st.success(f"Encontrei {len(unique_tracks)} músicas!")
            
            links = []
            for i, track in enumerate(unique_tracks, 1):
                nome = track['name']
                artista = track['artists'][0]['name']
                link = track['external_urls']['spotify']
                links.append(link)
                st.write(f"**{i}.** {nome} - {artista}")
            
            pyperclip.copy("\n".join(links))
            st.success("✅ Links copiados!")
            
            if st.button("🚀 Abrir Spotify"):
                webbrowser.open(f"https://open.spotify.com/search/{genero}")
            
            st.info("Abra o Spotify → Crie uma playlist nova → Cole os links")
        else:
            st.error("Não encontrei músicas.")

st.caption("Feito pelo Grok")