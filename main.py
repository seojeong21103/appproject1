import streamlit as st
import random
import requests

# --------------------------------------------------
# 기본 설정
# --------------------------------------------------

st.set_page_config(
    page_title="Mood Music 🎧",
    page_icon="🎵",
    layout="centered"
)

# --------------------------------------------------
# 음악 데이터
# --------------------------------------------------

music_data = {
    "행복해요": [
        ("Dynamite", "BTS"),
        ("Super Shy", "NewJeans"),
        ("After LIKE", "IVE"),
        ("Queencard", "(G)I-DLE"),
        ("LOVE DIVE", "IVE")
    ],

    "기분이 좋아요": [
        ("Magnetic", "ILLIT"),
        ("OMG", "NewJeans"),
        ("ASAP", "STAYC"),
        ("파이팅 해야지", "부석순"),
        ("한 페이지가 될 수 있게", "DAY6")
    ],

    "평범해요": [
        ("밤양갱", "비비"),
        ("Ditto", "NewJeans"),
        ("Love Lee", "AKMU"),
        ("고백", "멜로망스"),
        ("예뻤어", "DAY6")
    ],

    "우울해요": [
        ("밤편지", "아이유"),
        ("그대만 있다면", "너드커넥션"),
        ("비가 오는 날엔", "헤이즈"),
        ("한숨", "이하이"),
        ("너의 모든 순간", "성시경")
    ],

    "스트레스 받아요": [
        ("MANIAC", "Stray Kids"),
        ("Baddie", "IVE"),
        ("ANTIFRAGILE", "LE SSERAFIM"),
        ("God's Menu", "Stray Kids"),
        ("Drama", "aespa")
    ]
}

# --------------------------------------------------
# 기분별 배경
# --------------------------------------------------

mood_backgrounds = {
    "행복해요":
        "linear-gradient(135deg, #FFF4B8 0%, #FFD6E7 100%)",

    "기분이 좋아요":
        "linear-gradient(135deg, #D9F5FF 0%, #D9E7FF 100%)",

    "평범해요":
        "linear-gradient(135deg, #F1E7FF 0%, #E7EFFF 100%)",

    "우울해요":
        "linear-gradient(135deg, #DCEBFF 0%, #C9D9F5 100%)",

    "스트레스 받아요":
        "linear-gradient(135deg, #FFE2D1 0%, #FFD0D8 100%)"
}

# --------------------------------------------------
# 디자인
# --------------------------------------------------

