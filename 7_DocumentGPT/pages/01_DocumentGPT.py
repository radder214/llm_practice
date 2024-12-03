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
st.title("Document GPT")
st.markdown("""
    ## Welcome!
    ##### Use this chatbot to ask questions to an AI about your files!
    ##### Upload your files on the sidebar.
""")

# @st.cache_data ==> decorator
    # 사용자의 질문이 들어올 때 마다 load, split, embedding 등을 할 수는 없다.
    # 넘겨받은 파일이 동일하다면 해당 함수를 재실행하지 않는다.
    # 재실행하는 대신에 기존에 반환했던 값을 다시 반환한다.
# @st.cache_data(show_spinner="Embedding file...") ==> 오류 발생해서 우선 st.cache_resource 임시로 사용 [24.12.01]
@st.cache_resource(show_spinner="Embedding file...")
def embed_file(file):
    # upload 된 파일 저장 ==> UnstructuredFileLoader 에게 파일 위치를 넘겨주기 위해
    file_content = file.read()
    file_path    = f"./cache/files/{file.name}" # 파일 저장 경로

    # file_content 내용을 file_path 에 저장
        # open(file_path, ...) ==> file_path에 있는 파일을 열어라
        # wb = 파일을 binary로 write
    with open(file_path, mode="wb") as uploaded_file:
        uploaded_file.write(file_content)

    # embedding 한 것을 저장할 경로 For Cache
    cache_dir = LocalFileStore(f"./cache/embeddings/{file.name}")
    
    # text splitter 설정
    splitter = CharacterTextSplitter.from_tiktoken_encoder(
        separator     = "\n",
        chunk_size    = 600,
        chunk_overlap = 100
    )

    # 파일 load and split
    # [as-is]
    # loader = UnstructuredFileLoader(file_path)
    # [to-be]
    loader = UnstructuredLoader(file_path)
    docs = loader.load_and_split(text_splitter=splitter)

    # embedding
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

    # vector Store에서 질문과 관련된 문서 가져오기
    retriever = vectorStore.as_retriever(
        search_type="similarity",   # 유사도 검색 방식
        search_kwargs={"k": 4}      # 검색 관련 추가 파라미터
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



# 사용자가 본인 파일 upload
with st.sidebar:
    file = st.file_uploader(
        label= "Upload a .txt, .pdf, .docx file",
        type = ["txt", "pdf", "docx"]
    )

if file:
    # 사용자가 upload 한 파일을 기반으로 한 retriever를 가져온다.
    retriever = embed_file(file)
    # 사용자에게 처음으로 보여줄 메시지(그냥 의미 없음, 껍데기 같은 역할)
    send_message("I'm ready! Ask away!", "ai", False)
    # 채팅 기록 화면에 뿌리기
    paint_history()
    
    # 사용자 질문 받기
    message = st.chat_input("Ask anything about your file")
    if message:
        send_message(message, "human")
        # 사용자 질문을 retriever에 던져서 질문과 관련된 Document를 가져온다.
        docs = retriever.invoke(message)
        # 각 Document의 page_content를 합쳐서 템플릿에 넣는다. using List Comprehension
        docs = "\n\n".join(document.page_content for document in docs) # "🔥".join(["1", "2", "3"]) --> 1🔥2🔥3
        st.write(docs)
else :
    # 1. 기존에 upload 한 파일을 더 이상 사용하지 않고, 다른 파일을 upload 후 사용하고 싶을 때
    # 2. 화면에 처음 들어 왔을 때에도 아래 코드가 실행된다.(file 변수의 값이 없으므로)
    st.session_state.messages = [] # session_state 초기화


# [Document 구조]
# Document(
#     metadata={
#         'source': './cache/files/chapter_one.txt',
#         'last_modified': '2024-12-03T19:07:35',
#         'languages': ['eng'],
#         'file_directory': './cache/files',
#         'filename': 'chapter_one.txt',
#         'filetype': 'text/plain',
#         'parent_id': '71fe05d11862faa92ae87089d5b28417',
#         'category': 'NarrativeText',
#         'element_id': '48b982806c63bf69d86ee934268bc872'
#     },
#     page_content="Winston turned round abruptly. He had set his features into the expression of quiet optimism which it was advisable to wear when facing the telescreen. He crossed the room into the tiny kitchen. By leaving the Ministry at this time of day he had sacrificed his lunch in the canteen, and he was aware that there was no food in the kitchen except a hunk of dark-coloured bread which had got to be saved for tomorrow's breakfast. He took down from the shelf a bottle of colourless liquid with a plain white label marked VICTORY GIN. It gave off a sickly, oily smell, as of Chinese ricespirit. Winston poured out nearly a teacupful, nerved himself for a shock, and gulped it down like a dose of medicine."
# )