import streamlit as st
import numpy as np
import cv2

from forensics import (
    edge_analysis,
    noise_analysis,
    highlight_suspicious_regions_with_mask,
    calculate_tampering_score,
    ela_analysis,
    ela_score
)

st.set_page_config(page_title="Image Tampering Detector", layout="wide")

st.title("🕵️‍♂️ Image Tampering Detector AI")

uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Convert uploaded file to image
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)

    st.image(image, caption="Uploaded Image", use_column_width=True)

    # 🔍 Processing
    edges = edge_analysis(image)
    noise = noise_analysis(image)

    result, mask = highlight_suspicious_regions_with_mask(image, edges, noise)

    edge_noise_score = calculate_tampering_score(edges, noise)

    ela = ela_analysis(image)
    ela_val = ela_score(ela)

    final_score = (edge_noise_score + ela_val) / 2

    # 📊 Display Scores
    st.subheader("📊 Analysis Results")
    st.write(f"Edge+Noise Score: {edge_noise_score:.2f}")
    st.write(f"ELA Score: {ela_val:.2f}")
    st.write(f"Final Score: {final_score:.2f}")

    # 🧠 Verdict
    if final_score < 5:
        st.success("✅ Image Looks Authentic")
    elif final_score < 15:
        st.warning("⚠️ Suspicious (Possible Tampering)")
    else:
        st.error("❌ Image is Tampered")

    # 🖼️ Show Outputs
    st.subheader("🔍 Processed Outputs")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.image(edges, caption="Edges")

    with col2:
        st.image(np.uint8(np.absolute(noise)), caption="Noise")

    with col3:
        st.image(result, caption="Tampered Regions Highlighted")

    st.image(ela, caption="ELA Analysis")