st.markdown(
    """
    <style>

    .stApp {
        transition: background 0.8s ease;
    }

    .title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        color: #6c63ff;
        margin-top: 10px;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 17px;
        color: #666;
        margin-bottom: 30px;
    }

    .music-card {
        background: rgba(255,255,255,0.92);
        padding: 25px;
        border-radius: 25px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        text-align: center;
        margin-top: 15px;
    }

    .music-title {
        font-size: 28px;
        font-weight: 700;
        color: #333;
    }

    .artist {
        font-size: 17px;
        color: #777;
        margin-top: 5px;
    }

    .reason {
        background: rgba(245,243,255,0.9);
        padding: 16px;
        border-radius: 15px;
        color: #555;
        line-height: 1.8;
        margin-top: 18px;
    }

    .footer {
        text-align: center;
        color: #777;
        font-size: 13px;
        margin-top: 40px;
        margin-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# 제목
# --------------------------------------------------

st.markdown(
    '<div class="title">🎧 Mood Music</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">지금 나의 기분과 컨디션에 딱 맞는 음악을 찾아보세요 ✨</div>',
    unsafe_allow_html=True
)

# --------------------------------------------------
# 기분 선택
# --------------------------------------------------

st.markdown("### 💭 지금 기분은 어떤가요?")

mood = st.selectbox(
    "감정",
    [
        "행복해요",
        "기분이 좋아요",
        "평범해요",
        "우울해요",
        "스트레스 받아요"
    ],
    label_visibility="collapsed"
)

# --------------------------------------------------
# 배경색 변경
# --------------------------------------------------

background = mood_backgrounds[mood]

st.markdown(
    f"""
    <style>
    .stApp {{
        background: {background};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div style="
        text-align:center;
        color:#666;
        margin-bottom:20px;
        font-size:16px;
    ">
        현재 선택한 기분 : <b>{mood}</b>
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# 컨디션
# --------------------------------------------------

st.markdown("### 🔋 오늘의 컨디션은?")

energy = st.radio(
    "컨디션",
    [
        "⚡ 에너지가 넘쳐요",
        "😊 적당히 괜찮아요",
        "😴 조금 피곤해요",
        "🥱 많이 피곤해요"
    ],
    horizontal=True,
    label_visibility="collapsed"
)

# --------------------------------------------------
# 음악 분위기
# --------------------------------------------------

st.markdown("### 🎶 어떤 음악을 듣고 싶나요?")

style = st.select_slider(
    "음악 분위기",
    options=[
        "🌙 잔잔하게",
        "🌿 편안하게",
        "☀️ 기분 좋게",
        "💃 신나게"
    ],
    value="☀️ 기분 좋게"
)

# --------------------------------------------------
# 음악 추천 버튼
# --------------------------------------------------

if st.button(
    "✨ 나에게 맞는 음악 추천받기",
    use_container_width=True
):

    songs = music_data[mood]

    # 피곤한 경우
    if "피곤" in energy:

        songs = [
            ("밤편지", "아이유"),
            ("Ditto", "NewJeans"),
            ("한숨", "이하이"),
            ("너의 모든 순간", "성시경"),
            ("Love Lee", "AKMU")
        ]

    # 에너지가 넘치는 경우
    elif "에너지가 넘쳐요" in energy:

        songs = [
            ("Dynamite", "BTS"),
            ("Super Shy", "NewJeans"),
            ("ANTIFRAGILE", "LE SSERAFIM"),
            ("LOVE DIVE", "IVE"),
            ("God's Menu", "Stray Kids")
        ]

    song, artist = random.choice(songs)

    st.session_state["song"] = song
    st.session_state["artist"] = artist
    st.session_state["mood"] = mood
    st.session_state["energy"] = energy
    st.session_state["style"] = style

# --------------------------------------------------
# 추천 결과
# --------------------------------------------------

if "song" in st.session_state:

    song = st.session_state["song"]
    artist = st.session_state["artist"]

    st.markdown("---")

    st.markdown("### 💖 오늘의 추천 음악")

    # --------------------------------------------------
    # iTunes에서 썸네일 가져오기
    # --------------------------------------------------

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

                artwork_url = result.get(
                    "artworkUrl100"
                )

                if artwork_url:

                    artwork_url = artwork_url.replace(
                        "100x100",
                        "600x600"
                    )

    except Exception:
        artwork_url = None

    # --------------------------------------------------
    # 썸네일
    # --------------------------------------------------

    if artwork_url:

        st.image(
            artwork_url,
            width=280
        )

    else:

        st.markdown(
            """
            <div style="
                width:280px;
                height:280px;
                margin:20px auto;
                border-radius:25px;
                background:rgba(255,255,255,0.75);
                display:flex;
                align-items:center;
                justify-content:center;
                font-size:80px;
                box-shadow:0 10px 30px rgba(0,0,0,0.12);
            ">
                🎵
            </div>
            """,
            unsafe_allow_html=True
        )

    # --------------------------------------------------
    # 음악 정보
    # --------------------------------------------------

    st.markdown(
        f"""
        <div class="music-card">

            <div class="music-title">
                {song}
            </div>

            <div class="artist">
                {artist}
            </div>

            <div class="reason">
                💭 현재 기분은 <b>{st.session_state["mood"]}</b><br>
                🔋 컨디션은 <b>{st.session_state["energy"]}</b><br>
                🎶 원하는 분위기는 <b>{st.session_state["style"]}</b>
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------
    # Spotify / 설명보기
    # --------------------------------------------------

    spotify_query = (
        f"{song} {artist}"
        .replace(" ", "%20")
    )

    col1, col2 = st.columns(2)

    # Spotify
    with col1:

        st.link_button(
            "🟢 Spotify에서 듣기",
            f"https://open.spotify.com/search/{spotify_query}",
            use_container_width=True
        )

    # 설명보기
    with col2:

        if st.button(
            "📖 설명보기",
            use_container_width=True
        ):

            st.query_params["song"] = song
            st.query_params["artist"] = artist

            st.switch_page(
                "pages/chat.py"
            )

    # --------------------------------------------------
    # 다른 음악 추천
    # --------------------------------------------------

    if st.button(
        "🔄 다른 음악 추천",
        use_container_width=True
    ):

        st.session_state.pop(
            "song",
            None
        )

        st.session_state.pop(
            "artist",
            None
        )

        st.rerun()

# --------------------------------------------------
# 하단
# --------------------------------------------------

st.markdown(
    """
    <div class="footer">
        🎵 오늘의 기분에 맞는 음악으로 잠깐의 휴식을 가져보세요 :)
    </div>
    """,
    unsafe_allow_html=True
)
