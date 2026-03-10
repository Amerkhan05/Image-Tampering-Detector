import cv2
import numpy as np

# 🔍 Edge Detection
def edge_analysis(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    return edges


# 🔍 Noise Detection
def noise_analysis(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    noise = cv2.Laplacian(gray, cv2.CV_64F)
    return noise


# 🔥 Highlight Suspicious Regions
def highlight_suspicious_regions_with_mask(image, edges, noise):
    noise = np.uint8(np.absolute(noise))

    # Ensure same size
    noise = cv2.resize(noise, (edges.shape[1], edges.shape[0]))

    # Combine
    combined = cv2.addWeighted(edges, 0.5, noise, 0.5, 0)

    _, thresh = cv2.threshold(combined, 50, 255, cv2.THRESH_BINARY)

    result = image.copy()
    result[thresh > 0] = [0, 0, 255]

    return result, thresh


# 📊 Score Calculation
def calculate_tampering_score(edges, noise):
    edge_score = np.mean(edges)
    noise_score = np.mean(np.abs(noise))

    final_score = (edge_score + noise_score) / 2
    return final_score


# 🧠 ELA (Error Level Analysis)
def ela_analysis(image):
    temp_path = "temp.jpg"

    cv2.imwrite(temp_path, image, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    compressed = cv2.imread(temp_path)

    ela = cv2.absdiff(image, compressed)
    ela = cv2.convertScaleAbs(ela, alpha=10)

    return ela


def ela_score(ela):
    return np.mean(ela)