import streamlit as st
from langchain.prompts import PromptTemplate

# st.write --> 넘겨준 것이 무엇이든 화면에 나타낸다.
st.write("hello")
st.write([1, 2, 3, 4])
st.write({"x" : 1, "y" : 2})
st.write(PromptTemplate)
st.write(PromptTemplate.from_template("xxxx"))

st.selectbox(
    "Choose your model",
    ("GPT-3", "GPT-4"),
)