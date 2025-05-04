const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const statusText = document.getElementById('motion');

const socket = io("http://localhost:5000");

socket.on("message", (data) => {
    console.log(data.motion, 'data received from server');
    statusText.textContent = data.motion ? "Mouvement détecté !" : "Aucun";
    statusText.style.color = data.motion ? "red" : "green";

    if (data.frame) {
        const uint8Arr = new Uint8Array(data.frame);
        const blob = new Blob([uint8Arr], { type: 'image/jpeg' });
        document.getElementById('motionFrame').src = URL.createObjectURL(blob);
    }
});


navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
    video.srcObject = stream;
});

setInterval(() => {
    if (video.readyState === video.HAVE_ENOUGH_DATA) {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        canvas.toBlob(blob => {
        const reader = new FileReader();
        reader.onload = () => {
            const arrayBuffer = reader.result;
            socket.emit("message", arrayBuffer);
        };
        reader.readAsArrayBuffer(blob);
        }, 'image/jpeg');
    }
}, 500);
