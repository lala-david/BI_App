import streamlit as st
import requests
import json
import os
import base64

st.markdown("""
    <style>
        .header {
            background-color: #FF8C00; 
            padding: 10px;
            text-align: center;
            color: white;
            font-size: 14px;
            font-weight: bold;
            border-radius: 5px 5px 0 0;
        }
        .message-container {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            width: 80%;
        }
        .user-message, .bot-message {
            display: flex;
            align-items: center;
            padding: 10px;
            border-radius: 20px;
            margin: 10px;
            width: 70%;
        }
        .user-message {
            background-color: #FFD580; 
            margin-left: auto;
            flex-direction: row-reverse;
            border: 1px solid #000000;
        }
        .bot-message {
            background-color: #FFFFFF; 
            border: 1px solid #000000;  
            margin-right: auto;
        }
        .profile-pic {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            margin: 0 10px;
        }
        .message-container::-webkit-scrollbar {
            width: 10px;
        }
        .message-container::-webkit-scrollbar-thumb {
            background: #FF8C00;  
            border-radius: 10px;
        }
        .message-container::-webkit-scrollbar-track {
            background: #FFF5E1;  
        }
        .text-input {
            border: 2px solid #FF8C00;  
            border-radius: 10px;
            padding: 10px;
            width: calc(100% - 24px);
            margin: 12px 0;
        }
        .send-button {
            background-color: #FF8C00; 
            color: white;
            border: none;
            border-radius: 10px;
            padding: 10px 20px;
            cursor: pointer;
        }
        .send-button:hover {
            background-color: #FFA500; 
        }
    </style>
""", unsafe_allow_html=True)

# Add the header
st.markdown('<div class="header">Welcome to Bivis World!</div>', unsafe_allow_html=True)

st.title("Bivis")

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

json_file_path = 'uploads/temperature.json'

def upload_file(json_file_path):
    if os.path.exists(json_file_path):
        with open(json_file_path, 'rb') as f:
            files = {'file': ('temperature.json', f, 'application/json')}
            response = requests.post("http://../upload", files=files)

        if response.status_code == 200:
            st.success("자동 파일 업로드 및 처리 완료.")
            return True
        else:
            st.error(f"자동 파일 업로드 중 오류가 발생했습니다. 상태 코드: {response.status_code}")
            st.error(response.text)
            return False
    else:
        st.warning("자동 업로드할 JSON 파일이 존재하지 않습니다.")
        return False

upload_successful = upload_file(json_file_path)

st.write("Hello! Bivis Lab Bot!")

def load_image_as_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

if 'user_image' not in st.session_state:
    st.session_state.user_image = load_image_as_base64("./assets/img/user.png")

if 'bot_image' not in st.session_state:
    st.session_state.bot_image = load_image_as_base64("./assets/img/wepo.jpg")

def send_message(user_input):
    if user_input:
        if upload_successful:
            response = requests.post(
                "http://../chat",
                json={"message": user_input}
            )
            
            if response.status_code == 200:
                bot_response = response.json().get("response")
 
                st.session_state['messages'].append({"role": "user", "content": user_input})
                st.session_state['messages'].append({"role": "bot", "content": bot_response})
                st.experimental_rerun()
            else:
                st.error("오류가 발생했습니다. 다시 시도해 주세요.")
                st.error(f"상태 코드: {response.status_code}")
                st.error(response.text)
        else:
            st.warning("JSON 파일 업로드가 성공적으로 완료되지 않았습니다.")
    else:
        st.warning("질문을 입력하세요.")

 
st.write('<div class="message-container">', unsafe_allow_html=True)
for message in st.session_state['messages']:
    if message["role"] == "user":
        st.markdown(f'''
            <div class="user-message">
                <img src="data:image/png;base64,{st.session_state.user_image}" class="profile-pic">
                <div>{message["content"]}</div>
            </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown(f'''
            <div class="bot-message">
                <img src="data:image/png;base64,{st.session_state.bot_image}" class="profile-pic">
                <div>{message["content"]}</div>
            </div>
        ''', unsafe_allow_html=True)
st.write('</div>', unsafe_allow_html=True)
 
with st.form(key='message_form', clear_on_submit=True):
    user_input = st.text_input("질문을 입력하세요", key="text_input", max_chars=1000, placeholder="입력하세요 요기에...")
    submit_button = st.form_submit_button(label='질문 보내기')

if submit_button:
    send_message(user_input)
