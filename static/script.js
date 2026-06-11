document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('audioFile');
    const uploadText = document.getElementById('uploadText');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const error = document.getElementById('error');
    const result = document.getElementById('result');
    const prediction = document.getElementById('prediction');
    const spectrogram = document.getElementById('spectrogram');
    const uploadArea = document.querySelector('.upload-area');

    // File upload handling
    fileInput.addEventListener('change', handleFileSelect);
    
    // Analyze button click handler
    analyzeBtn.addEventListener('click', handleAnalyze);
    
    // Drag and drop handling
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);

    function handleFileSelect(e) {
        const file = e.target.files[0];
        if (file) {
            const allowedTypes = ['audio/mp3', 'audio/wav', 'audio/aac'];
            if (allowedTypes.includes(file.type)) {
                uploadText.textContent = file.name;
                analyzeBtn.disabled = false;
                error.style.display = 'none';
            } else {
                showError('Please upload an MP3, WAV, or AAC file.');
                resetUpload();
            }
        }
    }

    async function handleAnalyze() {
        if (!fileInput.files[0]) {
            showError('Please select an audio file first.');
            return;
        }

        setLoading(true);
        error.style.display = 'none';
        result.style.display = 'none';

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        try {
            const response = await fetch('/recognize', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                prediction.textContent = data.data.result;
                if (data.data.spectrogram) {
                    spectrogram.src = 'data:image/png;base64,' + data.data.spectrogram;
                    spectrogram.style.display = 'block';
                } else {
                    spectrogram.style.display = 'none';
                }
                result.style.display = 'block';
            } else {
                throw new Error(data.message || 'Failed to analyze audio');
            }
        } catch (err) {
            showError(err.message);
        } finally {
            setLoading(false);
        }
    }

    function handleDragOver(e) {
        e.preventDefault();
        uploadArea.style.borderColor = '#3b82f6';
    }

    function handleDragLeave(e) {
        e.preventDefault();
        uploadArea.style.borderColor = '#4b5563';
    }

    function handleDrop(e) {
        e.preventDefault();
        uploadArea.style.borderColor = '#4b5563';
        
        const file = e.dataTransfer.files[0];
        if (file) {
            fileInput.files = e.dataTransfer.files;
            handleFileSelect({ target: fileInput });
        }
    }

    function showError(message) {
        error.textContent = message;
        error.style.display = 'block';
    }

    function setLoading(loading) {
        analyzeBtn.disabled = loading;
        document.querySelector('.loading').style.display = loading ? 'flex' : 'none';
        document.querySelector('.button-text').style.display = loading ? 'none' : 'inline';
    }

    function resetUpload() {
        uploadText.textContent = 'Click to upload or drag & drop your audio file';
        fileInput.value = '';
        analyzeBtn.disabled = true;
        spectrogram.style.display = 'none';
    }
});
