import numpy as np
import cv2
import os

def generate_sample_ecg(output_path):
    # Image dimensions
    width, height = 800, 400
    img = np.ones((height, width, 3), dtype=np.uint8) * 255

    # Draw grid (simulating ECG paper)
    for x in range(0, width, 10):
        color = (220, 220, 255) if x % 50 != 0 else (180, 180, 255)
        thickness = 1 if x % 50 != 0 else 2
        cv2.line(img, (x, 0), (x, height), color, thickness)
    for y in range(0, height, 10):
        color = (220, 220, 255) if y % 50 != 0 else (180, 180, 255)
        thickness = 1 if y % 50 != 0 else 2
        cv2.line(img, (0, y), (width, y), color, thickness)

    # Generate ECG signal (simulated)
    x_axis = np.arange(width)
    y_axis = np.ones(width) * (height // 2)
    
    # Add R-peaks
    peak_indices = np.arange(100, width - 100, 150) 
    for p in peak_indices:
        # Simple waves as Gaussian-like peaks
        # P wave
        p_wave = 15 * np.exp(-((np.arange(width) - (p-40))**2) / 50)
        # QRS complex
        qrs_wave = 100 * np.exp(-((np.arange(width) - p)**2) / 10)
        # T wave
        t_wave = 25 * np.exp(-((np.arange(width) - (p+60))**2) / 100)
        
        y_axis -= (p_wave + qrs_wave + t_wave)

    # Add noise
    y_axis += np.random.normal(0, 2, width)

    # Draw the signal
    points = np.column_stack((x_axis, y_axis)).astype(np.int32)
    cv2.polylines(img, [points], False, (0, 0, 0), 2)

    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cv2.imwrite(output_path, img)
    print(f"Sample ECG generated at {output_path}")

if __name__ == "__main__":
    generate_sample_ecg("static/sample_ecg.png")
