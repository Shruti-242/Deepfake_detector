document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('fileInput');
    const predictionResult = document.getElementById('prediction-result');
    const confidenceLevel = document.getElementById('confidence-level');

    fileInput.addEventListener('change', async () => {
        const file = fileInput.files[0];
        if (file) {
            predictionResult.textContent = 'Analyzing...';
            confidenceLevel.textContent = '--'; // Reset confidence

            const formData = new FormData();
            formData.append('file', file);

            try {
                // Replace 'YOUR_BACKEND_ENDPOINT' with the actual URL of your deepfake detection API
                const response = await fetch('YOUR_BACKEND_ENDPOINT', {
                    method: 'POST',
                    body: formData,
                });

                if (response.ok) {
                    const data = await response.json();
                    predictionResult.textContent = data.prediction; // Assuming your backend returns a 'prediction' field
                    confidenceLevel.textContent = `${(data.confidence * 100).toFixed(2)}%`; // Assuming a 'confidence' field (0-1)
                } else {
                    predictionResult.textContent = 'Error processing file.';
                    console.error('Error from backend:', response.status);
                }
            } catch (error) {
                predictionResult.textContent = 'Network error.';
                console.error('Network error:', error);
            }
        } else {
            predictionResult.textContent = 'No file selected.';
            confidenceLevel.textContent = '--';
        }
    });
});