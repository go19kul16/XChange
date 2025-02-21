import streamlit as st
import random
import string
import os

# Set up a directory for storing content (in a production environment, you'd use a cloud service)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Function to generate a random 4-digit PIN
def generate_pin():
    return ''.join(random.choices(string.digits, k=4))

# Function to send text or file
def send_file_or_text():
    choice = st.radio("Choose to send a file or text", ("File", "Text"))
    pin = generate_pin()  # Generate PIN before storing any content

    if choice == "Text":
        text_to_send = st.text_area("Enter the text you want to send:")
        if text_to_send:
            st.write(f"Your PIN is: {pin}")
            # Store the text content in a file with the PIN as the filename
            with open(os.path.join(UPLOAD_FOLDER, f"{pin}.txt"), 'w') as f:
                f.write(text_to_send)
            return pin
    elif choice == "File":
        uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf", "jpg", "png", "docx"])
        if uploaded_file is not None:
            st.write(f"Your PIN is: {pin}")
            # Save the file with the PIN as the filename
            with open(os.path.join(UPLOAD_FOLDER, f"{pin}_{uploaded_file.name}"), 'wb') as f:
                f.write(uploaded_file.getbuffer())
            return pin
    return None

# Function to receive content using the PIN
def receive_content():
    pin_entered = st.text_input("Enter the PIN to receive the content:")

    if pin_entered:
        file_path = os.path.join(UPLOAD_FOLDER, f"{pin_entered}.txt")
        # Check if it's a text file first
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
            st.write("Text received:")
            st.write(content)
        else:
            # If not a text file, check for any file that contains the PIN
            for file in os.listdir(UPLOAD_FOLDER):
                if pin_entered in file:
                    st.write(f"File received: {file}")
                    with open(os.path.join(UPLOAD_FOLDER, file), 'rb') as f:
                        st.download_button(label="Download the file", data=f, file_name=file)
                    break
            else:
                st.error("Incorrect PIN. Please try again.")

# Main Streamlit UI
st.title("Secure File/Text Transfer App")

# Create two columns: one for sending, one for receiving
col1, col2 = st.columns(2)

# **Sender Column (col1)**:
with col1:
    st.header("Send Content")
    pin = send_file_or_text()
    if pin:
        st.success(f"Your PIN is: {pin}")  # Inform the user about the PIN for sending

# **Receiver Column (col2)**:
with col2:
    st.header("Receive Content")
    receive_content()
    
