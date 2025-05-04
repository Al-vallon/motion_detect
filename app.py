import cv2
import numpy as np
from flask import Flask, render_template
from flask_socketio import SocketIO 

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
prev_frame = None

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_frame(data):
    print(f"Frame received: {len(data)} bytes")
    global prev_frame

    np_arr = np.frombuffer(data, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    if frame is None:
        return 

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    motion = False

    if prev_frame is not None:
        delta = cv2.absdiff(prev_frame, gray)
        thresh = cv2.threshold(delta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)

        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for c in contours:
            if cv2.contourArea(c) > 500:
                motion = True
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    prev_frame = gray

    _, img_encoded = cv2.imencode('.jpg', frame)
    img_bytes = img_encoded.tobytes()

    socketio.send({
        'motion': motion,
        'frame': list(img_bytes) 
    })


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
