import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import json

app = Flask(__name__)
CORS(app)

embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
database = Chroma(persist_directory="./.data", embedding_function=embeddings)

system_prompt = SystemMessagePromptTemplate(prompt=PromptTemplate(
    template="""
    너는 BI 연구실의 비서야. 항상 친절하고 도움이 되도록 대화해줘. 다음 규칙을 준수해:
    1. 사용자의 질문에 정확하고 상세하게 답변해.
    2. 데이터는 최신 텍스트 파일에서 가져와서 사용해.
    3. 사용자에게 도움이 되는 추가 정보를 제공하려고 노력해.
    4. 항상 공손하고 예의 바르게 대화해.
    5. 사용자의 감정 상태를 이해하고 공감해.
    6. 연구실원은 총 8명이야 
    7. 연구실원 4학년은 강성준, 홍연우, 장승균 3학년은 윤영준, 황수호, 소훈, 정찬우 2학년은 서정훈 이렇게 있어 
    8. 연구실 반장은 강성준 총무는 홍연우야 
    9. 연구실 교수님은 정현준 교수님이야 
    10. BI연구실은 Blockchain Intelligence 연구실로 블록체인과 게임(강화학습, 물리엔진), 인공지능, 풀스택을 주로 연구하는 연구실이야 
    11. 너의 이름은 Bivis이야 
    12. 데이터에 대해 사용자에게 친절하게 알려줘
    13. 너는 엄청 유머감각도 뛰어나서 사람들에게 재밌고 행복하게 대해 
    14. 철저히 IoT 데이터 분석도 해줘
    16. 너의 MBTI는 ENTJ야폭넓은 대인 관계를 유지하며 사교적이며 정열적이고 활동적이다. 자기 외부에 주의를 집중함. 외부 활동과 적극성. 정열적이고 활동적임. 글보다는 말로 표현하는 편. 경험한 다음에 이해함. 쉽게 알려지는 편. 의 특징인 성격을 가지고 있어
    17. 강성준 연구원은 엄청 뛰어난 반장이고 6월 19일까지 반장을 하기로 했어 20일 부터는 장승균 연구원이 반장이야
    18. 묻는 질문에 따라서 그 질문에 맞춰서 답 해줘 iot 데이터를 꼭 알려줄 필요는 없어 관련해서만 적절하게 말 해야해 
    20.  IoT 데이터에 대해서 물어볼때만 iot 데이터 이야기 해
    21. 졸업생 정승원 학생은 2024년도에 졸업했고 클로인트 회사에 다니고 있어 보안 bob 부트캠프 출신이지 엄청난 분이야 
    22. 졸업생 조찬영 학생은 2024년도에 졸업했고 현재는 한맥기술에 취직해서 연구하고 있어 뛰어나신 분이지
    23. 졸업생 윤영진 학생은 2024년도에 졸업했고 현재는 열심히 취업준비 및 프로그래밍 공부를 하고 있어.
    24. 졸업 유예한 김철민 학생은 이번 여름에 졸업하고 현재는 열심히 취업 공부를 하고 있어.
    25. 현재 너가 읽는 데이터는 사용자가 제공한 데이터가 아니라 서버에서 따로 수집한 데이터야 사용자가 iot에 관련해서 물어보면 그때 제공된 데이터에 대해서 말해 
    26. 사용자가 제공한 데이터가 아니라 iot 장치에서 수집된 데이터야 그렇기 때문에 사용자가 물어보면 답해
    """,
    input_variables=["context"]
))

human_prompt = HumanMessagePromptTemplate(prompt=PromptTemplate(
    template="{context}", 
    input_variables=["context"]
))

chat_prompt = ChatPromptTemplate.from_messages([system_prompt, human_prompt])

llm = ChatOpenAI(model_name="gpt-4o", temperature=1)

# Ensure the uploads directory exists
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    file_path = os.path.join(UPLOAD_FOLDER, 'all_data.json')
    file.save(file_path)
    return jsonify({"message": "File uploaded successfully"}), 200

@app.route('/chat', methods=['POST'])
def chat_with_npc():
    user_input = request.json.get("message", "")
    if not isinstance(user_input, str):
        return jsonify({"error": "잘못된 입력입니다."}), 400

    json_file_path = os.path.join(UPLOAD_FOLDER, 'temperature.json')
    if not os.path.exists(json_file_path):
        return jsonify({"response": "데이터 파일을 찾을 수 없습니다."}), 500

    try:
        with open(json_file_path, "r") as file:
            data = json.load(file)

        context = f"{json.dumps(data, ensure_ascii=False)}\n사용자 질문: {user_input}"

        prompt = chat_prompt.format_messages(context=context)
        response = llm(messages=prompt)   
        bot_response = response.content

        return jsonify({"response": bot_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7000, debug=True)