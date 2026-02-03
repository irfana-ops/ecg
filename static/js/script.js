document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const btnAnalyze = document.getElementById('btn-analyze');
    const fileInfo = document.getElementById('file-info');
    const filenameDisplay = document.getElementById('filename-display');
    const loader = document.getElementById('loader');
    const uploadContent = document.getElementById('upload-content');
    const resultsCard = document.getElementById('results-card');
    
    let chart = null;

    // Trigger file input
    dropZone.addEventListener('click', () => fileInput.click());

    // Drag and Drop
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        if (e.dataTransfer.files.length) {
            handleFileSelect(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
            handleFileSelect(e.target.files[0]);
        }
    });

    function handleFileSelect(file) {
        if (!file.type.startsWith('image/')) {
            alert('Please select an image file');
            return;
        }
        
        filenameDisplay.textContent = file.name;
        fileInfo.style.display = 'block';
        btnAnalyze.disabled = false;
        
        // Visual feedback
        dropZone.style.borderColor = 'var(--accent)';
    }

    btnAnalyze.addEventListener('click', async () => {
        const file = fileInput.files[0] || (filenameDisplay.textContent ? {fake:true} : null);
        if (!file) return;

        // Show Loader
        loader.style.display = 'block';
        uploadContent.style.opacity = '0.5';
        btnAnalyze.disabled = true;

        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.error) {
                alert('Error: ' + data.error);
            } else {
                displayResults(data);
            }
        } catch (err) {
            console.error(err);
            alert('An error occurred while processing the image.');
        } finally {
            loader.style.display = 'none';
            uploadContent.style.opacity = '1';
            btnAnalyze.disabled = false;
        }
    });

    function displayResults(data) {
        resultsCard.style.display = 'block';
        resultsCard.scrollIntoView({ behavior: 'smooth' });

        // Update Text Fields
        document.getElementById('val-hr').textContent = `${data.heart_rate} BPM`;
        document.getElementById('val-abnormality').textContent = data.abnormality;
        document.getElementById('val-stress').textContent = data.stress_level;
        document.getElementById('val-confidence').textContent = `${data.confidence_score}%`;
        document.getElementById('val-advice').textContent = data.medical_advice;

        // Styling based on abnormality
        const hrVal = document.getElementById('val-hr');
        if (data.abnormality !== 'Normal') {
            hrVal.classList.add('warning');
        } else {
            hrVal.classList.remove('warning');
            hrVal.classList.add('highlight');
        }

        // Render Chart
        renderChart(data.waveform);
    }

    function renderChart(waveform) {
        const ctx = document.getElementById('ecgChart').getContext('2d');
        
        if (chart) {
            chart.destroy();
        }

        // Downsample for better performance if signal is too long
        const downsampled = waveform.length > 1000 ? 
            waveform.filter((_, i) => i % 2 === 0) : waveform;

        chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: new Array(downsampled.length).fill(''),
                datasets: [{
                    label: 'Digital ECG Waveform',
                    data: downsampled,
                    borderColor: '#10b981',
                    borderWidth: 2,
                    pointRadius: 0,
                    tension: 0.2,
                    fill: false
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: { display: false },
                    y: { 
                        display: true,
                        grid: { color: 'rgba(255, 255, 255, 0.1)' },
                        ticks: { color: 'rgba(255, 255, 255, 0.5)' }
                    }
                },
                animation: {
                    duration: 2000,
                    easing: 'easeInOutQuart'
                }
            }
        });
    }
});
