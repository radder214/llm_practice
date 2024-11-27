import streamlit as st
from datetime import datetime

# 데이터가 변경되는 모든 경우에 python 파일 '전체가 다시 실행'된다.
# ajax 처럼 특정 부분만 refresh 되는게 아니라 전체 페이지가 refresh 된다.

# 데이터가 변경될 때마다 refresh 된다.
st.title(datetime.today().strftime("%H:%M:%S"))

# 1
model = st.selectbox(
    "Choose your model",
    ("GPT-3", "GPT-4")
)
st.write(model)
# refresh 특징을 이용해 특정 widget을 숨기거나 보여줄 수 있다.
if model == "GPT-3":
    st.write("cheap")
    st.button("GPT-3 Go")
else :
    st.write("not cheap")
    st.button("GPT-4 Go")

# 2
name = st.text_input("What is Your Name?")
st.write(name)

# 3
value = st.slider("temperature", min_value=0.1, max_value=1.0, step=0.1)
st.write(value)