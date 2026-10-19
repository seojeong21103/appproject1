import base64
import random
from pathlib import Path

import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="당신을 위한 디저트 추천 주사위",
    page_icon="🎲",
    layout="centered",
    initial_sidebar_state="collapsed",
)

BASE_DIR = Path(__file__).parent
COVER_PATH = BASE_DIR / "cover.png"

DESSERTS = {
    1: {"name": "딸기 케이크", "emoji": "🍰", "description": "부드러운 생크림과 상큼한 딸기가 만나는 클래식 디저트!", "mood": "달콤하고 포근한 기분이 필요할 때", "taste": "상큼", "pairing": "따뜻한 아메리카노", "mission": "케이크 위에서 딸기를 가장 먼저 찾아보기"},
    2: {"name": "마카롱", "emoji": "🍬", "description": "알록달록한 색과 쫀득한 식감으로 기분 전환하기 좋은 디저트!", "mood": "작고 귀여운 달콤함이 당길 때", "taste": "달콤", "pairing": "우유 또는 바닐라 라테", "mission": "오늘의 기분과 어울리는 색 고르기"},
    3: {"name": "와플", "emoji": "🧇", "description": "바삭한 와플에 시럽이나 아이스크림을 곁들여 먹어 봐!", "mood": "든든하면서도 달콤한 간식이 먹고 싶을 때", "taste": "든든", "pairing": "바닐라 아이스크림 한 스쿱", "mission": "토핑을 딱 두 가지 조합해 보기"},
    4: {"name": "푸딩", "emoji": "🍮", "description": "탱글탱글하고 부드러운 식감이 매력적인 디저트!", "mood": "부담 없이 부드러운 디저트가 당길 때", "taste": "부드러움", "pairing": "홍차 또는 밀크티", "mission": "한 입씩 천천히 식감에 집중해 보기"},
    5: {"name": "초콜릿 브라우니", "emoji": "🍫", "description": "진한 초콜릿 풍미가 가득한 꾸덕꾸덕한 브라우니!", "mood": "진하고 깊은 달콤함이 필요할 때", "taste": "초코", "pairing": "차가운 우유", "mission": "견과류 토핑이 있는 버전 찾아보기"},
    6: {"name": "아이스크림", "emoji": "🍨", "description": "차갑고 달콤하게 즐기는 언제나 반가운 디저트!", "mood": "시원하게 기분 전환하고 싶을 때", "taste": "시원", "pairing": "바삭한 쿠키", "mission": "평소 안 먹어 본 맛에 도전하기"},
}

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&family=Black+Han+Sans&display=swap');
.stApp { background:#080808; color:#f8f8f8; }
header[data-testid="stHeader"] { background:transparent; }
#MainMenu, footer {visibility:hidden;}
.block-container {max-width:850px; padding-top:2rem; padding-bottom:3rem;}
.title {font-family:'Black Han Sans',sans-serif;color:#fff;text-align:center;font-size:clamp(2rem,6vw,3.6rem);line-height:1.25;}
.subtitle {font-family:'Gowun Dodum',sans-serif;text-align:center;color:#c9c9c9;font-size:1.05rem;margin:.6rem 0 1.5rem;}
.hint {text-align:center;color:#aaa;font-family:'Gowun Dodum',sans-serif;margin-top:1rem;}
div.stButton > button {font-family:'Gowun Dodum',sans-serif;font-weight:700;border:1px solid #fff;background:#fff;color:#080808;border-radius:14px;min-height:3.2rem;transition:all .15s ease;}
div.stButton > button:hover {border-color:#ddd;background:#dedede;color:#000;transform:translateY(-1px);}
div[data-testid="stButton"] button[kind="primary"] {font-size:1.4rem;}
.dice-stage {display:flex;justify-content:center;align-items:center;min-height:230px;margin:.4rem auto 0;perspective:700px;}
.cube {position:relative;width:120px;height:120px;transform-style:preserve-3d;animation:float 2s ease-in-out infinite;}
.face {position:absolute;width:120px;height:120px;border:3px solid #111;border-radius:20px;background:#f7f7f7;color:#080808;display:flex;align-items:center;justify-content:center;font-size:3.7rem;font-weight:900;box-shadow:inset -7px -7px 0 #d6d6d6;}
.front {transform:translateZ(60px);} .right {transform:rotateY(90deg) translateZ(60px);} .top {transform:rotateX(90deg) translateZ(60px);}
.cube-idle {animation:float 2s ease-in-out infinite, wobble 1.1s linear infinite;}
.boom-stage .cube {animation:spinboom 1.15s ease-in forwards;}
@keyframes float {0%,100%{margin-top:0}50%{margin-top:-12px}}
@keyframes wobble {0%{transform:rotateX(0) rotateY(0)}25%{transform:rotateX(100deg) rotateY(130deg)}50%{transform:rotateX(220deg) rotateY(250deg)}75%{transform:rotateX(350deg) rotateY(400deg)}100%{transform:rotateX(540deg) rotateY(720deg)}}
@keyframes spinboom {0%{transform:rotateX(0) rotateY(0) scale(1);opacity:1}55%{transform:rotateX(720deg) rotateY(900deg) scale(1.1);opacity:1}78%{transform:rotateX(1080deg) rotateY(1300deg) scale(1.35);opacity:.9;filter:brightness(2)}100%{transform:rotateX(1440deg) rotateY(1800deg) scale(.05);opacity:0;filter:brightness(4)}}
.boom-title {font-family:'Black Han Sans',sans-serif;text-align:center;font-size:clamp(3rem,10vw,5.5rem);color:#fff;text-shadow:0 0 18px #fff, 4px 4px 0 #777;animation:slam .55s cubic-bezier(.2,1.5,.4,1) both;}
.boom-sub {text-align:center;color:#aaa;font-family:'Gowun Dodum',sans-serif;margin:.5rem 0 1rem;}
@keyframes slam {0%{transform:scale(4) rotate(12deg);opacity:0}65%{transform:scale(.85) rotate(-4deg);opacity:1}100%{transform:scale(1) rotate(0);opacity:1}}
.spark {position:relative;text-align:center;font-size:2rem;letter-spacing:1rem;animation:flash .5s steps(2,end) infinite alternate;}
@keyframes flash {from{opacity:.3;transform:scale(.8)}to{opacity:1;transform:scale(1.15)}}
.result-card {border:1px solid #555;border-radius:20px;padding:1.5rem 1.25rem;margin-top:1.2rem;text-align:center;background:linear-gradient(145deg,#171717,#090909);}
.dessert-emoji {font-size:4rem;line-height:1.3;}
.dessert-name {font-family:'Black Han Sans',sans-serif;font-size:2.2rem;color:white;margin:.25rem 0 .7rem;}
.dessert-desc {color:#e4e4e4;font-family:'Gowun Dodum',sans-serif;font-size:1.05rem;}
.dessert-mood {color:#aaa;font-family:'Gowun Dodum',sans-serif;margin-top:.7rem;font-size:.95rem;}
.feature-card {border:1px solid #393939;border-radius:16px;padding:1rem;background:#111;height:100%;}
.feature-label {color:#aaa;font-size:.85rem;margin-bottom:.35rem;}
.feature-value {color:#fff;font-size:1.05rem;font-weight:700;}
hr {border-color:#333;}
</style>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = st.query_params.get("page", "home")
if "first_roll_done" not in st.session_state:
    st.session_state.first_roll_done = False
if "dice_result" not in st.session_state:
    st.session_state.dice_result = None
if "roll_history" not in st.session_state:
    st.session_state.roll_history = []
if "show_boom" not in st.session_state:
    st.session_state.show_boom = False

page = st.query_params.get("page", st.session_state.page)

if page == "home":
    if not COVER_PATH.exists():
        st.error("cover.png 파일을 찾을 수 없어요. main.py와 같은 폴더에 cover.png를 넣어 주세요.")
        st.stop()
    image_data = base64.b64encode(COVER_PATH.read_bytes()).decode("utf-8")
    st.markdown(
        f'''<a href="?page=dice" target="_self" aria-label="디저트 추천 시작하기" style="display:block;line-height:0;border-radius:18px;overflow:hidden;cursor:pointer;">
        <img src="data:image/png;base64,{image_data}" alt="당신을 위한 디저트 추천 주사위 - 눌러서 시작" style="display:block;width:100%;height:auto;transition:transform .2s ease;" />
        </a><div class="hint">이미지를 눌러 디저트 추천을 시작하세요</div>''',
        unsafe_allow_html=True,
    )
else:
    st.markdown('<div class="title">오늘의 디저트는?</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">첫 번째 주사위에는 함정이 숨어 있어…</div>', unsafe_allow_html=True)

    if st.session_state.show_boom:
        st.markdown('''<div class="dice-stage boom-stage"><div class="cube"><div class="face front">⚀</div><div class="face right">⚁</div><div class="face top">⚂</div></div></div>
        <div class="spark">✦　✧　✦</div><div class="boom-title">꽝!</div><div class="boom-sub">주사위가 폭발했다! 이번에는 디저트가 없어…</div>''', unsafe_allow_html=True)
        if st.button("다시 도전하기", key="after_boom", type="primary", use_container_width=True):
            st.session_state.show_boom = False
            st.rerun()
    else:
        st.markdown('''<div class="dice-stage"><div class="cube cube-idle"><div class="face front">⚀</div><div class="face right">⚁</div><div class="face top">⚂</div></div></div>''', unsafe_allow_html=True)
        st.markdown('<div class="hint">주사위를 눌러 굴려 봐!</div>', unsafe_allow_html=True)
        if st.button("🎲 주사위 굴리기", key="roll_dice", type="primary", use_container_width=True):
            if not st.session_state.first_roll_done:
                st.session_state.first_roll_done = True
                st.session_state.dice_result = None
                st.session_state.show_boom = True
                st.rerun()
            else:
                number = random.randint(1, 6)
                dessert = DESSERTS[number]
                try:
                    api_key = st.secrets["GEMINI_API_KEY"]
                    client = OpenAI(
                        api_key=api_key,
                        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
                    )
                    response = client.chat.completions.create(
                        model="gemini-3.5-flash-lite",
                        messages=[
                            {"role": "system", "content": "너는 재미있고 친근한 한국어 디저트 추천가야. 주어진 디저트 이름은 바꾸지 말고, 짧고 개성 있는 추천 이유를 2문장으로 써. 이모지는 최대 2개만 사용해."},
                            {"role": "user", "content": f"주사위 숫자는 {number}이고 정해진 디저트는 {dessert['name']}이야. 이 디저트를 추천하는 짧고 재미있는 설명을 작성해 줘."},
                        ],
                        temperature=0.9,
                        max_tokens=120,
                    )
                    ai_description = response.choices[0].message.content.strip()
                except KeyError:
                    st.error('Gemini API 키가 없어요. Streamlit Cloud의 Settings → Secrets에 GEMINI_API_KEY = "발급받은_API_키"를 추가해 주세요.')
                    st.stop()
                except Exception as exc:
                    st.error(f"Gemini API 호출에 실패했어요. API 키와 모델 설정을 확인해 주세요. 상세 내용: {exc}")
                    st.stop()

                st.session_state.dice_result = {"number": number, "dessert": dessert, "ai_description": ai_description}
                st.session_state.roll_history.insert(0, number)
                st.session_state.roll_history = st.session_state.roll_history[:5]
                st.rerun()

    if st.session_state.dice_result is not None and not st.session_state.show_boom:
        result = st.session_state.dice_result
        number = result["number"]
        dessert = result["dessert"]
        st.markdown('<hr>', unsafe_allow_html=True)
        st.markdown(f'''<div class="result-card">
            <div style="color:#aaa;font-family:'Gowun Dodum',sans-serif;">오늘의 주사위 숫자</div>
            <div style="font-family:'Black Han Sans',sans-serif;font-size:3.4rem;color:#fff;">{number}</div>
            <div class="dessert-emoji">{dessert['emoji']}</div>
            <div class="dessert-name">{dessert['name']}</div>
            <div class="dessert-desc">{result['ai_description']}</div>
            <div class="dessert-mood">✦ {dessert['mood']} ✦</div>
        </div>''', unsafe_allow_html=True)
        st.markdown("### 🍽️ 디저트 페어링 추천")
        left, right = st.columns(2)
        with left:
            st.markdown(f'''<div class="feature-card"><div class="feature-label">함께 먹으면 좋은 것</div><div class="feature-value">☕ {dessert['pairing']}</div></div>''', unsafe_allow_html=True)
        with right:
            st.markdown(f'''<div class="feature-card"><div class="feature-label">오늘의 작은 미션</div><div class="feature-value">✨ {dessert['mission']}</div></div>''', unsafe_allow_html=True)
        if st.button("🎲 다시 굴리기", key="roll_again", use_container_width=True):
            st.session_state.dice_result = None
            st.rerun()

    if st.session_state.roll_history:
        st.markdown("### 🧾 최근 뽑은 디저트")
        st.caption("　·　".join(f"{n}. {DESSERTS[n]['emoji']} {DESSERTS[n]['name']}" for n in st.session_state.roll_history))
        if st.button("기록 지우기", key="clear_history"):
            st.session_state.roll_history = []
            st.rerun()

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    if st.button("← 첫 화면으로 돌아가기", key="go_home", use_container_width=True):
        st.session_state.dice_result = None
        st.session_state.show_boom = False
        st.session_state.page = "home"
        st.query_params.clear()
        st.rerun()
