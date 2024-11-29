import streamlit as st
import time

st.set_page_config(page_title="Document GPT", page_icon="📖")
st.title("Document GPT")

# ========== streamlit의 Chat Element에 대해 알아보자 ==========
# with st.chat_message("human"):
#     # 해당 block 안에 들어가는 모든 것은 사람이 작성한 것이 된다.
#     st.write("Hello")

# with st.chat_message("ai"):
#     # 해당 block 안에 들어가는 모든 것은 ai가 작성한 것이 된다.
#     st.write("how are you")

# with st.status("Embedding file...", expanded=True) as status:
#     time.sleep(2)
#     st.write("Getting the file")
#     time.sleep(2)
#     st.write("Embedding the file")
#     time.sleep(2)
#     st.write("Caching the file")
#     status.update(label="Error", state="error")

# ========== AI와 사람 간의 가상 대화를 만들어보자 to 메시지 저장 로직 이해 With session_state ==========
# st.session_state.messages 생성
if "messages" not in st.session_state:
    st.session_state.messages = []

def send_message(message, role, save=True): # save=True --> default parameter
    with st.chat_message(role):
        st.write(message)
    if save:
        st.session_state.messages.append({
            "message" : message,
            "role"    : role
        })

# session_state를 이용해 대화 기록 화면에 뿌리기
for message in st.session_state.messages:
    send_message(message["message"], message["role"], False)

message = st.chat_input("Send a message to the AI")
if message:
    send_message(message, "human")
    time.sleep(2)
    send_message(f"You said: {message}", "ai")
