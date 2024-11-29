import streamlit as st

st.title("title")

# sidebar 에서 데이터가 변경돼도 전체 페이지가 refresh 되는 것은 동일하다.
# sidebar 포함 전체 페이지가 '다시 실행'된다는 말이다.

# ======== sidebar 제작 방법 1(잘 사용하지 않는 방법) ========
# st.sidebar.title("sidebar title")
# st.sidebar.text_input("What is your name?")


# ======== sidebar 제작 방법 2(with 키워드 사용) ========
with st.sidebar: # with block 안에 적는 모든 widget들은 sidebar 안에 들어간다.
    st.title("sidebar title")
    st.text_input("What is your name?")
    st.slider(label="temperature", min_value=0.1, max_value=0.9)

# ===================================================================
# tab_one, tab_two, tab_three 각각에 내용을 추가해보자
tab_one, tab_two, tab_three = st.tabs(["A", "B", "C"])
with tab_one:
    st.write("A tab Pages")
with tab_two:
    st.write("B tab Pages")
with tab_three:
    st.write("C tab Pages")