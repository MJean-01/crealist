import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pyperclip
import webbrowser

st.set_page_config(page_title="Grok Playlist", page_icon="🎵")

st.title("🎵 Grok Playlist Creator")
st.write("Recomendações melhores")

CLIENT_ID = "8a48218f1d5948e3b4e32f2461574df0"
CLIENT_SECRET = "ba27eb8411de4a6e89f327cea6cb1e88"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
))

genero = st.text_input("Gênero musical", value="trap")
quantidade = st.slider("Quantidade de músicas", 5, 40, 20)

if st.button("🔥 Gerar Playlist", type="primary"):
    with st.spinner(f"Gerando recomendações de {genero}..."):
        try:
            # Usa recommendations (melhor que search simples)
            results = sp.recommendations(
                seed_genres=[genero.lower()],
                limit=quantidade,
                min_popularity=60   # Tenta pegar músicas mais conhecidas
            )
            
            tracks = results['tracks']
            
            if tracks:
                st.success(f"Encontrei {len(tracks)} recomendações!")
                
                links = []
                for i, track in enumerate(tracks, 1):
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
                st.error("Não encontrou recomendações. Tente outro gênero.")
        except Exception as e:
            st.error("Erro ao buscar recomendações. Tente outro gênero.")

st.caption("Feito pelo Grok • Recomendações")