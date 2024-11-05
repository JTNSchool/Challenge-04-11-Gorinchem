// Wait for the DOM to be fully loaded
window.onload = function() {
    // Access the video element and canvas
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');

    // Request access to the webcam
    navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
            video.srcObject = stream;  // Set the video source to the stream
            video.play(); // Start playing the video stream
        })
        .catch((err) => {
            console.error("Error accessing webcam: " + err);
        });

    // Capture image when button is clicked
    document.getElementById('captureButton').addEventListener('click', function() {
        context.drawImage(video, 0, 0, canvas.width, canvas.height); // Draw the video frame to the canvas
        const imageUrl = canvas.toDataURL('image/png'); // Get the image data as a PNG

        // Display the captured image on the page
        const photoElement = document.getElementById('photo');
        photoElement.src = imageUrl;
        photoElement.style.display = 'block'; // Show the image

        // Send the image data to the server
        fetch('http://127.0.0.1:5001/upload-image', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image: imageUrl })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error uploading image:', error);
        });
    });
};
