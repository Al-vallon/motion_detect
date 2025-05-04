# 🎯 Motion Detection Web Application

A real-time motion detection system that works in your browser. This application uses computer vision techniques to detect motion from your webcam and displays the results in a web interface.



---

## 🚀 Features

- 📸 Real-time motion detection through your web browser  
- 🖥️ Split-screen interface showing raw and processed video feed  
- 🎯 Visual indicators highlighting detected movement areas  
- 🟢 Status updates showing when motion is detected  
- ⚙️ Adjustable sensitivity for optimized performance  

---

## 🛠️ Technology Stack

- **Backend**: Python, Flask, Flask-SocketIO  
- **Computer Vision**: OpenCV  
- **Frontend**: HTML, CSS, JavaScript  
- **Communication**: WebSockets  
- **Containerization**: Docker  

---

## 🔍 How It Works

1. The browser captures video frames using the built-in camera API  
2. Frames are sent to the server via WebSockets  
3. The server processes each frame with OpenCV:
   - Convert to grayscale and apply Gaussian blur  
   - Calculate frame difference  
   - Apply thresholding and dilation  
   - Detect contours to identify motion areas  
4. When motion is detected:
   - A processed frame with highlighted areas is sent back  
   - The browser displays both original and processed streams  

---

## 🧪 Installation and Setup

### ✅ Prerequisites
- A modern web browser with camera access  

---

## 🐳 Docker Installation
Ensure Docker & Docker Compose are installed.

```bash
# Clone the repository
git clone https://github.com/yourusername/motion-detection-app.git
cd motion-detection-app

# Build and run
docker-compose up --build
```
```bash
http://localhost:5000
```
##⚙️ Configuration
Adjust motion detection sensitivity in app.py:

THRESHOLD_VALUE = 20 — lower = more sensitive

CONTOUR_AREA = 300 — lower = detects smaller movements

blur kernel size — affects noise reduction & precision

## 🧾 Standalone Version
Use motion_detect.py to run detection without the web interface.
```bash
python motion_detect.py
```
## 📄 License
This project is licensed under the MIT License.

## 🙏 Acknowledgments
OpenCV

Flask & Flask-SocketIO

The open-source community 💜
