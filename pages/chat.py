import streamlit as st
import requests
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Mood Music - 여기서 듣기",
    page_icon="🎵",
    layout="centered"
)

# --------------------------------------------------
# 곡 정보 받기
# --------------------------------------------------

song = st.query_params.get("song", "")
artist = st.query_params.get("artist", "")

if not song or not artist:
    st.warning("재생할 음악을 찾을 수 없어요.")
    st.stop()

# --------------------------------------------------
# 배경
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at top, #fff1c9 0%, transparent 35%),
        linear-gradient(135deg, #3b2417, #160e09);
    color: white;
}

.player-title {
    text-align: center;
    font-size: 38px;
    font-weight: 800;
    margin-top: 20px;
    margin-bottom: 5px;
}

.player-subtitle {
    text-align: center;
    color: #d8c8bb;
    margin-bottom: 35px;
}

/* 축음기 */
.phonograph {
    position: relative;
    width: 330px;
    height: 330px;
    margin: 20px auto 35px auto;
}

/* 레코드 */
.record {
    position: absolute;
    width: 270px;
    height: 270px;
    left: 25px;
    top: 35px;
    border-radius: 50%;

    background:
        repeating-radial-gradient(
            circle,
            #171717 0px,
            #171717 5px,
            #252525 6px,
            #111111 8px
        );

    box-shadow:
        0 18px 35px rgba(0,0,0,0.55),
        inset 0 0 20px rgba(255,255,255,0.08);

    animation: spin 5s linear infinite;
}

/* 레코드 가운데 */
.record::after {
    content: "";
    position: absolute;
    width: 70px;
    height: 70px;
    left: 100px;
    top: 100px;
    border-radius: 50%;
    background: #d9a441;
    box-shadow: inset 0 0 0 10px #8e5e19;
}

/* 가운데 구멍 */
.record::before {
    content: "";
    position: absolute;
    width: 13px;
    height: 13px;
    left: 128px;
    top: 128px;
    border-radius: 50%;
    background: #1c130e;
    z-index: 2;
}

/* 톤암 */
.arm {
    position: absolute;
    width: 145px;
    height: 12px;
    background: #d5b78b;
    right: -10px;
    top: 85px;
    border-radius: 20px;
    transform: rotate(35deg);
    transform-origin: left center;
    z-index: 5;
    box-shadow: 0 4px 8px rgba(0,0,0,0.4);
}

/* 바늘 */
.needle {
    position: absolute;
    width: 30px;
    height: 38px;
    background: #c79b55;
    right: -8px;
    top: 110px;
    transform: rotate(35deg);
    border-radius: 5px;
    z-index: 6;
}

/* 축음기 몸체 */
.base {
    position: absolute;
    width: 310px;
    height: 65px;
    left: 10px;
    bottom: 0;
    background: linear-gradient(145deg, #8b542f, #4c2816);
    border-radius: 18px;
    box-shadow: 0 15px 25px rgba(0,0,0,0.5);
}

/* 스피커 */
.horn {
    position: absolute;
    width: 125px;
    height: 125px;
    right: -5px;
    top: -35px;
    background: linear-gradient(135deg, #d4a15c, #70421d);
    clip-path: polygon(
        100% 0,
        20% 30%,
        0 50%,
        20% 70%,
        100% 100%
    );
    z-index: 4;
}

/* 회전 */
@keyframes spin {
    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}

.song-card {
    background: rgba(255,255,255,0.10);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 25px;
    padding: 25px;
    text-align: center;
    backdrop-filter: blur(10px);
    margin-bottom: 25px;
}

.song-name {
    font-size: 28px;
    font-weight: 800;
}

.artist-name {
    color: #d8c8bb;
    font-size: 17px;
    margin-top: 7px;
}

.preview-info {
    text-align: center;
    color: #d8c8bb;
    font-size: 14px;
    margin-top: 15px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# 제목
# --------------------------------------------------

st.markdown(
    '<div class="player-title">🎵 Mood Music</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="player-subtitle">나만의 작은 축음기 🎶</div>',
    unsafe_allow_html=True
)

# --------------------------------------------------
# 음악 검색
# --------------------------------------------------

preview_url = None
artwork_url = None

try:

    response = requests.get(
        "https://itunes.apple.com/search",
        params={
            "term": f"{song} {artist}",
            "media": "music",
            "entity": "song",
            "limit": 1
        },
        timeout=5
    )

    if response.status_code == 200:

        data = response.json()

        if data.get("results"):

            result = data["results"][0]

            preview_url = result.get("previewUrl")
            artwork_url = result.get("artworkUrl100")

            if artwork_url:
                artwork_url = artwork_url.replace(
                    "100x100",
                    "600x600"
                )

except Exception:
    pass

# --------------------------------------------------
# 음악 정보
# --------------------------------------------------

st.markdown(
    f"""
    <div class="song-card">
        <div class="song-name">{song}</div>
        <div class="artist-name">{artist}</div>
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# 축음기
# --------------------------------------------------

st.markdown(
    """
    <div class="phonograph">

        <div class="record"></div>

        <div class="arm"></div>

        <div class="needle"></div>

        <div class="horn"></div>

        <div class="base"></div>

    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# 5초 미리듣기
# --------------------------------------------------

if preview_url:

    audio_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                background: transparent;
                text-align: center;
                font-family: sans-serif;
            }}

            audio {{
                width: 100%;
                max-width: 500px;
            }}

            .text {{
                color: #d8c8bb;
                font-size: 14px;
                margin-top: 8px;
            }}
        </style>
    </head>

    <body>

        <audio id="player" controls>
            <source src="{preview_url}" type="audio/mp4">
        </audio>

        <div class="text">
            🎶 약 5초 동안 미리 들어볼 수 있어요
        </div>

        <script>

            const player = document.getElementById("player");

            player.addEventListener("timeupdate", function() {{

                if (player.currentTime >= 5) {{
                    player.pause();
                    player.currentTime = 0;
                }}

            }});

        </script>

    </body>
    </html>
    """

    components.html(
        audio_html,
        height=90
    )

else:

    st.info(
        "이 곡은 현재 미리듣기를 제공하지 않아요."
    )

# --------------------------------------------------
# Spotify
# --------------------------------------------------

spotify_query = f"{song} {artist}".replace(" ", "%20")

st.link_button(
    "🟢 Spotify에서 듣기",
    f"https://open.spotify.com/search/{spotify_query}",
    use_container_width=True
)

# --------------------------------------------------
# 메인으로 돌아가기
# --------------------------------------------------

if st.button(
    "🏠 음악 추천으로 돌아가기",
    use_container_width=True
):
    st.switch_page("main.py")
