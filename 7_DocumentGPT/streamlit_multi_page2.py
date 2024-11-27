import streamlit as st

st.set_page_config(
    page_title="Fullstack GPT Home",
    page_icon="🤖"
)

st.title("Fullstack GPT Home")

# ============= page 들을 추가해 보자 =============
# pages 라는 이름의 '폴더'를 만들어야 한다.(pages 라는 이름을 반드시 지켜야 한다.)
# why? Streamlit이 pages 폴더를 찾기 때문이다.

# 아래와 같은 작명법으로 page 들의 순서를 정할수도 있다.
# 01_DocumentGPT
# 02_QuizGPT
# 03_PrivateGPT