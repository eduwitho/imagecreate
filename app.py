import streamlit as st
import openai
from io import BytesIO
from PIL import Image
import base64

# 타이틀과 이미지를 모두 중앙에 배치
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(
        "<h1 style='text-align: center; line-height:1.2;'>👨‍🎨이상형<br>그려드립니다.🎨</h1>",
        unsafe_allow_html=True
    )
    st.image("3.png", width=300)

st.write("원하는 이상형을 설명해주세요.")
st.write("너무 긴 설명은 오히려 왜곡된 결과를 낼 수 있으므로, 핵심만 명확히 담는 것이 좋습니다!")

st.markdown(
    """
    <div style="background-color:#e3f2fd; padding: 12px; border-radius: 8px;">
        <span style="font-size: 0.92em;">
            <b>예시 :</b><br>
            - 눈이 크고 쌍꺼풀이가 있는 여성, 피부는 하얗고 청순한 분위기<br>
            - 차가운 도시 남자 스타일, 수트 입고 있는, 차분한 인상
        </span>
    </div>
    """,
    unsafe_allow_html=True
)

# OpenAI API 키 입력 (환경변수나 secrets로 관리 권장)
import os
from dotenv import load_dotenv

load_dotenv()

# --- OpenAI API KEY ---
openai.api_key = os.getenv("OPENAI_API_KEY")

user_input = st.text_input(
    "유명인의 얼굴은 생성하지 않도록 제한되어 있으므로 실존 인물은 언급하지 마세요.🚫",
    value=""
)

img_bytes = None

def make_dalle_prompt(user_text):
    # 한국인 스타일을 강조하여 프롬프트 생성
    return (
        f"A realistic portrait photo of a Korean person described as: {user_text}. "
        "Ultra high quality, studio lighting, natural skin, no celebrities, no text, close-up."
    )

if st.button("이미지 생성하기"):
    if user_input.strip():
        dalle_prompt = make_dalle_prompt(user_input)
        with st.spinner("이미지 생성 중..."):
            response = openai.images.generate(
                model="dall-e-3",
                prompt=dalle_prompt,
                n=1,
                size="1024x1024"
            )
            img_url = response.data[0].url
            img_response = st.session_state.get("img_response")
            if not img_response or img_response["url"] != img_url:
                img_response = {"url": img_url, "bytes": None}
                import requests
                image_data = requests.get(img_url)
                img_bytes = image_data.content
                img_response["bytes"] = img_bytes
                st.session_state["img_response"] = img_response
            else:
                img_bytes = img_response["bytes"]
            image = Image.open(BytesIO(img_bytes))
            st.image(image, caption="생성된 이상형 이미지", use_column_width=True)
    else:
        st.warning("이상형을 입력해주세요.")

# 다운로드 버튼 중앙 하단 배치
if "img_response" in st.session_state and st.session_state["img_response"]["bytes"]:
    img_bytes = st.session_state["img_response"]["bytes"]
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.download_button(
            label="이미지 다운로드",
            data=img_bytes,
            file_name="ideal_type.png",
            mime="image/png",
            use_container_width=True
        )