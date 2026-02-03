# ECG Digitize: Paper to Digital Health Assessment

A web-based system to convert scanned ECG paper images into digital signals, perform feature extraction, and provide health assessments.

## Features
- **Image Processing**: Extracts digital signals from scanned ECG papers using OpenCV.
- **Waveform Visualization**: Interactive digital waveform display using Chart.js.
- **Signal Analysis**: 
  - Peak detection (R-peaks) for Heart Rate calculation.
  - Abnormality detection (Bradycardia, Tachycardia, Normal).
- **Intelligent Logic**: 
  - Stress level estimation based on HR and Signal Variability.
  - Signal confidence score based on trace clarity.
- **Medical Advice**: Rule-based medical guidance and lifestyle suggestions.
- **Modern UI**: Dark mode, glassmorphism design, and smooth animations.

## Tech Stack
- **Backend**: Python Flask
- **Frontend**: HTML5, Vanilla CSS, JavaScript
- **Libraries**: OpenCV, NumPy, SciPy, Chart.js, Lucide Icons

## Setup Instructions
1. **Activate Virtual Environment**:
   ```bash
   .\venv\Scripts\activate
   ```
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Application**:
   ```bash
   python app.py
   ```
4. **Access the Website**: Open `http://127.0.0.1:5000` in your browser.

## Testing
- You can use the **Download Sample ECG** link on the website to get a synthetic ECG image for testing.
- Upload the image to see the digitization and analysis in action.

## Project Structure
- `app.py`: Flask application routes.
- `utils/ecg_processor.py`: Core logic for signal extraction and analysis.
- `templates/`: HTML templates.
- `static/`: CSS, JS, and uploaded images.
- `utils/generate_sample.py`: Script to generate testing data.
