import streamlit as st
from notifications import send_notification
from cam import start_webcam, model
from gdrive import upload_detected_folders


import threading
import os


def run_script():
    os.system("python gdrive.py")


# Run the script in a new thread
thread = threading.Thread(target=run_script)
thread.start()

path = "https://ultralytics.com/images/zidane.jpg"

st.title("Smart Surveillance System")
content1 = "A security system that uses advanced technologies like artificial intelligence (AI), computer vision, " \
           "and machine learning to monitor and analyze video feeds in real-time. It enhances traditional surveillance " \
           "systems by automating the monitoring process, detecting anomalies, recognizing objects, " \
           "tracking movement, and even providing real-time alerts."
content2 = "Our model has two main features : \n" \
           "1. Instant Alert Notifications \n" \
           "2. Upload to Drive"
st.text(content1)
st.text(content2)

st.subheader("Enter image address :")
try:
    path = st.text_input("Enter any link")
    results = model(path)
    col1, col2 = st.columns(2)

    with col1:
        st.image(path, caption="Original Image")

    with col2:
        st.image(results.render(), caption="Detected Image")

except Exception as e:
    st.error(f"An unexpected error occurred: {str(e)}")

st.subheader("1. Access Webcam")
content3 = "This feature allows the application to access your device's webcam, enabling real-time video capture and " \
           "processing. By granting permission to use the webcam, users can interact with the app through facial " \
           "recognition, live video streaming, or other webcam-based functionalities."
st.text(content3)

if st.button("webcam"):
    start_webcam()

st.subheader("2. Instant Alert Notifications")
content4 = "Instant alert notifications are a key feature of modern smart surveillance systems, enabling real-time " \
           "communication with security personnel or users when suspicious activity is detected. These alerts are " \
           "designed to provide immediate information about potential security threats, allowing for quick action to " \
           "be taken. This proactive approach ensures enhanced security, faster response times, and greater peace of " \
           "mind for both residential and commercial environments."
st.text(content4)
message = st.text_area("Enter the message")
if st.button("Send Email"):
    if message:
        send_notification(message)
    else:
        message = "Alerting the user"
        send_notification(message)

st.subheader("3. Storing to the cloud")
content5 = "In a smart surveillance system, cloud storage allows for the secure and scalable storage of video footage " \
           "and sensor data captured by cameras and IoT devices. By storing data in the cloud, users can remotely " \
           "access live feeds, archived recordings, and real-time analytics from anywhere, ensuring constant " \
           "monitoring and quick retrieval of crucial information. The cloud infrastructure offers high availability, " \
           "automatic backups protecting sensitive surveillance data while enabling easy scalability for expanding " \
           "surveillance networks. This approach ensures that data is safely stored and accessible, even if local " \
           "hardware fails, providing peace of mind and continuous surveillance operations."
st.text(content5)

if st.button("Upload to cloud"):
    upload_detected_folders()
