const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const statusText = document.getElementById('motion');
const motionFrame = document.getElementById('motionFrame');

// Initialize Socket.IO connection
const socket = io();

// Handle detection messages
socket.on('detection', (data) => {
    // Update status
    statusText.textContent = data.motion ? "Motion detected!" : "No motion";
    statusText.style.color = data.motion ? "red" : "green";

    // If a frame is received, display it
    if (data.frame) {
        motionFrame.src = `data:image/webp;base64,${data.frame}`;
    }
});

// Request camera access
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
        video.play();
    })
    .catch(err => {
        console.error("Camera access error: ", err);
    });

// Function to send frames to the server
function sendFrame() {
    if (video.readyState === video.HAVE_ENOUGH_DATA) {
        // Set canvas size to match video
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        
        // Draw video image on canvas
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        // Get image data in JPEG format
        canvas.toBlob(blob => {
            const reader = new FileReader();
            reader.onload = () => {
                // Send binary data to server
                socket.emit("message", reader.result);
            };
            reader.readAsArrayBuffer(blob);
        }, 'image/webp', 0.8);  // Quality 0.8 to reduce size
    }
}

// Send frames every 200ms to improve responsiveness
setInterval(sendFrame, 200);
