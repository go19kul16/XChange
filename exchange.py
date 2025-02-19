import streamlit as st
import random
import string
import os
import zipfile

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
        uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf", "jpg", "png", "docx", "zip"])
        if uploaded_file is not None:
            st.write(f"Your PIN is: {pin}")
            # If the file is a ZIP, handle it differently
            if uploaded_file.name.endswith(".zip"):
                with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
                    # Extract ZIP contents
                    zip_path = os.path.join(UPLOAD_FOLDER, pin)
                    os.makedirs(zip_path, exist_ok=True)
                    zip_ref.extractall(zip_path)
                    st.write(f"ZIP file extracted to: {zip_path}")
            else:
                # Save other files with the PIN as part of the filename
                with open(os.path.join(UPLOAD_FOLDER, f"{uploaded_file.name}"), 'wb') as f:
                    f.write(uploaded_file.getbuffer())
            return pin
    return None

# Function to receive content using the PIN
def receive_content():
    pin_entered = st.text_input("Enter the PIN to receive the content:")

    if pin_entered:
        # Check if it's a text file first
        text_file_path = os.path.join(UPLOAD_FOLDER, f"{pin_entered}.txt")
        if os.path.exists(text_file_path):
            with open(text_file_path, 'r') as f:
                content = f.read()
            st.write("Text received:")
            st.write(content)
        else:
            # If not a text file, check for files that contain the PIN (for non-text files, including ZIPs)
            found = False
            for file in os.listdir(UPLOAD_FOLDER):
                if pin_entered in file:
                    found = True
                    file_path = os.path.join(UPLOAD_FOLDER, file)
                    st.write(f"File received: {file}")

                    # If it's a ZIP, allow extraction and list extracted files
                    if file.endswith(".zip"):
                        # Extract the ZIP file first
                        zip_extract_path = os.path.join(UPLOAD_FOLDER, pin_entered)
                        os.makedirs(zip_extract_path, exist_ok=True)
                        
                        with zipfile.ZipFile(file_path, 'r') as zip_ref:
                            zip_ref.extractall(zip_extract_path)
                            st.write(f"ZIP file extracted to: {zip_extract_path}")
                        
                        # List the extracted files and provide download links
                        extracted_files = os.listdir(zip_extract_path)
                        if extracted_files:
                            st.write("Extracted files:")
                            for extracted_file in extracted_files:
                                extracted_file_path = os.path.join(zip_extract_path, extracted_file)
                                # Provide download button for each extracted file
                                with open(extracted_file_path, 'rb') as f:
                                    st.download_button(
                                        label=f"Download {extracted_file}",
                                        data=f,
                                        file_name=extracted_file
                                    )
                        else:
                            st.write("No files extracted from the ZIP.")
                    else:
                        # For non-ZIP files, just provide a download button
                        if os.path.isfile(file_path):  # Ensure it's not a directory
                            with open(file_path, 'rb') as f:
                                st.download_button(label="Download the file", data=f, file_name=file)
                    break

            if not found:
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
