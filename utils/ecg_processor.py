import cv2
import numpy as np
from scipy.signal import find_peaks
import os

def process_ecg_image(image_path):
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Could not read image")

    # 1. Preprocessing
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Simple thresholding to isolate the darker lines (ECG trace)
    # Using adaptive thresholding to handle uneven lighting
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY_INV, 11, 2)

    # 2. Signal Extraction
    # We'll simplified this by taking the average y-coordinate of the black pixels in each column
    height, width = thresh.shape
    signal = []
    
    for x in range(width):
        column = thresh[:, x]
        black_pixels = np.where(column > 127)[0]
        if len(black_pixels) > 0:
            # Take the median position of black pixels to reduce noise from grid lines
            signal.append(np.median(black_pixels))
        else:
            # Interpolate if no pixel found (basic)
            if len(signal) > 0:
                signal.append(signal[-1])
            else:
                signal.append(height // 2)

    # Convert to numpy array and invert (since y increases downwards in images)
    signal = np.array(signal)
    signal = height - signal 

    # 3. Feature Extraction
    # Find R-peaks (simplified: local maxima with a certain height and distance)
    # We normalize the signal first
    norm_signal = (signal - np.min(signal)) / (np.max(signal) - np.min(signal) + 1e-6)
    peaks, properties = find_peaks(norm_signal, height=0.5, distance=width//20)

    # Calculate Heart Rate
    # Assuming standard paper speed (e.g. 25mm/s) and some pixels-to-mm conversion
    # For a demo, we'll estimate based on the frequency of peaks in the image width
    # Let's assume the image represents roughly 5 seconds of ECG
    if len(peaks) > 1:
        intervals = np.diff(peaks)
        avg_interval = np.mean(intervals)
        # Assuming 100 pixels = 1 second for a 500px wide image (adjust as needed)
        pixels_per_sec = width / 5.0 
        hr = (60 * pixels_per_sec) / avg_interval
    else:
        hr = 0

    # 4. Abnormality Detection
    abnormality = "Normal"
    advice = "Your ECG appears normal. Maintain a healthy lifestyle and regular checkups."
    
    if hr < 60:
        abnormality = "Bradycardia (Low Heart Rate)"
        advice = "Low heart rate detected. If you feel dizzy or faint, please consult a doctor."
    elif hr > 100:
        abnormality = "Tachycardia (High Heart Rate)"
        advice = "High heart rate detected. This could be due to stress, caffeine, or an underlying condition. Consider professional evaluation."
    
    if len(peaks) < 2:
        abnormality = "Arrythmia / Signal Unclear"
        advice = "The system couldn't detect a regular rhythm. Ensure the image is clear and the trace is continuous."

    # 5. ML/Intelligent Logic (Simulation for Student Project)
    # Stress Level based on HR and Heart Rate Variability (HRV)
    if len(peaks) > 2:
        hrv = np.std(np.diff(peaks))
        # High HR + Low HRV usually indicates stress
        stress_score = (hr / 150 * 50) + (10 - hrv/width*100)
    else:
        stress_score = 30 # Default
        
    stress_score = min(max(stress_score, 10), 95) # Clamp 10-95
    
    stress_level = "Low"
    if stress_score > 70: stress_level = "High"
    elif stress_score > 40: stress_level = "Moderate"

    # Confidence Score
    # Based on peak prominence and signal-to-noise ratio simulation
    confidence = min(len(peaks) * 15, 99) if len(peaks) > 0 else 0
    if np.max(norm_signal) - np.min(norm_signal) < 0.2:
        confidence *= 0.5 # Weak signal

    return {
        'waveform': signal.tolist(),
        'heart_rate': round(hr, 1),
        'abnormality': abnormality,
        'stress_level': stress_level,
        'confidence_score': round(confidence, 1),
        'medical_advice': advice
    }
