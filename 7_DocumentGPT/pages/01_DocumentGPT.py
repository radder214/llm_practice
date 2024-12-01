import streamlit as st
# [as-is]
from langchain.document_loaders import UnstructuredFileLoader
# [to-be]
from langchain_unstructured     import UnstructuredLoader
from langchain.text_splitter    import CharacterTextSplitter
from langchain_openai           import OpenAIEmbeddings
from langchain.vectorstores     import Chroma, FAISS
from langchain.embeddings       import CacheBackedEmbeddings
from langchain.storage          import LocalFileStore

st.set_page_config(page_title="Document GPT", page_icon="📖")

# @st.cache_data ==> decorator
    # 사용자의 질문이 들어올 때 마다 load, split, embedding 등을 할 수는 없다.
    # 넘겨받은 파일이 동일하다면 해당 함수를 재실행하지 않는다.
    # 재실행하는 대신에 기존에 반환했던 값을 다시 반환한다.
# @st.cache_data(show_spinner="Embedding file...") ==> 오류 발생해서 우선 st.cache_resource 임시로 사용 [24.12.01]
@st.cache_resource(show_spinner="Embedding file...")
def embed_file(file):
    # 2.
    # upload 된 파일 저장 ==> UnstructuredFileLoader 에게 파일 위치를 넘겨주기 위해
    file_content = file.read()
    file_path    = f"./cache/files/{file.name}" # 파일 저장 경로

    # 3. file_content 내용을 file_path 에 저장
        # open(file_path, ...) ==> file_path에 있는 파일을 열어라
        # wb = 파일을 binary로 write
    with open(file_path, mode="wb") as uploaded_file:
        uploaded_file.write(file_content)

    # 4. embedding 한 것을 저장할 경로 For Cache
    cache_dir = LocalFileStore(f"./cache/embeddings/{file.name}")
    
    # 5. text splitter 설정
    splitter = CharacterTextSplitter.from_tiktoken_encoder(
        separator     = "\n",
        chunk_size    = 600,
        chunk_overlap = 100
    )

    # 6. 파일 load and split
    # [as-is]
    # loader = UnstructuredFileLoader(file_path)
    # [to-be]
    loader = UnstructuredLoader(file_path)
    docs = loader.load_and_split(text_splitter=splitter)

    # 7. embedding
    embedding = OpenAIEmbeddings()
    cached_embedding = CacheBackedEmbeddings.from_bytes_store(
        underlying_embeddings    = embedding,
        document_embedding_cache = cache_dir
    )
    # Chroma로 하니까 해당 단계에서 Error가 발생해서 FAISS로 변경
    vectorStore = FAISS.from_documents(
        documents = docs,
        embedding = cached_embedding
    )

    # 8. vector Store에서 질문과 관련된 문서 가져오기
    retriever = vectorStore.as_retriever(
        search_type="similarity",   # 유사도 검색 방식
        search_kwargs={"k": 6}      # 검색 관련 추가 파라미터
                                        # "k": 6 ==> 6개의 검색결과 반환
    )
    return retriever

# 생성된 메시지를 화면에 뿌린다 & st.session_state.messages에 저장
def send_message(message, role, save=True):
    with st.chat_message(role):
        st.markdown(message)
    if save:
        st.session_state.messages.append({
            "message" : message,
            "role"    : role
        })

# st.session_state.messages에 담겨있는 채팅 기록을 화면에 뿌린다.
def paint_history():
    for message in st.session_state.messages:
        send_message(message["message"], message["role"], False)

st.title("Document GPT")

st.markdown("""
    ## Welcome!
    ##### Use this chatbot to ask questions to an AI about your files!
    ##### Upload your files on the sidebar.
""")

# 1.
# 사용자가 본인의 파일 upload
with st.sidebar:
    file = st.file_uploader(
        label= "Upload a .txt, .pdf, .docx file",
        type = ["txt", "pdf", "docx"]
    )

if file:
    # 1-1. 질문하고 대답을 받는다.
    retriever = embed_file(file)
    send_message("I'm ready! Ask away!", "ai", False)
    paint_history()
    
    message = st.chat_input("Ask anything about your file")
    if message:
        send_message(message    , "human")
        send_message("ai_answer", "ai")
else :
    # 1. 기존에 upload 한 파일을 더 이상 사용하지 않고 다른 파일을 upload 후 사용하고 싶을 때
    # 2. 화면에 처음 들어 왔을 때에도 아래 코드가 실행된다.(file 변수의 값이 없으므로)
    st.session_state.messages = [] # session_state 초기화