import cv2 # type: ignore[import]
import numpy as np # type: ignore[import]
from flask import Flask, render_template # type: ignore[import]
from flask_socketio import SocketIO, send, emit # type: ignore[import]
import base64

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
prev_frame = None

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_frame(data):
    global prev_frame
    
    # Correct decoding of the received message
    if isinstance(data, str):
        try:
            header, encoded = data.split(",", 1)
            data = base64.b64decode(encoded)
        except:
            print("Error: incorrect data format")
            return
    
    try:
        np_arr = np.frombuffer(data, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        
        if frame is None:
            print("Error: frame not decodable")
            return

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        motion = False
        if prev_frame is not None:
            delta = cv2.absdiff(prev_frame, gray)
            thresh = cv2.threshold(delta, 20, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=3)
            
            contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for c in contours:
                if cv2.contourArea(c) > 300:  
                    motion = True
                    break
            
            # Draw rectangles on contours
            if motion:
                for c in contours:
                    if cv2.contourArea(c) > 300:
                        (x, y, w, h) = cv2.boundingRect(c)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                # Encode the image to send it
                ret, buffer = cv2.imencode('.jpg', frame)
                frame_bytes = buffer.tobytes()
                
                # Convert to base64 for sending via Socket.IO
                frame_base64 = base64.b64encode(frame_bytes).decode('utf-8')
                socketio.emit('detection', {'motion': motion, 'frame': frame_base64})
            else:
                socketio.emit('detection', {'motion': motion})
                
        # Update previous frame
        prev_frame = gray
        
    except Exception as e:
        print(f"Error during detection: {e}")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
