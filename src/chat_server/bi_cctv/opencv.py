import cv2
import streamlit as st
import numpy as np
from PIL import Image
from io import BytesIO
import base64

logo = Image.open("../assets/img/bi.png")
buffered = BytesIO()
logo.save(buffered, format="PNG")
logo_base64 = base64.b64encode(buffered.getvalue()).decode()

st.set_page_config(
    page_title="BI-LAB CCTV",
    page_icon=logo,
    layout="wide",
)

st.markdown(
    f"""
    <style>
    .title-container {{
        display: flex;
        align-items: center;
        justify-content: center;
        margin-top: 20px;
    }}
    .title-text {{
        font-size: 2.5rem;
        font-weight: bold;
        margin-left: 10px;
    }}
    .logo {{
        height: 50px;
        width: 50px;
    }}
    .count-box {{
        text-align: center;
        font-size: 1.5rem;
        margin-top: 20px;
        color: #ff6347;
    }}
    .webcam-frame {{
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }}
    .button-container {{
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="title-container">
        <img src="data:image/png;base64,{logo_base64}" class="logo">
        <div class="title-text">BI-LAB CCTV</div>
    </div>
    """,
    unsafe_allow_html=True
)

FRAME_WINDOW = st.image([])
count_placeholder = st.markdown("<div class='count-box'>현재 인원 수: 0</div>", unsafe_allow_html=True)

net = cv2.dnn.readNet("yolov4-tiny.weights", "yolov4-tiny.cfg")
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

def detect_people():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        height, width, channels = frame.shape

        blob = cv2.dnn.blobFromImage(frame, 0.00392, (320, 320), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5 and classes[class_id] == 'person':
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = (0, 255, 0)
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        FRAME_WINDOW.image(frame[:, :, ::-1])
        count_placeholder.markdown(f"<div class='count-box'>현재 인원 수: {len(indexes)}</div>", unsafe_allow_html=True)

    cap.release()

st.markdown(
    f"""
    <div class="button-container">
        <button onclick="detect_people()">Start Webcam</button>
    </div>
    """,
    unsafe_allow_html=True
)

detect_people()